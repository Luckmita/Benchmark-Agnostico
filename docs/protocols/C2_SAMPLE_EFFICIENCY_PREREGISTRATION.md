# C2 - Eficiência amostral

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - QUANTITATIVE PREREGISTRATION REQUIRED`

CHANGE-ID vigente: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

## Pergunta

O agente aprende utilmente com quantidade limitada de interações, atingindo limiar de desempenho em tempo razoável comparado a baseline aleatório?

## Construto operacional

Eficiência amostral mede a quantidade de interações necessárias para atingir um alvo de desempenho pré-definido. Compara o número de passos do agente com aprendizagem habilitada contra o controle aleatório, mantendo a mesma estrutura de tarefa que C1.

## Hipótese

`H1`: o agente com aprendizagem habilitada atinge o limiar de desempenho com significativamente menos interações que o baseline aleatório.

`H0`: a quantidade de interações não demonstra economia mensurável ou o agente não atinge o limiar.

## Tarefa

Reutiliza `C1BanditEnvironment` do protocolo aprovado de C1. O limiar será definido como a mediana de desempenho final do controle aleatório, arredondada para o quartil superior.

Metrica primária: `steps_to_threshold` do modulo `benchmark_core.metrics`.

## Controles

- Random: baseline negativo sem aprendizagem.
- EpsilonGreedy com epsilon fixo: baseline positivo com aprendizagem.

## Protocolo proposto

Idêntico ao C1, mas a análise foca no passo em que cada agente ultrapassa o limiar, não na curva completa.

## Metricas

- Passos até atingir o limiar por seed.
- Mediana, IC95 e distribuição completa.
- Win rate: proporção de seeds em que o agente aprende supera o aleatório.

## Seeds e budget

`PENDENTE - identicos ao C1 final`.

## Proximo passo

Aprovar ou rejeitar a proposta C2 após validar que C1 foi congelada com valores finais. C2 reutiliza a mesma tarefa, então ambas podem ser executadas em um único batch.
