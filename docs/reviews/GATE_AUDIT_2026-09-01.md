# Auditoria corretiva dos gates B0-B16

Data: 2026-09-01  
Resultado: `BLOCKED`  
CHANGE-ID: `CHG-2026-09-01-GATE-REALIGNMENT`  
Escopo: evidencia presente no repositorio publico, sem arquiteturas candidatas

## Regra de avaliacao

Um gate recebe `PASS` somente quando cada criterio de saida possui evidencia reproduzivel. Codigo ou documento produzido fora da ordem linear pode ser reaproveitado como prototipo, mas nao fecha antecipadamente um gate. `READY`, `PROPOSED` e `VALIDATED` nao equivalem a `FROZEN`.

## Matriz de evidencia

| Gate | Criterio normativo | Evidencia encontrada | Resultado | Bloqueador/proximo teste |
| --- | --- | --- | --- | --- |
| B0 | governanca e regras aprovadas | charter, decisoes e revisao B0/B1 | PASS historico | completar papeis nominais, licenca e mecanismo externo sem reabrir a regra central |
| B1 | capacidades operacionalmente definidas | matriz e protocolos canonicos; aprovacao explicita de 2026-09-02 | PASS | parametros quantitativos permanecem sujeitos a preregistro antes dos runs confirmatorios |
| B2 | contrato universal neutro funcionando | contrato v0.1; manifest/schema; lifecycle; capabilities; testes | PASS | mudancas futuras no protocolo exigem CHANGE-ID |
| B3 | registry, rastreabilidade e reproducao | instalacao limpa; runner isolado; CLI; registry; raw/metrics/logs/manifests; hashes e tempos por `run_id` | IN REVIEW | auditar unicidade, imutabilidade e ambiente reproduzivel |
| B4 | controles implementados e validados | Random e EpsilonGreedy em bandit | BLOCKED | controles positivos/negativos pertinentes por construto |
| B5 | aprendizagem e generalizacao | C1 exploratoria; generalizacao nao demonstrada | BLOCKED | vertical C1 valida e C3 TRAIN/ID/OOD/transfer |
| B6 | dependencia temporal e planejamento | nenhum teste normativo | BLOCKED | tarefas que exijam retencao e consequencias atrasadas |
| B7 | drift e continual learning | mudanca de bandit exploratoria | BLOCKED | deteccao/adaptacao e sequencia A-B-C-D com reteste |
| B8 | perturbacoes e OOD | variantes de probabilidade exploratorias | BLOCKED | curva degradacao-intensidade, recovery e ataques |
| B9 | transferencia multidominio | nenhum conjunto multidominio | BLOCKED | mesmo agente congelado em familias distintas; adapters auditados |
| B10 | resource accounting | nenhum accounting comparavel | BLOCKED | CPU/GPU/RAM/VRAM/tempo e energia quando mensuravel |
| B11 | validade e discriminacao do benchmark | diferencas de medias exploratorias | BLOCKED | sensibilidade, especificidade, confiabilidade, shortcuts e leakage por bateria |
| B12 | red team concluido | nenhuma auditoria adversarial separada | BLOCKED | equipe/revisor separado e relatorio de ataques/correcoes |
| B13 | avaliacao final selada | nenhum repositorio/storage restrito | BLOCKED | custodia, geracao, acesso, hashes e isolamento fisico |
| B14 | release candidate congelada | claims historicos sem pre-requisitos | BLOCKED | concluir B1-B13; congelar codigo, metricas, budgets, pesos e hashes |
| B15 | terceiro reproduz conclusoes | nenhuma replicacao independente | BLOCKED | terceiro reconstrui, roda baselines e assina relatorio |
| B16 | primeira submissao | inexistente, como exigido | PROHIBITED | somente abrir depois de B14 e B15 em PASS |

## Achados que invalidam os freezes historicos como gate

1. O batch C3-C11 executou somente C3, C4, C5, C6 e C10; C7-C9 e C11 permaneceram `READY`.
2. Os IDs e nomes de C3-C11 nao correspondem ao plano diretor.
3. O script marcou `PASS` na ausencia de excecao, sem aplicar limiar cientifico ou o Mann-Whitney U declarado.
4. C4 usou apenas sete seeds chamadas de treino; nao houve avaliacao ID-heldout, OOD ou structural transfer.
5. C10 mediu retorno em quatro acoes, nao calibracao de incerteza; a eficiencia computacional normativa e C11.
6. Os JSONs agregados nao incluem `run_id`, hashes, hardware/software, raw por seed, logs ou manifests.
7. Nao ha evidencia de auditoria independente, conjunto selado separado ou replicacao por terceiro.

## Evidencia corretiva adicionada em 2026-09-02

- `configs/public/capacity_taxonomy.json` e `tests/test_capacity_taxonomy.py` impedem nova troca silenciosa de IDs.
- `scripts/check_governance.py` verifica status B1, barreira B16, protocolos canonicos e marcacao do historico superado.
- `src/benchmark_core/tasks/c_batteries.py` contem apenas prototipos publicos coerentes com C2-C9; C10 esta em `metrics.py` e C11 em `resources.py`.
- Scripts historicos de freeze e validacao generica retornam erro e nao sobrescrevem resultados.
- `python -m benchmark_core.cli run-public-c1` produziu, em ambiente virtual limpo, registry com `run_id`, hash do codigo/config, timestamps, hardware/software e os cinco grupos de artefatos.
- Suite em ambiente virtual limpo: `45 passed, 3 skipped`; skips limitados a symlinks indisponiveis no Windows usado.

## Decisao

B1 foi reaberto pela correcao e posteriormente aprovado pelo responsavel do projeto em 2026-09-02. B2 e o gate atual; todos os gates B2-B16 permanecem sem aprovacao vigente. Os resultados existentes sao preservados como experimentos exploratorios publicos. Nenhuma submissao candidata foi observada.

## Skills

`gate-review` foi aplicada. Nenhuma nova skill e promovida: o procedimento corretivo ainda nao demonstrou repetibilidade suficiente e nao deve virar automacao antes de concluir esta rodada.
