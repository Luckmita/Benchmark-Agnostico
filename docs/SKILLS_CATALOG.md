# Catalogo de skills

O repositorio e a fonte canonica. Skills aprovadas podem ser exportadas para o perfil local, mas nunca o contrario.

| Nome | Status | Gate de origem | Gatilho | Evidencia |
| --- | --- | --- | --- | --- |
| `gate-review` | active | B0 | Fechamento de gate ou marco grande | Esta skill e o primeiro caso vertical; validada pelo `scripts/skill_validator.py` |

## Status

- `proposed`: criada, mas ainda nao aprovada para uso automatico.
- `active`: validada e disponivel para agentes.
- `deprecated`: preservada para historico, nao recomendada para novos trabalhos.

## Regras

Cada skill deve possuir `SKILL.md` com frontmatter contendo `name` e `description`, e as secoes `When to use`, `Inputs`, `Procedure`, `Output`, `Validation` e `Limits`. Toda skill ativa precisa de evidencia reproduzivel, gate de origem e validacao automatica.

Skills nao podem conter candidatos, seeds seladas, tarefas ocultas, ground truth, hints, segredos ou instrucoes que alterem a neutralidade do benchmark.
