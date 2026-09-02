# Decisoes e pendencias

## Decisoes adotadas provisoriamente

| ID | Decisao | Motivo | Estado |
| --- | --- | --- | --- |
| D-001 | Python >=3.12,<3.15; ambiente B3 de referencia fixado em 3.14.7 | preserva compatibilidade inicial e registra a versao realmente reproduzida | adotada em 2026-09-02 |
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
| D-014 | Aprovar B1 corrigido como definicao de construtos e estrutura de protocolos C1-C11 | a aprovacao explicita do responsavel aceita a taxonomia, hipoteses, controles, metricas e criterios de invalidacao; parametros quantitativos continuam sujeitos a preregistro | adotada em 2026-09-02 |
| D-015 | Versionar o contrato universal v0.1 com capabilities estritas e `AgentDecision` para incerteza | elimina divergencia entre manifest/runtime e torna a capability C10 observavel sem exigir mecanismo interno | adotada em 2026-09-02 |
| D-016 | Tornar `run_id` portavel e unico, raw imutavel e ambiente B3 versionado | fecha riscos de sobrescrita, corrida simples, JSON nao finito e ambiente ambiguo | adotada em 2026-09-02 |

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

### CHG-2026-09-02-B1-CORRECTIVE-APPROVAL

- Motivacao: aprovacao explicita do responsavel do projeto para o B1 corrigido.
- Impacto cientifico: a matriz e os protocolos canonicos C1-C11 passam de draft a estrutura metodologica aprovada; B2 torna-se o gate atual.
- Escopo: construtos, hipoteses, familias de tarefas, controles, metricas, riscos de shortcut/leakage e criterios `TEST_INVALID`.
- Fora do escopo: nao congela seeds, budgets, limiares, splits, bins, pesos, tarefas finais ou variantes seladas; esses itens exigem preregistro antes de experimento confirmatorio e freeze.
- Testes afetados: governance check, taxonomia e revisao documental B1.
- Compatibilidade: preserva os prototipos publicos e o historico superado; nao cria sealed nem altera resultados anteriores.
- Risco de vies: controlado pela aprovacao anterior a candidatos e pela proibicao de usar resultados exploratorios para escolher parametros confirmatorios.
- Resultado esperado: iniciar revisao formal de B2 sem liberar B3-B16.
- Evidencia: `docs/reviews/B1_CORRECTIVE_APPROVAL_2026-09-02.md`.

### CHG-2026-09-02-B2-UNIVERSAL-API

- Motivacao: a revisao B2 encontrou capabilities sem validacao de tipo, divergencia possivel entre manifest/specification, persistencia nao serializavel e ausencia de formato observavel para incerteza.
- Impacto cientifico: define como acao e confianca chegam ao ambiente e a C10; nao altera reward, tarefa, seed, budget ou scoring.
- Testes afetados: protocolo, manifest, runner, episodios, avaliacao, CLI e schema.
- Compatibilidade: agentes sem incerteza continuam retornando acao bruta; manifests ganham defaults publicos validos. Agentes que declaram incerteza devem retornar `AgentDecision`.
- Risco de vies: baixo; o envelope e arquiteturalmente neutro e aceita qualquer mecanismo interno.
- Resultado esperado: contrato black-box rejeita declaracoes inconsistentes antes do run e preserva confianca no raw.
- Evidencia: `docs/contracts/UNIVERSAL_AGENT_API_V0.1.md` e `docs/reviews/B2_GATE_REVIEW_2026-09-02.md`.

### CHG-2026-09-02-B3-REPRODUCIBLE-RUNS

- Motivacao: a revisao B3 encontrou duplicacao possivel de `run_id`, writes nao atomicos, raw sobrescrevivel, JSON nao finito e perda de trajetoria parcial.
- Impacto cientifico: melhora rastreabilidade e preservacao de evidencia; nao altera tarefas, rewards, seeds, budgets, metricas ou scoring.
- Testes afetados: artifacts, registry, episode, run, CLI e instalacao limpa.
- Compatibilidade: IDs portaveis continuam aceitos; IDs com caracteres dependentes de sistema passam a ser rejeitados. Raw nao aceita overwrite.
- Risco de vies: nenhum esperado; a mudanca impede reescrita ou perda seletiva de evidencia.
- Resultado esperado: cada `run_id` e reivindicado uma vez, cada arquivo novo usa criacao exclusiva e erros preservam passos concluidos.
- Evidencia: `docs/ENVIRONMENT_B3.md` e futura revisao de gate B3.
