# Plano de execucao

## Objetivo

Entregar um benchmark agnostico, reproduzivel e auditavel que produza um vetor de capacidades, e nao um ranking unico de inteligencia. As dimensoes iniciais sao aprendizagem, eficiencia amostral, generalizacao, adaptacao, dependencia temporal, planejamento, continual learning, robustez, transferencia multidominio, incerteza e eficiencia computacional.

## Fases e gates

| Gate | Resultado obrigatorio | Evidencia de saida |
| --- | --- | --- |
| B0 | Charter e governanca | escopo, papeis, conflito de interesse, CHANGE-ID |
| B1 | Definicoes cientificas | construto, hipotese, metricas, controles e preregistro por bateria |
| B2 | API universal | contrato black-box, ciclo de vida, capabilities opcionais e testes de contrato |
| B3 | Infraestrutura | runner, registry, artefatos, hashes, ambiente reproduzivel e CLI |
| B4 | Baselines | random, rule-based e baselines tecnicamente pertinentes com testes |
| B5 | Core tasks | aprendizagem e generalizacao |
| B6 | Temporal tasks | dependencia temporal e planejamento |
| B7 | Adaptacao | drift, continual learning e protocolos de mudanca |
| B8 | Robustez | perturbacoes, falhas, leakage e red team |
| B9 | Multidominio | adapters somente como conversores de protocolo |
| B10 | Eficiencia | CPU, GPU, memoria, tempo, energia quando mensuravel |
| B11 | Validacao do benchmark | sensibilidade, especificidade, discriminacao, confiabilidade, shortcuts e leakage |
| B12 | Auditoria adversarial | relatorio independente de ataques e correcoes |
| B13 | Conjunto selado | seeds, tarefas e perturbacoes fora do ambiente publico |
| B14 | Release candidate | freeze de codigo, metricas, pesos, budgets e hashes |
| B15 | Replicacao independente | terceiro reconstrui, roda baselines e reproduz conclusoes |
| B16 | Submissao | manifest, adapter auditado, execucao selada e relatorio automatico |

A ordem e linear ate B15. A primeira submissao so pode entrar depois da barreira de congelamento.

## Criterio de pronto por bateria

Cada bateria deve conter: construto operacional; hipotese preregistrada; tarefa publica e variante selada; controles positivo e negativo; seeds e budget; metricas primarias e secundarias; analise estatistica; teste de shortcut; teste de leakage; formato de artefatos; criterio TEST_INVALID.

## Entregaveis iniciais

1. Charter aprovado e matriz de responsabilidades.
2. Especificacao da API e manifest.
3. Esquema do registry experimental.
4. Runner deterministico com `run_id` e hashes.
5. Uma bateria vertical completa, preferencialmente C1, incluindo baseline e validacao.
6. Processo de release com sanitizer e freeze.

## Avanco B2

O contrato inicial foi implementado em `src/benchmark_core/protocol.py` com testes para agente minimo, persistencia opcional, rejeicao de implementacao incompleta e seed invalida. `AgentManifest` e `schemas/agent_manifest.schema.json` cobrem metadados, capabilities e timeout finito; `check_determinism` cobre entradas publicas repetidas. O runner B3 possui timeout real, isolamento por processo, episodios stateful, registry append-only, artefatos estruturados e CLI de hash; B2/B3 continuam abertos ate integrar limites semanticos definidos pelos ambientes e um fluxo de run completo.

## Skills evolutivas

O fechamento de cada gate deve executar `gate-review`. O agente revisa testes, decisoes, incidentes, auditorias e comandos; quando encontrar um procedimento repetivel, cria uma skill em `.github/skills/<nome>/SKILL.md`, valida com `scripts/skill_validator.py` e registra a evidencia em `docs/SKILLS_CATALOG.md`. Skills ativas podem ser exportadas para outras IAs, mas nao substituem governanca nem aprovacao cientifica.

## Ordem de implementacao recomendada

1. Especificar contratos e schemas antes de ambientes.
2. Implementar runner, logging e registry antes de muitas tarefas.
3. Provar uma bateria ponta a ponta.
4. Generalizar o framework para as demais baterias.
5. Validar o benchmark contra controles e ataques.
6. Selar, auditar e somente entao abrir submissao.

## Riscos que bloqueiam um gate

- Tarefa que pode ser resolvida sem a capacidade declarada.
- Metrica que premia um shortcut ou recompensa hackeada.
- Resultado sem raw data, config, seed, hardware ou hashes.
- Adapter que adiciona memoria, features, interpretacao ou ground truth.
- Alteracao apos observar candidato sem abrir nova versao major.
- Baseline ou auditoria que nao pode ser reproduzido por terceiro.
