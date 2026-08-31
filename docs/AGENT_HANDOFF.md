# Manual para agentes

## Missao

Continuar o benchmark sem violar neutralidade arquitetural, reproducibilidade ou separacao de dados. O agente deve deixar o workspace em estado verificavel, com documentos e testes que permitam retomada.

## Ordem de leitura

1. `README.md`.
2. `PLANO_DIRETOR_MESTRE_BENCHMARK_IA_ML.pdf`.
3. `docs/EXECUTION_PLAN.md`.
4. `docs/TECHNICAL_DESIGN.md`.
5. `docs/GIT_POLICY.md`.
6. `docs/DECISIONS.md`.
7. Codigo e testes do gate atual.
8. `docs/SKILLS_CATALOG.md` e `docs/SKILL_LIFECYCLE.md`.
9. `docs/CHARTER_B0.md` e `docs/CONSTRUCT_MATRIX_B1.md`.

## Protocolo operacional

1. Verificar `git status` e nao apagar mudancas existentes.
2. Identificar o gate atual e seu criterio de saida.
3. Formular uma hipotese local e um teste barato que possa refuta-la.
4. Fazer a menor alteracao testavel.
5. Rodar primeiro o teste do slice alterado.
6. Atualizar docs, schemas e CHANGE-ID quando a mudanca for cientifica.
7. Registrar resultado, limitações e proximo passo.
8. Ao fechar gate ou marco grande, executar `gate-review` e avaliar se surgiu um procedimento reutilizavel como skill.

## Nao fazer

- Nao abrir arquitetura candidata antes de B14/B15.
- Nao criar tarefa por causa de um modelo especifico.
- Nao adicionar inteligencia a adapter.
- Nao expor seeds, tarefas, perturbacoes ou parametros selados.
- Nao publicar somente media.
- Nao trocar score vetorial por um score unico sem decisao cientifica.
- Nao corrigir teste invalido culpando o agente.
- Nao fazer commit ou push sem pedido explicito do responsavel.
- Nao promover skill sem validacao automatica, evidencia e entrada no catalogo.
- Nao tratar skill como aprovacao cientifica ou como mecanismo de controle de acesso.

## Contrato de handoff

Ao parar, atualizar `docs/DECISIONS.md` ou criar um registro em `docs/STATUS.md` contendo: data, agente, gate, objetivo, arquivos tocados, comandos executados, resultado, riscos, decisoes pendentes e proximo passo executavel.

Se uma skill for criada ou alterada, registrar tambem gatilho, gate de origem, evidencia, hash/versao, resultado do validador e status no catalogo.

## Primeiro trabalho recomendado

Revisar e aprovar o charter B0; depois completar a matriz B1 com construtos, hipoteses, controles, metricas, budgets, seeds e criterios de invalidacao. Depois implementar uma vertical C1 completa antes de expandir o framework.
