# HISTORICO SUPERADO - C4 - Generalização

> Este prototipo usou uma taxonomia incorreta. C4 canonico e Adaptacao a mudancas. Consulte `C4_ADAPTATION_PREREGISTRATION.md`. Preservado somente para rastreabilidade pelo `CHG-2026-09-01-GATE-REALIGNMENT`.

Status: `PROPOSED - PENDING SCIENTIFIC REVIEW`

CHANGE-ID: `CHG-2026-09-01-C4-PROTOCOL-PROPOSAL`

Pergunta: O agente aprende uma política que generaliza para instâncias não vistas durante treinamento?

Construto: Generalização mede desempenho em held-out test set com distribuição idêntica mas seeds diferentes.

Metrica: Retorno e AUC no test set; comparação com train-only.

Tarefas candidatas: C1BanditEnvironment com seeds reservadas para teste.

Proximo passo: Aprovar ou rejeitar após definir split train/test.
