# Decisoes e pendencias

## Decisoes adotadas provisoriamente

| ID | Decisao | Motivo | Estado |
| --- | --- | --- | --- |
| D-001 | Python 3.12 para a infraestrutura inicial | ecossistema cientifico e facilidade de reproducao | provisoria |
| D-002 | Resultado primario e vetor por capacidade | evita esconder fraquezas em score unico | alinhada ao plano |
| D-003 | Separacao fisica entre core, submissions e sealed | reduz leakage e conflito de interesse | obrigatoria |
| D-004 | Registry proprio com raw imutavel e hashes | rastreabilidade sem depender de servico externo | provisoria |
| D-005 | Primeira vertical ponta a ponta em C1 | reduz risco antes da expansao | proposta |
| D-006 | Skills versionadas em `.github/skills`, com `AGENTS.md` como contrato permanente | permite continuidade entre agentes e IAs | adotada |
| D-007 | Promocao automatica condicionada a validador, evidencia, catalogo e CHANGE-ID quando aplicavel | reduz conhecimento informal sem liberar mudanca cientifica | adotada |
| D-008 | Exportacao para perfil local e IAs externas e derivada e opt-in | preserva uma fonte canonica e evita sobrescrita local | adotada |
| D-009 | Aprovar B0 e B1 como charter de governanca e estrutura metodologica inicial | habilita a implementacao controlada de B2 sem liberar submissions | adotada em 2026-08-31 |
| D-010 | C1 sera a primeira bateria vertical e sera preregistrada antes da implementacao da tarefa | reduz risco cientifico antes da expansao do benchmark | proposta em 2026-09-01 |
| D-011 | Aprovar a proposta C1 para implementacao controlada, mantendo parametros pendentes fora do freeze | permite construir a primeira vertical sem fingir que o protocolo final esta congelado | adotada em 2026-09-01 |
| D-012 | Reabrir B1 e classificar os freezes de 2026-09-01 como historicos, sem efeito de liberacao | a evidencia nao satisfaz a ordem B1-B15, a taxonomia normativa ou os criterios de validade | adotada em 2026-09-01 |
| D-013 | Reservar B14 para release candidate, B15 para replicacao independente e B16 para submissao | restaura a semantica normativa dos gates e impede entrada prematura de candidatos | adotada em 2026-09-01 |

## Pendencias que bloqueiam freeze

| ID | Questao | Responsavel sugerido | Gate |
| --- | --- | --- | --- |
| P-001 | Quais tarefas concretas representam cada capacidade? | conselho cientifico | B1 |
| P-002 | Qual universo de ambientes e dominios entra na v1? | conselho + engenharia | B1/B9 |
| P-003 | Quais budgets, seeds e criterios de parada? | metodologia | B1 |
| P-004 | Como medir energia de modo comparavel? | engenharia | B10 |
| P-005 | Qual infraestrutura de storage e acesso do sealed? | seguranca/ops | B3/B13 |
| P-006 | Qual esquema final de manifest e contrato de capability? | API | B2 |
| P-007 | Qual mecanismo de preregistro e auditoria externa? | governanca | B0/B11 |
| P-008 | Qual politica de licenca e contribuicao? | responsavel do repositorio | B0 |

## Registro de mudanca

Toda alteracao relevante deve adicionar uma entrada com `CHANGE-ID`, motivacao, impacto cientifico, testes afetados, compatibilidade, risco de viés e resultado esperado. Nao editar silenciosamente uma decisao congelada.

### CHG-2026-08-31-B0-B1-APPROVAL

- Motivacao: aprovacao explicita do responsavel para fechar B0 e B1.
- Impacto: charter e matriz inicial passam a ser base aprovada para B2.
- Testes afetados: revisao de fechamento e validacao documental.
- Compatibilidade: nenhuma submissao ou conjunto selado foi alterado.
- Risco de vies: protocolos, seeds, budgets e limiares continuam pendentes de definicao.
- Resultado esperado: implementacao tecnica prossegue sob o escopo aprovado.

### CHG-2026-09-01-GATE-REALIGNMENT

- Motivacao: auditoria de transicao encontrou conflito entre o plano diretor, o status ativo, a taxonomia C1-C11 e os documentos de freeze.
- Impacto cientifico: B1 e reaberto; os resultados C1-C11 existentes passam a ser evidencia exploratoria publica, sem validade de conjunto selado ou release candidate.
- Testes afetados: contratos de taxonomia, protocolos, baterias publicas, rastreabilidade de runs e auditoria documental de gates.
- Compatibilidade: artefatos e documentos historicos sao preservados; seus claims de gate deixam de ser vigentes. Nenhum resultado de candidato existe ou e alterado.
- Risco de vies: baixo e redutor; a mudanca ocorre antes de qualquer submissao e remove claims nao sustentados.
- Resultado esperado: IDs C1-C11 voltam a representar os construtos normativos e cada gate passa a depender de evidencia reproduzivel.
- Evidencia: `docs/CORRECTIVE_REVIEW_PLAN.md` e `docs/reviews/GATE_AUDIT_2026-09-01.md`.
