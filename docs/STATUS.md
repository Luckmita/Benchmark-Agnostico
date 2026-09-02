# Status do projeto

- Data de referencia: 2026-09-02
- Fonte normativa: `PLANO_DIRETOR_MESTRE_BENCHMARK_IA_ML.pdf`
- Gate atual: `B4 - IN REVIEW`
- Ultimo gate vigente aprovado: `B3`
- CHANGE-ID ativo: `CHG-2026-09-02-B3-REPRODUCIBLE-RUNS`
- Branch de trabalho: `fix/chg-2026-09-01-gate-realignment`
- Barreira: nenhuma arquitetura candidata antes da conclusao de B14 e B15; submissao somente em B16

## Resultado da auditoria de transicao

Os registros de freeze produzidos em 2026-09-01 sao preservados como historico, mas foram superados como fonte de status. Eles nao demonstram o fechamento linear de B1-B15 e nao autorizam conjunto selado, release candidate, replicacao independente ou candidatos.

Principais motivos:

- a matriz B1 mantinha campos `PENDENTE` definidos como bloqueadores;
- a implementacao C3-C11 divergia da taxonomia do plano diretor;
- capacidades marcadas `READY` foram resumidas como validadas e congeladas;
- o batch calculava apenas diferencas de media, sem o teste estatistico declarado;
- os resultados agregados nao continham a cadeia completa de artefatos por `run_id`;
- B11, B12, B13 e B15 nao possuiam evidencias reproduziveis;
- B14/B15 foram incorretamente descritos como fase de inscricao, que pertence a B16.

## Evidencia tecnica existente

- Componentes prototipais de API, runner isolado, registry append-only, artifacts e avaliacao multi-seed.
- Tarefa publica exploratoria C1 baseada em bandit.
- Experimentos publicos exploratorios derivados de bandit, sem validade de freeze.
- Suite atual: `55 passed, 3 skipped` no ambiente B3 limpo; os skips cobrem symlinks indisponiveis no ambiente.
- Skill `gate-review` valida pelo `scripts/skill_validator.py`.

Essa evidencia pode ser reaproveitada, mas deve ser revalidada contra os criterios formais de B1-B3.

## Gate review vigente

Resultado B3: `PASS` em 2026-09-02, apos reproducao limpa da infraestrutura e run publico rastreavel.

| Gate | Estado | Evidencia ou bloqueador principal |
| --- | --- | --- |
| B0 | PASS historico | charter e revisao B0/B1 de 2026-08-31 |
| B1 | PASS | matriz e protocolos canonicos aprovados como framework; parametros quantitativos exigem preregistro posterior |
| B2 | PASS | contrato v0.1, manifest/schema, lifecycle, capabilities e testes de conformidade |
| B3 | PASS | ambiente versionado, runner, registry, artifacts imutaveis, hashes, CLI e reproducao limpa |
| B4 | IN REVIEW | selecionar e validar controles/baselines pertinentes por construto |
| B5-B10 | NOT STARTED como gates | prototipos existentes nao cobrem validacao confirmatoria |
| B11 | NOT STARTED | sem validacao completa do benchmark |
| B12 | NOT STARTED | sem red team independente |
| B13 | NOT STARTED | sem repositorio/storage selado separado |
| B14 | BLOCKED | depende de B1-B13 |
| B15 | BLOCKED | exige terceiro independente |
| B16 | PROHIBITED | primeira submissao somente apos a barreira |

A matriz detalhada esta em `docs/reviews/GATE_AUDIT_2026-09-01.md`.

## Marco corretivo concluido em 2026-09-02

1. Status, decisoes, historico e taxonomia canonica corrigidos.
2. Instalacao editavel, testes e run publico rastreavel implementados.
3. Contratos e evidencias B2/B3 melhorados sem alegar fechamento prematuro.
4. Prototipos publicos C1-C11 realinhados; scripts de falso freeze/`PASS` desativados.
5. Bloqueios externos de B12, B13 e B15 registrados sem simular sua conclusao.

Revisao: `docs/reviews/CORRECTIVE_MILESTONE_REVIEW_2026-09-02.md`.

## Proximo passo executavel

Construir a matriz B4 de controles negativos/positivos e baselines tecnicamente pertinentes, começando pela vertical C1. Nenhum conjunto selado ou candidato deve ser criado.

## Handoff

- Agente: Codex
- Objetivo: B3 aprovado; iniciar matriz e validacao B4
- Plano: `docs/CORRECTIVE_REVIEW_PLAN.md`
- Comandos-base: `python -m pytest -q`; `python scripts/skill_validator.py`; validacoes focadas registradas nos commits
- Validacao atual: `55 passed, 3 skipped`; ambiente limpo, governance e skill validator passaram
- Riscos: aprovacao cientifica, infraestrutura sealed, red team separado e replicacao independente exigem autoridade/evidencia externa
