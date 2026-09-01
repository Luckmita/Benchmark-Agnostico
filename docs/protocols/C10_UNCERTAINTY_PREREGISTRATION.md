# C10 - Incerteza

Status: `CORRECTIVE DRAFT - PENDING SCIENTIFIC APPROVAL`  
CHANGE-ID: `CHG-2026-09-01-GATE-REALIGNMENT`

## Hipotese e tarefa

`H1`: quando o agente declara confianca probabilistica, sua confianca acompanha a frequencia de acerto e permite abstencao util. Agentes sem confianca explicita recebem `NOT_SUPPORTED`, nao `FAIL`.

## Controles e metricas

Controles: confianca constante, predictor nao calibrado e oracle analitico. Metricas: Brier score, ECE com bins preregistrados, calibration curve, selective accuracy e cobertura-risco. Splits, bins, shifts, seeds e tratamento de classes vazias devem ser fixados antes dos resultados.

## Validade

Testar label/ground-truth leakage, confidence fora de [0,1], bins escolhidos pos hoc e exclusao seletiva. O resultado e `TEST_INVALID` se a dificuldade nao variar ou se a confianca puder ser inferida de metadados ocultos.

## Proximo passo

Adicionar contrato opcional de predicao/confianca e validadores de Brier/ECE sem obrigar mecanismo interno.
