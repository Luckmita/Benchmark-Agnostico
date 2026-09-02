# C8 - Robustez

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - QUANTITATIVE PREREGISTRATION REQUIRED`

CHANGE-ID: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

## Hipotese e tarefa

`H1`: o desempenho apresenta degradacao controlada e recuperavel conforme aumenta a intensidade de ruido, missing observations, bias, delay, outliers, falha de acao ou distribution shift. Perturbacoes sao wrappers independentes da logica do agente.

## Controles e metricas

Controles: intensidade zero, controle de falha e baseline robusto pertinente. Metricas: curva degradacao-intensidade, area robusta, worst-case e recovery. Tipos, grade de intensidade, combinacoes, seeds e budget devem ser preregistrados.

## Validade

Testar perturbacao que sinaliza a resposta, altera ground truth, muda budget ou favorece politica fixa. O resultado e `TEST_INVALID` se o wrapper muda o construto em vez da observacao/acao declarada.

## Proximo passo

Validar um wrapper de observacao e um de falha de acao em tarefa publica ja aprovada.
