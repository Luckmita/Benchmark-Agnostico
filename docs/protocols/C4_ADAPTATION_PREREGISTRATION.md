# C4 - Adaptacao a mudancas

Status: `CORRECTIVE DRAFT - PENDING SCIENTIFIC APPROVAL`  
CHANGE-ID: `CHG-2026-09-01-GATE-REALIGNMENT`

## Hipotese e tarefa

`H1`: apos mudanca nao anunciada de dinamica, recompensa, sensor ou acoes, o agente reduz regret e recupera desempenho mais rapido que uma politica persistente. A tarefa publica parametriza tipo, instante e magnitude; a combinacao final pertence a B13.

## Controles e metricas

Controles: politica persistente, reset oracle somente para limite analitico e baseline adaptativo pertinente. Metricas: detection latency, adaptation latency, post-change regret e recovery rate. Janelas pre/pos, seeds, budget e regra para quem nao recupera devem ser preregistrados.

## Validade

Testar flags, timing fixo, reset encoberto e observacoes que revelem diretamente a nova politica. O resultado e `TEST_INVALID` se persistir sem adaptar recebe o mesmo score ou se a mudanca e detectavel por metadado estranho ao construto.

## Proximo passo

Validar a familia publica em ao menos dois tipos de drift antes de selecionar o protocolo confirmatorio.
