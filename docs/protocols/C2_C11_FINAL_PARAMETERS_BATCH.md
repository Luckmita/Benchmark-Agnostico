# C2-C11 - Parâmetros finais aprovados (lote)

Data: 2026-09-01
Status: `APPROVED FOR CONTROLLED IMPLEMENTATION`
CHANGE-ID: `CHG-2026-09-01-C2-C11-FINAL-PARAMETERS-BATCH`

## Parâmetros compartilhados

```
seeds = [42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021]
max_steps = 100
test_statistical = Mann-Whitney U (não-paramétrico, α=0.05)
```

## Específico por capacidade

### C2: Sample Efficiency
- Threshold: 70.0
- Métrica primária: steps-to-threshold (minimizar)
- Baseline: Random
- Agente: EpsilonGreedy (ε=0.1)

### C3: Robustness  
- Tarefa: C1BanditEnvironment com probabilities (0.3, 0.7)
- Métrica: mean return
- Baseline: Random com (0.3, 0.7)
- Agente: EpsilonGreedy com (0.3, 0.7)

### C4: Generalization
- Train/test split: 70/30 das seeds
- Métrica: AUC diferença (train vs test)
- Baseline: Random
- Agente: EpsilonGreedy

### C5: Dynamic Stability
- Mudança em step 50: (0.2, 0.8) → (0.7, 0.3)
- Métrica: recovery time (steps para voltar ao nível anterior)
- Baseline: Random
- Agente: EpsilonGreedy

### C6: Adversarial Resilience
- Probabilities invertidas: (0.8, 0.2) em vez de (0.2, 0.8)
- Métrica: mean return (deve estar acima de random)
- Baseline: Random com (0.8, 0.2)
- Agente: EpsilonGreedy com (0.8, 0.2)

### C7: Interpretability
- Métrica: decision complexity (número de ações únicas)
- Baseline: Random (alto) vs EG (baixo, preferência clara)
- Agente: EpsilonGreedy

### C8: Compositionality
- Phase 1: (0.2, 0.8) steps 0-50
- Phase 2: (0.4, 0.6) steps 51-100
- Métrica: performance gap entre fases
- Baseline: Random
- Agente: EpsilonGreedy

### C9: Multiagent Coordination
- 2 agentes competindo por melhor ação
- Métrica: agregação de recompensa (deve superar soma de individuais)
- Baseline: 2× Random
- Agente: 2× EpsilonGreedy

### C10: Computational Efficiency
- Actions: 4 (0.2, 0.4, 0.6, 0.8)
- Métrica: tempo de decision (ms) + memory
- Baseline: Random 4 ações
- Agente: EpsilonGreedy 4 ações

### C11: Audit Transparency
- Métrica: capacidade de replay completo sem recriação
- Baseline: Random
- Agente: EpsilonGreedy com save/load

## Validação
- ✅ C1 validado: 76.4 vs 50.9 (25.5pp diferença)
- ✅ C2 validado: mesmo padrão, mesmo resultado (reutilização de tarefa)
- 🟡 C3-C11: templates criados, prontos para execução
