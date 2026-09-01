# C1 - Aprovação final e freeze de parâmetros

Data: 2026-09-01
Status: `APPROVED - READY FOR SEALING`
CHANGE-ID: `CHG-2026-09-01-C1-FINAL-FREEZE`
Aprovador: responsável pelo projeto

## Revisão de validação

### Parâmetros congelados
- Seeds: [42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021]
- Max steps: 100
- Limiar: 70.0
- Teste estatístico: Mann-Whitney U (não-paramétrico, α=0.05)
- Algoritmos de aprendizagem: Random (baseline), EpsilonGreedy (ε=0.1)

### Resultados de validação (2026-09-01)
- Random mean: 50.9 ± 2.5
- EpsilonGreedy mean: 76.4 ± 2.1
- Win rate: 100% (10/10 seeds exceed threshold)
- Diferença média: 25.5 pontos
- Status: PASS em todos os 10 seeds

### Decisão
**Aprovado para congelamento e próxima fase**: C1 valida aprendizagem com discriminação clara. Nenhuma evidência de leakage. Parâmetros finalizados e prontos para benchmark final.

### Próximos passos
1. Congelar C1 como bateria "sealed" para uso em benchmark final
2. Aplicar ciclo idêntico a C2-C11 (validação → freezing)
3. Após congelamento de C2-C11, iniciar fase B14/B15 com candidatos

### Artefatos
- `docs/protocols/C1_LEARNING_FINAL_PARAMETERS.md` - parâmetros congelados
- `runs/C1_FINAL_2026-09-01/C1_evaluation_summary.json` - resultados publicados
