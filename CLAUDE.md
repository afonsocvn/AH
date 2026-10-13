# Registo Pessoal de Saúde (Health Data Registry)

Este repositório é um **registo de saúde pessoal**, focado numa única pessoa
(o utilizador). O objetivo é manter um histórico estruturado dos seus dados
de saúde ao longo do tempo — peso, sinais vitais, exames, exercício,
medicação e bem-estar geral — para que seja fácil ver tendências e diferenças
entre registos.

## Como este projeto deve ser usado

- `data/profile.yaml` contém a informação de base (relativamente estável):
  idade/data de nascimento, altura, sexo, condições crónicas, alergias,
  medicação atual, historial relevante. Atualiza este ficheiro quando algo
  de base muda (nova condição diagnosticada, mudança de medicação crónica,
  etc.) em vez de repetir a informação em cada entrada de log.
- `logs/` contém séries temporais — cada ficheiro é uma lista de entradas
  com `date:` em formato ISO (`YYYY-MM-DD`). Cada novo registo é uma entrada
  **nova**, adicionada ao fundo da lista — nunca apagar ou reescrever
  entradas antigas, este é um histórico.
- `logs/measurements.yaml` — peso, IMC, composição corporal, sinais vitais
  (tensão arterial, frequência cardíaca, etc.).
- `logs/exams.yaml` — resultados de análises e exames médicos, com o tipo de
  exame, valores e, se relevante, intervalo de referência.
- `logs/exercise.yaml` — treinos e atividade física.
- `logs/medications.yaml` — medicação e suplementos, incluindo alterações de
  dose ao longo do tempo (isto é histórico, diferente do estado atual em
  `data/profile.yaml`).
- `logs/symptoms.md` — notas em texto livre sobre sintomas, energia, sono,
  humor, bem-estar geral. Não precisa de ser estruturado.
- `logs/lesoes.yaml` — lesões/dores relacionadas com treino (ex: tendinite,
  dores articulares), com zona, estado e evolução ao longo do tempo. Usar
  para acompanhar recuperação, não só registar o episódio inicial.
- `data/objetivos.yaml` — objetivos ativos (ex: prova/evento com data,
  tempo-alvo), com histórico de revisões. Estado atual, não um log — mas
  cada objetivo guarda o histórico das suas revisões.
- `data/modelo_treino.md` — especificação do modelo quantitativo de
  treino (eficiência aeróbica, previsões cruzadas, sinais de alerta de
  cadência, sensibilidade ao calor). Ler antes de qualquer análise de
  performance ou prescrição de treino.
- `scripts/analise_treino.py` — calcula a tendência de Efficiency Factor
  (velocidade/FC) a partir de `logs/exercise.yaml`. Correr sempre que
  houver corridas fáceis novas desde a última análise (`python3
  scripts/analise_treino.py logs/exercise.yaml`).
- `data/equipamento.yaml` — sapatilhas e quilómetros acumulados (fator
  de lesão mensurável).

## Comportamento esperado

Quando o utilizador fornecer novos dados (uma medição, um resultado de
análises, uma sessão de exercício, uma nota sobre como se sente, etc.):

1. Identifica o(s) ficheiro(s) certo(s) em `logs/` e acrescenta uma nova
   entrada com a data de hoje (ou a data indicada pelo utilizador).
2. Compara com a entrada anterior mais recente da mesma métrica e refere a
   diferença de forma clara e breve (ex: "peso desceu 1.2 kg desde 2026-07-01",
   "tensão arterial subiu ligeiramente face à última medição").
3. Se os novos dados implicarem uma mudança de base (ex: nova medicação
   crónica, novo diagnóstico), atualiza também `data/profile.yaml`.
4. Nunca inventes valores. Se faltar informação, pergunta ou deixa o campo
   a `null`/vazio.
5. Este é um histórico — usa o histórico git (commits) como registo adicional
   de mudanças ao longo do tempo, além das próprias entradas datadas.
6. **Confirma sempre a data real de hoje antes de a usar num registo** —
   nunca assumas a data a partir do contexto de uma corrida/evento.
7. **Faz `git push` para o remoto a cada poucas alterações, não só no fim
   de uma sessão longa.** Este ambiente é efémero e todo o histórico local
   já se perdeu DUAS VEZES neste projeto por falta de push atempado
   (ver git log / pedir ao utilizador para confirmar que o acesso de
   escrita ao GitHub está autorizado). Se o push falhar por falta de
   autorização, diz isso claramente ao utilizador e sugere os links de
   autorização em vez de assumir que vai resolver-se sozinho.

## Coaching: plano dinâmico, não estático (desde 2026-10-12)

A partir de 2026-10-12 o foco deixou de ser a maratona (pausada, não
cancelada — ver `data/objetivos.yaml`). O foco passa a ser 5km, 10km,
21km (meia maratona) e trail, com a Meia Maratona de Cascais (final de
fevereiro de 2027, data exata por confirmar) como próxima prova concreta.

O utilizador pediu explicitamente um treinador direto — análises honestas
e realistas, não conversa mole — e um **plano dinâmico, não um calendário
fixo escrito à partida**. A razão: planos rígidos partem-se quando a vida
acontece (doença, lesão, férias), como se viu na maratona.

### Filosofia (desde 2026-10-13): performance geral do corpo, não running-maximalismo

O utilizador foi explícito: "isto não é mega sério para mim". Faz
escalada, surf, e outras atividades, e quer o corpo com melhor
performance em geral — a corrida (e a Meia de Cascais) é um objetivo
dentro disso, não o projeto inteiro. Isto significa:

- **Não tratar dias sem corrida, ou semanas com escalada/surf em vez de
  treino, como desvios a corrigir.** São inputs válidos, não falhas.
- **Previsões e potencial a longo prazo são intervalos realistas, não
  valores exatos nem promessas** (ver `data/modelo_treino.md` secção 3.1
  e 3.2) — o utilizador quer ser levado a sério sobre onde pode chegar,
  sem exagero nem falsa precisão.
- `logs/exercise.yaml` já aceita qualquer `tipo` de atividade (não só
  "corrida") — registar escalada/surf/etc. da mesma forma quando o
  utilizador mencionar, não só correr.
- O objetivo final é "ajudar dentro da flexibilidade" — sugestões que
  encaixam na vida real do utilizador, não um programa rígido que ele
  tem de servir.

Isto significa, para qualquer sessão futura deste projeto:

1. **Nunca escrever um plano de treino de várias semanas de uma vez.**
   Propor sempre só os próximos 1-4 dias, com base no estado atual.
2. **Antes de prescrever o próximo treino, olhar para:**
   - `logs/exercise.yaml` — carga/intensidade recente, há quanto tempo foi
     o último treino duro, padrão de fadiga.
   - `logs/lesoes.yaml` e `logs/symptoms.md` — qualquer dor/lesão ativa.
   - O que o utilizador disser sobre como se sente nesse momento.
   - Tempo até à próxima prova em `data/objetivos.yaml`.
3. **Se houve uma paragem** (doença, lesão, férias, o que for): não voltar
   ao "ponto onde o plano dizia que estarias". Recalcular a partir de onde
   o utilizador está agora. Nunca tentar compensar tempo perdido com
   aumento brusco de carga.
4. **Ser direto.** Se uma marca não bate certo com o esforço relatado, ou
   um treino correu mal, dizer isso claramente — o utilizador pediu
   análises honestas, não validação.
5. `data/objetivos.yaml` passa a ter um objetivo por distância (5km, 10km,
   21km, trail), cada um com PB atual e objetivo, em vez de um único
   objetivo de maratona. Atualizar o PB sempre que houver um treino/prova
   que o bata.
6. **Usar o modelo quantitativo, não só intuição.** Antes de prescrever
   ou analisar performance: correr `scripts/analise_treino.py` para a
   tendência de EF, consultar `queryTrainingLoadAssessment` +
   `queryRecoveryStatus` da Coros MCP para carga/recuperação ao vivo, e
   ler `data/modelo_treino.md` para o resto (previsões cruzadas Riegel,
   sinal de alerta de cadência <78-80, sensibilidade ao calor). Nunca
   usar só a previsão algorítmica da Coros (`queryFitnessAssessmentOverview`)
   sem a comparar com estimativas de campo — é sistematicamente otimista.
7. **Pedir dados leves ao longo do tempo, sem burocracia:** peso
   (`logs/measurements.yaml`), o que comeu antes/durante treinos
   importantes, sapatilhas/km acumulados (`data/equipamento.yaml`),
   temperatura/condições quando relevante. Só perguntar quando vier a
   propósito, não como checklist obrigatório.

## Privacidade

Estes são dados de saúde pessoais e sensíveis. O repositório remoto
(`afonsocvn/AH` no GitHub) deve ser mantido privado. Confirma com o
utilizador antes de qualquer ação que exponha estes dados publicamente
(tornar o repo público, partilhar um link, etc.) — mas não adies
indefinidamente o `git push` de rotina para o remoto privado por receio de
privacidade, pois isso já causou perda de dados duas vezes.
