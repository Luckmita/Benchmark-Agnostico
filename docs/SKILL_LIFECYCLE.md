# Ciclo de vida das skills

## Objetivo

Transformar procedimentos repetiveis descobertos no desenvolvimento do benchmark em conhecimento operacional reutilizavel por agentes, sem transformar observacoes casuais em regras cientificas.

## Extracao por gate

Ao fechar um gate ou marco grande, executar a skill `gate-review` e revisar:

1. `docs/STATUS.md`, decisoes, testes, relatorios, incidentes e auditorias.
2. Comandos que funcionaram e falharam.
3. Erros recorrentes, correcoes e verificacoes que se repetem.
4. Riscos de leakage, viés, dependencia de candidato e dados selados.
5. Procedimentos que outro agente conseguiria repetir com entradas e saidas claras.

Uma observacao so vira proposta quando houver gatilho claro, entradas, passos, saida, validacao e limites.

## Promocao

1. Criar a skill em `.github/skills/<nome>/SKILL.md` usando `_template`.
2. Adicionar a entrada em `docs/SKILLS_CATALOG.md` com status `proposed` e evidencias.
3. Rodar `python scripts/skill_validator.py`.
4. Executar o exemplo ou teste associado.
5. Confirmar que a skill nao expoe candidato, conjunto sealed, segredo, hint ou ground truth.
6. Confirmar `CHANGE-ID` se o procedimento tocar construto, ambiente, reward, metrica, scoring, seed, budget ou protocolo.
7. Alterar status para `active` somente com todos os checks verdes.
8. Registrar a promocao em `docs/STATUS.md` ou `docs/DECISIONS.md`.

A promocao automatica valida formato e evidencias; ela nao concede aprovacao cientifica nem libera um gate.

## Depreciacao

Uma skill deve ser marcada `deprecated` quando seu procedimento ficar incorreto, duplicado ou incompatível com uma versao nova. O arquivo e preservado para historico e recebe a referencia da substituta.

## Sincronizacao

O repositorio e canonico. A exportacao para o perfil local do VS Code deve ser opt-in, gerar backup e registrar nome, versao e hash. Nunca sobrescrever customizacao local silenciosamente. Para IAs sem suporte a skills, gerar um pacote textual a partir das skills ativas, omitindo qualquer conteudo restrito.

## Guardrails

- Skills orientam comportamento; nao substituem testes, governanca ou controles de acesso.
- Nenhuma skill pode orientar entrada de arquitetura candidata antes da barreira B14/B15.
- Uma skill nao pode alterar resultados historicos nem contornar CHANGE-ID.
