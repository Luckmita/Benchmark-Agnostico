# C7 - Continual learning

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - QUANTITATIVE PREREGISTRATION REQUIRED`

CHANGE-ID: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

## Hipotese e tarefa

`H1`: apos aprender A-B-C-D, o agente preserva competencias anteriores e demonstra transferencia mensuravel sem esconder perda por media agregada. O protocolo retesta cada tarefa apos cada fase relevante.

## Controles e metricas

Controles: treino isolado, ordem alternativa, from-scratch e politica sem atualizacao. Metricas: forgetting, backward transfer, forward transfer, plasticidade e retencao por tarefa. Budget deve ser igual por tarefa; ordem, seeds, retestes e uso permitido de replay devem ser preregistrados.

## Validade

Testar IDs de tarefa que permitam bancos independentes nao declarados, vazamento entre retestes e score que omita tarefas esquecidas. O resultado e `TEST_INVALID` se aprender a tarefa atual puder compensar integralmente destruicao das anteriores.

## Proximo passo

Definir familias A-D publicas com dificuldade equivalente e validar controles de ordem.
