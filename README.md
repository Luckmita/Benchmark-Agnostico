# Benchmark Agnostico para IA e ML

Este repositorio implementara uma plataforma independente para avaliar capacidades funcionais observaveis de agentes e arquiteturas de IA/ML. O documento normativo inicial e `PLANO_DIRETOR_MESTRE_BENCHMARK_IA_ML.pdf`.

## Regra principal

O benchmark deve ser construido, validado e congelado antes da entrada de qualquer arquitetura candidata. Nenhum resultado de candidato pode orientar tarefas, metricas, pesos, seeds, budgets ou o conjunto selado da versao avaliada.

## Documentacao de continuidade

- [Plano de execucao](docs/EXECUTION_PLAN.md): gates, entregaveis, criterios de saida e ordem de trabalho.
- [Charter B0](docs/CHARTER_B0.md): missao, escopo, papeis e criterios de governanca.
- [Matriz B1](docs/CONSTRUCT_MATRIX_B1.md): construtos, hipoteses, controles e pendencias cientificas.
- [Preregistracao C1](docs/protocols/C1_LEARNING_PREREGISTRATION.md): proposta da primeira bateria de aprendizagem.
- [Aprovacao C1](docs/reviews/C1_PROTOCOL_APPROVAL_2026-09-01.md): autorizacao para implementacao controlada.
- [Protocolos C1-C11](docs/protocols/README.md): indice canonico corretivo das onze capacidades.
- [Aprovacao historica C2-C11](docs/reviews/C2_C11_BATCH_APPROVAL_2026-09-01.md): registro preservado, sem efeito de freeze apos a revisao corretiva.
- [Revisao B0/B1](docs/reviews/B0_B1_GATE_REVIEW_2026-08-31.md): registro de aprovacao e evidencias.
- [Desenho tecnico](docs/TECHNICAL_DESIGN.md): API, componentes, dados, reproducibilidade e stack proposta.
- [Politica Git](docs/GIT_POLICY.md): organizacao de pastas, commits, branches, pull/push e revisao.
- [Manual de agentes](docs/AGENT_HANDOFF.md): protocolo para qualquer agente continuar o projeto.
- [Decisoes em aberto](docs/DECISIONS.md): pontos que exigem aprovacao antes de congelar a v1.

## Estado atual

Os gates B0-B3 foram aprovados com evidencias versionadas. B4 e o gate atual, dedicado a controles e baselines tecnicamente pertinentes. Existem tarefas publicas de desenvolvimento, mas nenhum gate B4-B15 esta atualmente aprovado como concluido.

Os registros de freeze de 2026-09-01 sao preservados como historico, porem nao autorizam conjunto selado, release candidate, replicacao ou submissao. O plano e a auditoria vigentes estao em [Plano de revisao corretiva](docs/CORRECTIVE_REVIEW_PLAN.md) e [Auditoria de gates](docs/reviews/GATE_AUDIT_2026-09-01.md).

Nenhuma arquitetura candidata pode entrar antes de B14 e B15 concluidos. A primeira submissao pertence a B16.

## Fonte de verdade

Em caso de conflito, a ordem e: plano diretor aprovado, decisoes registradas em `docs/DECISIONS.md`, contratos versionados no codigo e demais documentacao. Toda alteracao cientifica deve possuir CHANGE-ID e evidencias.

## Skills

Ao fechar cada gate, use `.github/skills/gate-review/SKILL.md` para verificar evidencias e procurar procedimentos reutilizaveis. Valide com `python scripts/skill_validator.py`; promova com `python scripts/skill_promote.py <nome>` e exporte para outras IAs com `python scripts/skill_export.py`.

## Ambiente de desenvolvimento

O ambiente B3 de referencia usa a versao registrada em `.python-version` e os pins de `requirements-dev.lock`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m pip install -e . --no-build-isolation --no-deps
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/skill_validator.py
```

Detalhes e limites: [ambiente de referencia B3](docs/ENVIRONMENT_B3.md).

Um run publico de desenvolvimento C1 pode ser produzido sem dados selados:

```powershell
python -m benchmark_core.cli run-public-c1 --output-root artifacts/public-demo --run-id demo-c1-seed-42 --seed 42
```

O comando cria `registry.jsonl` e os grupos `raw/`, `derived/`, `logs/`, `metrics/` e `manifest/` sob o `run_id`. Esses dados sao somente evidencia de infraestrutura/desenvolvimento; nao constituem benchmark congelado.
