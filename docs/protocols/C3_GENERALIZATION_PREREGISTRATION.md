# C3 - Generalizacao

Status: `CORRECTIVE DRAFT - PENDING SCIENTIFIC APPROVAL`  
CHANGE-ID: `CHG-2026-09-01-GATE-REALIGNMENT`

## Hipotese e tarefa

`H1`: um agente treinado somente em TRAIN preserva desempenho mensuravel em ID-HELDOUT, OOD e STRUCTURAL-TRANSFER, com gaps preregistrados. A familia publica deve permitir separar parametros, representacoes e estrutura; as combinacoes finais pertencem a B13.

## Controles e metricas

Controles: politica fixa, from-scratch, TRAIN e ID-HELDOUT. Metricas primarias: generalization gap e zero-shot transfer; secundarias: few-shot adaptation e recovery. Splits, seeds, budget, criterio de censura e teste estatistico devem ser aprovados antes do experimento confirmatorio.

## Validade

Testar memorizar seed/ID/ordem, pistas na representacao e acesso indevido ao split. O resultado e `TEST_INVALID` se uma politica que memoriza TRAIN resolve os niveis ocultos ou se TRAIN/ID/OOD nao diferem pela propriedade preregistrada.

## Proximo passo

Implementar apenas a familia publica e controles; submeter o protocolo completo a revisao cientifica antes de qualquer variante selada.
