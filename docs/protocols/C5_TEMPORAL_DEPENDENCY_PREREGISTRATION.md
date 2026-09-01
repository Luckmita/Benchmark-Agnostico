# C5 - Dependencia temporal

Status: `CORRECTIVE DRAFT - PENDING SCIENTIFIC APPROVAL`  
CHANGE-ID: `CHG-2026-09-01-GATE-REALIGNMENT`

## Hipotese e tarefa

`H1`: o agente usa uma pista observada antes da decisao e ausente no momento da resposta, mantendo precisao acima do controle sem pista sob atrasos e interferencia. A tarefa publica delayed-cue cobre delays 1, 5, 20, 50, 100 e 500 quando o budget permitir.

## Controles e metricas

Controles: sem pista, pista presente na decisao e agente memoryless. Metricas: precisao/retencao por delay, curva de degradacao e resistencia a distractors. Seeds, numero de trials, balanceamento de pistas e tratamento de timeout devem ser preregistrados.

## Validade

Testar codificacao da pista em seed, ordem, timing, estado do ambiente e reward. O resultado e `TEST_INVALID` se o controle sem pista supera chance sistematicamente ou se a resposta correta permanece observavel.

## Proximo passo

Implementar o ambiente publico e provar chance no controle sem pista antes de expandir delays.
