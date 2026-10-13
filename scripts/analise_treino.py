#!/usr/bin/env python3
"""
Analise quantitativa do historico de treino (logs/exercise.yaml).

Calcula metricas derivadas dos dados reais do atleta, nao de medias de
populacao:

1. Efficiency Factor (EF) = pace (km/h) / FC media, para corridas faceis.
   EF mais alto = mais velocidade por batimento = melhor eficiencia
   aerobica. E a mesma logica usada por treinadores de endurance
   (ex: TrainingPeaks "aerobic efficiency"), aplicada aqui aos dados
   proprios do atleta, nao a uma formula generica.
2. Tendencia de EF ao longo do tempo (regressao linear simples) —
   mostra se a eficiencia aerobica esta a melhorar, estagnada ou a piorar.
3. Resumo de carga recente (dependente de chamada ao Coros MCP, nao
   incluido aqui — ver data/objetivos.yaml -> estado_coros_*).

Uso: python3 analise_treino.py /caminho/para/logs/exercise.yaml
"""
import sys
import re
import datetime

try:
    import yaml
except ImportError:
    print("Precisa de pyyaml instalado (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

EASY_HR_MIN = 125
EASY_HR_MAX = 155
MIN_DIST_KM = 4.0
EXCLUDE_NAME_PATTERNS = [
    r"threshold", r"marathon pace", r"maratona", r"interval",
    r"aceleraç", r"aceleracoes",
]


def parse_pace_to_minkm(pace_str):
    """'5:38/km' -> 5.6333 (minutos por km, float)"""
    if not pace_str:
        return None
    m = re.match(r"(\d+):(\d+)", pace_str)
    if not m:
        return None
    mins, secs = int(m.group(1)), int(m.group(2))
    return mins + secs / 60.0


def is_easy_run(entry):
    nome = (entry.get("nome") or "").lower()
    for pat in EXCLUDE_NAME_PATTERNS:
        if re.search(pat, nome):
            return False
    hr = entry.get("fc_media")
    dist = entry.get("distancia_km")
    if hr is None or dist is None:
        return False
    if not (EASY_HR_MIN <= hr <= EASY_HR_MAX):
        return False
    if dist < MIN_DIST_KM:
        return False
    if entry.get("resultado"):  # race/DNF entries excluded
        return False
    return True


def compute_ef(entry):
    """EF = km/h dividido por FC media. Usa pace_medio (ou pace_medio_em_movimento)."""
    pace_str = entry.get("pace_medio") or entry.get("pace_medio_em_movimento")
    pace_minkm = parse_pace_to_minkm(pace_str)
    hr = entry.get("fc_media")
    if pace_minkm is None or not hr:
        return None
    kmh = 60.0 / pace_minkm
    return kmh / hr


def linear_trend(xs, ys):
    """Regressao linear simples (minimos quadrados), sem numpy."""
    n = len(xs)
    if n < 2:
        return None, None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    if den == 0:
        return None, None
    slope = num / den
    intercept = mean_y - slope * mean_x
    return slope, intercept


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "logs/exercise.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)

    entries = data.get("entries", [])
    easy = [e for e in entries if is_easy_run(e)]

    rows = []
    for e in easy:
        ef = compute_ef(e)
        if ef is None:
            continue
        date = datetime.date.fromisoformat(str(e["date"]))
        rows.append((date, ef, e.get("nome"), e.get("distancia_km"), e.get("fc_media")))

    rows.sort(key=lambda r: r[0])

    print(f"Corridas faceis identificadas (FC {EASY_HR_MIN}-{EASY_HR_MAX}, >= {MIN_DIST_KM}km, "
          f"excluindo sessoes de qualidade/prova): {len(rows)} de {len(entries)} totais\n")

    print(f"{'Data':<12} {'EF':<8} {'FC':<5} {'Dist':<7} Nome")
    for date, ef, nome, dist, hr in rows:
        print(f"{date}  {ef:.4f}  {hr:<5} {dist:<7} {nome}")

    if len(rows) >= 4:
        day0 = rows[0][0]
        xs = [(r[0] - day0).days for r in rows]
        ys = [r[1] for r in rows]
        slope, intercept = linear_trend(xs, ys)
        if slope is not None:
            weeks_span = (rows[-1][0] - rows[0][0]).days / 7.0
            ef_change = slope * (rows[-1][0] - rows[0][0]).days
            pct_change = (ef_change / rows[0][1]) * 100 if rows[0][1] else None
            print(f"\n--- Tendencia (regressao linear, {len(rows)} pontos, {weeks_span:.1f} semanas) ---")
            print(f"EF no inicio do periodo (ajustado): {intercept:.4f}")
            print(f"Variacao de EF por semana: {slope*7:+.5f}")
            print(f"Variacao total no periodo: {ef_change:+.4f} "
                  f"({pct_change:+.1f}%)" if pct_change is not None else "")
            if slope > 0:
                print("Interpretacao: eficiencia aerobica A MELHORAR (mais km/h por batimento ao longo do tempo).")
            elif slope < 0:
                print("Interpretacao: eficiencia aerobica A PIORAR ou fadiga acumulada — investigar causa (carga, doenca, calor).")
            else:
                print("Interpretacao: eficiencia aerobica estavel.")


if __name__ == "__main__":
    main()
