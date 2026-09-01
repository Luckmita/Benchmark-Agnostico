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
- [Protocolos C2-C11](docs/protocols/): propostas de 10 capacidades adicionais.
- [Aprovacao C2-C11](docs/reviews/C2_C11_BATCH_APPROVAL_2026-09-01.md): autorizacao para implementacao controlada em lote.
- [Revisao B0/B1](docs/reviews/B0_B1_GATE_REVIEW_2026-08-31.md): registro de aprovacao e evidencias.
- [Desenho tecnico](docs/TECHNICAL_DESIGN.md): API, componentes, dados, reproducibilidade e stack proposta.
- [Politica Git](docs/GIT_POLICY.md): organizacao de pastas, commits, branches, pull/push e revisao.
- [Manual de agentes](docs/AGENT_HANDOFF.md): protocolo para qualquer agente continuar o projeto.
- [Decisoes em aberto](docs/DECISIONS.md): pontos que exigem aprovacao antes de congelar a v1.

## Estado atual

Somente o plano diretor foi recebido. O projeto esta em B0, com a documentacao operacional em elaboracao. Nenhum codigo de benchmark ou adapter de candidato deve ser iniciado antes da aprovacao do charter.

## Fonte de verdade

Em caso de conflito, a ordem e: plano diretor aprovado, decisoes registradas em `docs/DECISIONS.md`, contratos versionados no codigo e demais documentacao. Toda alteracao cientifica deve possuir CHANGE-ID e evidencias.

## Skills

Ao fechar cada gate, use `.github/skills/gate-review/SKILL.md` para verificar evidencias e procurar procedimentos reutilizaveis. Valide com `python scripts/skill_validator.py`; promova com `python scripts/skill_promote.py <nome>` e exporte para outras IAs com `python scripts/skill_export.py`.
