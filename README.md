# Registo de Saúde Pessoal

Registo pessoal de dados de saúde, mantido ao longo do tempo com a ajuda do
Claude Code. Ver `CLAUDE.md` para o contexto completo sobre como este
repositório está organizado e como deve ser usado.

## Estrutura

```
data/
  profile.yaml        # dados de base: idade, altura, condições, medicação atual, etc.
  objetivos.yaml       # objetivos ativos (ex: maratona), com histórico de revisões
logs/
  measurements.yaml   # peso, IMC, composição corporal, sinais vitais
  exams.yaml            # análises e exames médicos
  exercise.yaml          # treinos e atividade física
  medications.yaml        # histórico de medicação e suplementos
  symptoms.md               # notas livres sobre sintomas e bem-estar
  lesoes.yaml                # lesões/dores relacionadas com treino
```

## Nota

Este repositório contém dados de saúde sensíveis. Se for tornado público ou
partilhado, os dados devem ser removidos ou anonimizados primeiro.
