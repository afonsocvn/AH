# Modelo de treino pessoal — especificação

Isto documenta o modelo usado para analisar o treino e gerar as próximas
sessões. Não é um plano escrito à partida (ver `CLAUDE.md`) — é o conjunto
de métricas, fórmulas e fontes de dados que alimentam cada decisão. Cada
secção diz: o que mede, de onde vêm os dados, qual a fórmula, e qual a
confiança atual (mais dados = mais confiança).

## 1. Carga e recuperação — motor: Coros, não reinventado

Não há vantagem em recriar isto: a Coros já usa um modelo validado
(impulso-resposta estilo Banister, carga aguda/crónica + rácio, o
equivalente a ATL/CTL/ACWR usado em TrainingPeaks/Strava).

- **Fonte:** `queryTrainingLoadAssessment` (carga curto/longo prazo,
  rácio, comentário) + `queryRecoveryStatus` (% recuperação, nível).
- **Uso:** gate principal antes de prescrever qualquer sessão dura.
  Rácio > ~1.3 sustentado = risco de lesão a subir (é literalmente o
  que precedeu o Aquiles/fascite em 2026-08/09).
- **Limite conhecido:** mede carga cardiovascular/muscular geral, NÃO
  sabe nada sobre lesões de tecido local (fascite, tendinite). Nunca
  usar "recovery 100%" como luz verde sem confirmar isso à parte.

## 2. Eficiência aeróbica (EF) — motor: script próprio

- **Fórmula:** `EF = velocidade (km/h) / FC média`, calculado só para
  corridas "fáceis" (FC 125-155, ≥4km, exclui sessões de qualidade/prova).
- **Fonte:** `logs/exercise.yaml` via `scripts/analise_treino.py`.
- **Porquê esta métrica:** isola a melhoria aeróbica real do ruído de
  pace (um dia pode correr mais rápido por boa forma OU por esforçar-se
  mais — EF normaliza por FC, por isso é mais fiável para ver progresso
  real ao longo de meses).
- **Resultado atual (2026-10-13, 52 corridas, 22.4 semanas):** EF subiu
  ~18.5% desde finais de abril. Interpretação: melhoria real de base
  aeróbica, consistente e sustentada, não um pico isolado.
- **Como usar:** recalcular sempre que houver >3-4 corridas fáceis novas
  desde a última vez. Uma quebra na tendência (EF a descer) é sinal de
  fadiga acumulada, doença a chegar, ou calor — não ignorar.

## 3. Previsões de prova — não usar só o algoritmo da Coros

A Coros dá previsões (`queryFitnessAssessmentOverview`) baseadas em
VO2max/economia — são **otimistas por definição** porque assumem pacing
e condições ideais, e não sabem nada sobre calor, fueling ou lesões
reais deste atleta. Comparação feita em 2026-10-13: Coros previu 3:22:59
de maratona; a estimativa de campo (a partir de um treino real de 35km)
deu ~3:59 — quase 40min de diferença.

**Modelo usado aqui:** extrapolação de Riegel (`T2 = T1 × (D2/D1)^1.06`)
a partir do **melhor esforço real conhecido mais próximo da distância**,
nunca a partir de VO2max isolado. Cada vez que há um esforço novo e mais
forte numa distância, a previsão dessa distância (e das vizinhas)
atualiza-se.

**Validação cruzada entre distâncias (2026-10-13):** usando os 3 melhores
registos reais (5k 22:03, 10k 50:01, 21k 1:46:40) para prever uns aos
outros via Riegel:
- 5k → prevê 10k em 45:52 e 21k em 1:41:13
- 10k → prevê 5k em 23:59 e 21k em 1:50:21
- 21k → prevê 5k em 23:09 e 10k em 48:17

O 10k real (50:01) é sistematicamente mais lento do que o que o 5k e o
21k preveem para ele — os outros dois concordam bem entre si. Conclusão:
**o registo de 10k provavelmente não foi um esforço máximo** (era uma
sessão de treino "Threshold Intervals", não um teste a sério) — há
margem real para um 10k mais rápido do que 50:01 se for testado a
esforço de prova. Isto é um insight real dos teus dados, não um palpite.

## 4. Sinal de alerta de cadência (prevenção de lesão)

- **Observação empírica (não genérica):** nos dois eventos onde este
  atleta teve problemas sérios (Cascais km16-18 e km27+, maratona de
  Carcavelos km22+), a cadência caiu de ~82-86 para **77-80 ou menos**
  imediatamente antes/durante a deterioração.
- **Uso:** em qualquer treino longo com dados de lap, assinalar se a
  cadência cair abaixo de ~78-80 de forma sustentada (não um lap
  isolado) — é um sinal de alerta mecânico específico deste corredor,
  antes mesmo de ele sentir dor.
- **Confiança:** baixa-média — só 2 episódios observados. Vai reforçar-se
  (ou refutar-se) com mais dados.

## 5. Sensibilidade ao calor

- **Dados disponíveis:** só 3 corridas com temperatura conhecida
  (Cascais 30°C, Parede 32-35°C, maratona Carcavelos 24°C) — API da
  Coros não devolve temperatura nos resumos de atividade, só nos
  ficheiros `.fit` detalhados.
- **Padrão observado (fraco, poucos pontos):** FC claramente mais alta
  nos primeiros km em calor forte (Cascais, Parede) vs. prova mais
  fresca (Carcavelos), mesmo com pace semelhante.
- **Confiança: baixa.** Precisa de mais pontos com temperatura conhecida
  para virar modelo a sério. Se partilhares a temperatura/condições dos
  próximos treinos (mesmo só "estava calor"/"fresco"), isto melhora.

## 6. Inclinação/terreno

- **Dados disponíveis:** só nos 3 treinos com `.fit` detalhado
  (ganho/perda de elevação por treino, não por km em todos).
- **Estado:** não há ainda dados suficientes para um modelo de
  custo-de-pace-por-declive pessoal. Fica para quando houver mais
  treinos com dados de lap detalhados (a maioria dos treinos "normais"
  importados via Coros MCP só tem o resumo, não os laps).

## Informação adicional que vou pedir ao longo do tempo (leve, não burocrático)

- **Peso** — já trackeado em `logs/measurements.yaml`, atualizar quando
  souberes um valor novo.
- **O que comeste antes/durante treinos importantes** — só nos longos ou
  se sentires algo estranho (GI, energia), não todos os dias.
- **Sapatilhas** — modelo e quilómetros acumulados (ver
  `data/equipamento.yaml`) — desgaste de sapatilha é fator de lesão real
  e mensurável, vale a pena trackear.
- **Temperatura/condições** quando achares relevante, para alimentar o
  modelo de calor.

Qualquer um destes, basta mencionares em conversa — não precisas de
formato especial.
