# C6 - Planejamento

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - QUANTITATIVE PREREGISTRATION REQUIRED`

CHANGE-ID: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

## Hipotese e tarefa

`H1`: o agente escolhe acoes por retorno futuro e supera um controle miope quando recompensa imediata e retorno atrasado conflitam. A familia publica varia horizonte e permite mudanca causal para testar replanejamento.

## Controles e metricas

Controles: politica miope, oracle analitico e baseline de planejamento tecnicamente pertinente. Metricas: retorno, regret, horizonte efetivo e desempenho apos mudanca causal. Grafos, horizontes, budget, seeds e regra de parada devem ser preregistrados.

## Validade

Testar pistas de rota, recompensa intermediaria informativa, politica fixa e correlacao entre acao imediata e alvo final. O resultado e `TEST_INVALID` se a melhor decisao puder ser escolhida maximizando apenas recompensa imediata.

## Proximo passo

Implementar um caso minimo de escolha atrasada e um controle miope antes de aumentar a familia de grafos.
