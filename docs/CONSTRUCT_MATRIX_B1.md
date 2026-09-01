# Matriz de construtos B1

Status: `REOPENED - CORRECTIVE DRAFT PENDING SCIENTIFIC APPROVAL - 2026-09-01`

Registro historico: `docs/reviews/B0_B1_GATE_REVIEW_2026-08-31.md`

Revisao vigente: `docs/reviews/GATE_AUDIT_2026-09-01.md`

CHANGE-ID: `CHG-2026-09-01-GATE-REALIGNMENT`

Esta matriz impede que uma bateria seja implementada antes de definir o que ela mede. Campos como tarefa, seed, budget e limiar permanecem pendentes ate preregistro e aprovacao cientifica.

## Contrato de preenchimento

Cada linha precisa responder: qual capacidade observavel e medida, qual hipotese sera testada, quais controles distinguem a capacidade de um shortcut, quais dados serao publicados, como a incerteza sera calculada e em que condicao o teste e `TEST_INVALID`.

| ID | Construto operacional | Hipotese preregistrada | Tarefa publica | Variante selada | Controles | Metricas primarias | Metricas secundarias | Seeds/budget | Shortcut/leakage | Criterio TEST_INVALID | Responsavel/status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | adquirir politica util por experiencia | melhora preregistrada da curva supera controle sem aprendizagem | bandit/contextual family publica | instancia isomorfa gerada e custodiada em B13 | random; fixed policy; baseline de aprendizagem | retorno; AUC; passos ate limiar | estabilidade entre seeds; falhas | lote publico separado do lote final; budget preregistrado | seed/ordem/reward leakage; politica fixa | controle positivo nao aprende ou controle negativo aparenta aprender | DRAFT; protocolo C1 requer nova aprovacao |
| C2 | aprender com menos interacoes ambientais | atinge alvo preregistrado com menos interacoes sob mesmo desempenho final | mesma familia valida de C1 com checkpoints | instancias C1 seladas e checkpoints fixos | random; baseline learning-curve matched | interacoes ate limiar; retorno/interacao | custo por ganho; censura | checkpoints e budget definidos antes do run | limiar derivado do proprio resultado; reuso indevido de treino | alvo inalcançavel ou metrica confunde desempenho final | DRAFT; protocolo C2 em revisao |
| C3 | generalizar para instancias e estruturas nao vistas | desempenho decai de forma mensuravel entre TRAIN, ID, OOD e transferencia | familia com parametros/representacoes particionados | combinacoes OOD/estruturais custodiadas em B13 | train; ID-heldout; OOD; fixed policy | gap; zero-shot; few-shot | recuperacao; variancia | splits, seeds e budget separados por nivel | IDs, ordem ou representacao revelam split | teste pode ser resolvido por memorizar TRAIN | DRAFT; protocolo canonico C3 |
| C4 | adaptar-se a mudanca nao anunciada | detecta e recupera apos drift melhor que politica persistente | ambiente publico com drift parametrizavel | tipo, momento e magnitude do drift selados | politica persistente; reset oracle apenas analitico | latencia de adaptacao; regret pos-mudanca | deteccao; recovery rate | pre/post windows e budget preregistrados | flag/timing revela mudanca; reset encoberto | controle persistente recebe a mesma pontuacao sem adaptar | DRAFT; protocolo canonico C4 |
| C5 | usar informacao passada quando nao esta observavel | precisao depende da pista anterior e degrada com atraso/interferencia | delayed-cue publica com delays e distractors | combinacoes de pista/delay/interferencia seladas | sem pista; pista presente; memoryless | retencao; precisao por delay | interferencia; falso recall | delays publicos de desenvolvimento; grade final selada | observacao/seed/ordem codifica a pista | agente sem acesso a pista supera chance de modo sistematico | DRAFT; protocolo canonico C5 |
| C6 | escolher acao por consequencias atrasadas | supera controle miope conforme horizonte cresce | escolha imediata versus retorno atrasado | grafos/horizontes/alteracoes causais selados | myopic; oracle analitico; planejador pertinente | retorno; regret; horizonte efetivo | replanejamento | horizontes e budget preregistrados | recompensa intermediaria revela rota; politica fixa | melhor acao pode ser escolhida pelo ganho imediato | DRAFT; protocolo canonico C6 |
| C7 | aprender sequencias sem destruir competencias | preserva A-D e demonstra transferencias mensuraveis | sequencia publica A-B-C-D com retestes | familias, ordem e variantes finais seladas | treino isolado; ordem alternativa; sem replay | forgetting; backward/forward transfer | plasticidade; retencao | budget igual por tarefa e reteste | IDs permitem banco por tarefa sem regra declarada | score de novas tarefas esconde destruicao das antigas | DRAFT; protocolo canonico C7 |
| C8 | manter degradacao mensuravel sob perturbacao | curva de desempenho degrada controladamente com intensidade | wrapper publico de ruido, missing, delay e falha | tipos/combinacoes/intensidades finais selados | intensidade zero; controle de falha | curva degradacao-intensidade | recuperabilidade; area robusta | grade de intensidade e repeticoes preregistradas | perturbação sinaliza resposta; wrapper altera ground truth | controle trivial permanece perfeito sob todas intensidades | DRAFT; protocolo canonico C8 |
| C9 | transferir para familias de problemas distintas | mesmo core congelado transfere entre dominios melhor que from-scratch | familias discretas, continuas, recursos e POMDP | instancias e combinacoes finais por dominio seladas | from-scratch; agente congelado; adapter identity | zero-shot; few-shot; desempenho final | velocidade; transferencia negativa | budget igual por dominio e adapter auditado | adapter extrai features, adiciona estado ou seleciona informacao | resultado depende de inteligencia no adapter | DRAFT; protocolo canonico C9 |
| C10 | produzir incerteza calibrada quando suportada | probabilidades declaradas acompanham frequencias observadas | predicao publica com dificuldade controlada | shifts e bins finais selados | predictor constante; nao calibrado; oracle analitico | Brier; ECE; selective accuracy | curva; cobertura-risco | bins e exclusoes preregistrados | confidence derivada de label/ground truth | confianca nao altera com dificuldade ou label vaza | DRAFT; `NOT_SUPPORTED` sem confianca explicita |
| C11 | entregar capacidade por custo computacional | custo e escalabilidade sao reproduziveis sob carga controlada | workloads publicos das baterias aprovadas | cargas finais vinculadas ao sealed | hardware fixo; warmup; medicao vazia | CPU/GPU time; RAM/VRAM; latencia | energia; parametros; interacoes | repeticoes, warmup e limites por hardware | cache, I/O ou setup excluido seletivamente | variancia instrumental impede comparacao | DRAFT; protocolo canonico C11 |

## Regras de revisao

- Campos vagos, nao aprovados ou sem responsavel nao sao criterio de aprovacao; sao bloqueios de B1.
- Nenhuma linha pode definir uma arquitetura interna necessaria.
- Controles devem testar sensibilidade e especificidade do construto.
- A variante selada deve ser gerada e armazenada fora do core publico.
- Seeds, budgets, pesos e limiares finais devem ser preregistrados antes do freeze.
- Alteracoes posteriores exigem CHANGE-ID e analise de comparabilidade.

## Saida esperada de B1

Uma linha aprovada por capacidade, com protocolo preregistrado, controles executaveis, plano estatistico, testes de shortcut/leakage e criterio objetivo de invalidacao.

As linhas acima sao propostas corretivas, nao aprovacao. B1 permanece `BLOCKED` ate revisao cientifica humana registrar responsavel, decisao e CHANGE-ID de aprovacao.
