# Instrucoes para agentes

Este projeto implementa um benchmark cientifico de IA/ML. Leia `README.md` e `docs/AGENT_HANDOFF.md` antes de editar.

Skills reutilizaveis ficam em `.github/skills/` e sao catalogadas em `docs/SKILLS_CATALOG.md`. O repositorio e a fonte canonica; copias para perfis locais sao derivadas.

## Regras inviolaveis

- O plano diretor PDF e a fonte normativa inicial.
- Nenhuma arquitetura candidata participa antes da barreira B14/B15.
- Adapters convertem protocolo; nao extraem features, adicionam memoria, hints, ground truth ou correcoes.
- Raw data, seeds, configs, hashes e run_id devem permanecer rastreaveis.
- Mudancas em construto, ambiente, reward, metrica, scoring, seeds, budget ou protocolo precisam de CHANGE-ID.
- Nao fazer commit, push, pull destrutivo ou alterar mudancas de terceiros sem autorizacao.

## Fluxo minimo

1. Verifique o gate atual e `git status`.
2. Leia a decisao ou contrato mais proximo da tarefa.
3. Declare hipotese, teste barato e menor mudanca.
4. Edite somente o slice necessario.
5. Rode validacao focada imediatamente.
6. Atualize status, decisoes e evidencias.

Ao fechar um gate ou marco grande, execute a skill `gate-review`. Extraia uma nova skill somente quando houver um procedimento repetivel, validacao executavel e limites claros. Nunca promova uma skill que contenha dados sealed, candidatos, segredos, hints ou ground truth.

O estado atual e documental, sem implementacao do core. O proximo passo recomendado e aprovar B0/B1 e criar a matriz de construtos das 11 capacidades.
