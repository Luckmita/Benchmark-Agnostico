# C11 - Eficiencia computacional

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - QUANTITATIVE PREREGISTRATION REQUIRED`

CHANGE-ID: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

## Hipotese e tarefa

`H1`: custos de treino e inferencia sao reproduziveis sob workload e hardware controlados, permitindo separar desempenho bruto de desempenho por recurso. C11 mede custo; expandir o numero de acoes sem medir recursos nao valida o construto.

## Controles e metricas

Controles: medicao vazia, warmup, baseline no mesmo processo e hardware fixo. Metricas: CPU/GPU time, wall time, RAM/VRAM peak, latencia, throughput, parametros, interacoes e energia quando mensuravel. Repeticoes, afinidade, concorrencia, warmup e limites devem ser preregistrados.

## Validade

Testar cache, setup/I/O omitido, processos filhos nao contabilizados, thermal throttling e instrumentacao dominante. O resultado e `TEST_INVALID` quando variancia instrumental ou hardware nao identificado impede comparacao.

## Proximo passo

Implementar resource accounting local com limitacoes explicitas e preparar protocolo de hardware comparavel para B10.
