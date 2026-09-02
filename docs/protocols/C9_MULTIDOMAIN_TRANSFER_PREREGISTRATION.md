# C9 - Transferencia multidominio

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - QUANTITATIVE PREREGISTRATION REQUIRED`

CHANGE-ID: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

## Hipotese e tarefa

`H1`: o mesmo core congelado transfere entre familias estruturalmente distintas melhor que from-scratch sob budget igual. Dominios-alvo incluem discreto, dinamica continua, recursos e observabilidade parcial; apenas adapters de protocolo podem mudar.

## Controles e metricas

Controles: from-scratch por dominio, core congelado e adapter identidade quando aplicavel. Metricas: zero-shot, few-shot, desempenho final, velocidade de adaptacao e transferencia negativa. Ordem, dominios, budgets, seeds e estado permitido entre dominios devem ser preregistrados.

## Validade

Auditar adapters para feature extraction, memoria, selecao semantica, hints e ground truth. O resultado e `TEST_INVALID` se remover o adapter inteligente altera a capacidade ou se o core muda entre dominios.

## Proximo passo

Especificar dois dominios publicos minimos e criar testes negativos de adapter antes da expansao.
