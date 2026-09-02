# Status do projeto

- Data de referencia: 2026-09-02
- Fonte normativa: `PLANO_DIRETOR_MESTRE_BENCHMARK_IA_ML.pdf`
- Gate atual: `B2 - IN REVIEW`
- Ultimo gate vigente aprovado: `B1`
- CHANGE-ID ativo: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`
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
- Suite atual: `45 passed, 3 skipped` apos `python -m pip install -e ".[dev]"`; os skips cobrem symlinks indisponiveis no ambiente.
- Skill `gate-review` valida pelo `scripts/skill_validator.py`.

Essa evidencia pode ser reaproveitada, mas deve ser revalidada contra os criterios formais de B1-B3.

## Gate review vigente

Resultado B1: `PASS` em 2026-09-02, por aprovacao explicita do responsavel do projeto.

| Gate | Estado | Evidencia ou bloqueador principal |
| --- | --- | --- |
| B0 | PASS historico | charter e revisao B0/B1 de 2026-08-31 |
| B1 | PASS | matriz e protocolos canonicos aprovados como framework; parametros quantitativos exigem preregistro posterior |
| B2 | IN REVIEW | contrato, manifest/schema, lifecycle e testes possuem prototipos executaveis |
| B3 | PARTIAL, sem avanco linear | runner, registry e reproducao existem, mas dependem de fechamento B2 |
| B4-B10 | NOT STARTED como gates | experimentos existentes sao exploratorios e nao cobrem os construtos normativos |
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

Executar a revisao formal B2 contra contrato neutro, lifecycle, manifest/schema, determinismo, timeouts, limites e conformidade. Parametros quantitativos das baterias continuam fora de freeze e nenhum conjunto selado deve ser criado.

## Handoff

- Agente: Codex
- Objetivo: B1 aprovado; preparar revisao formal B2
- Plano: `docs/CORRECTIVE_REVIEW_PLAN.md`
- Comandos-base: `python -m pytest -q`; `python scripts/skill_validator.py`; validacoes focadas registradas nos commits
- Validacao limpa: `45 passed, 3 skipped`; governance e skill validator passaram; run publico C1 rastreavel passou
- Riscos: aprovacao cientifica, infraestrutura sealed, red team separado e replicacao independente exigem autoridade/evidencia externa
