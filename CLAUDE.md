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

## Privacidade

Estes são dados de saúde pessoais e sensíveis. O repositório remoto
(`afonsocvn/AH` no GitHub) deve ser mantido privado. Confirma com o
utilizador antes de qualquer ação que exponha estes dados publicamente
(tornar o repo público, partilhar um link, etc.) — mas não adies
indefinidamente o `git push` de rotina para o remoto privado por receio de
privacidade, pois isso já causou perda de dados duas vezes.
