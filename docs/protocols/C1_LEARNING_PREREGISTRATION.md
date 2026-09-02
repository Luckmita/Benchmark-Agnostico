# C1 - Preregistracao de aprendizagem

Status: `APPROVED AS B1 CONSTRUCT PROTOCOL - 2026-09-02`

CHANGE-ID vigente: `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`

Registro vigente: `docs/reviews/B1_CORRECTIVE_APPROVAL_2026-09-02.md`

Este documento define a estrutura aprovada de construto para C1. Nao e um freeze e nao autoriza conjunto selado. Parametros quantitativos exigem preregistro separado antes da implementacao confirmatoria.

## Pergunta

O agente consegue adquirir uma politica util por experiencia, sem depender de comportamento especifico pre-programado para a tarefa?

## Construto operacional

Aprendizagem e a melhora observavel de desempenho ao longo de interacoes com um ambiente estacionario, comparada ao desempenho inicial e a controles que nao aprendem.

O teste mede comportamento. Nao infere modulo, memoria, representacao, algoritmo ou mecanismo interno.

## Hipotese

`H1`: sob o mesmo protocolo, um agente com aprendizagem habilitada apresenta melhora de retorno ao longo das interacoes e supera o controle aleatorio por uma diferenca predefinida.

`H0`: a curva de retorno do agente nao supera a variabilidade esperada do controle aleatorio ou nao demonstra tendencia de aprendizagem preregistrada.

## Tarefa candidata

Ambiente estacionario de decisao com observacao e acao publicas, recompensa atrasada o suficiente para exigir aquisicao de contingencia. A instancia final deve possuir parametros gerados por uma regra publica e uma variante selada da mesma familia.

Implementacao publica de desenvolvimento: `benchmark_core.tasks.C1BanditEnvironment` usa observacao constante, duas acoes e probabilidades de recompensa configuraveis. `RandomAgent` e `EpsilonGreedyAgent` fornecem controles executaveis para a vertical inicial. Esta implementacao serve para validar a infraestrutura; seus parametros default nao sao valores finais da v1.

A tarefa concreta, espaco de observacao, numero de acoes, distribuicao de recompensas e limiar ainda sao `PENDENTE` ate revisao de validade de construto.

## Controles

- `Random`: controle negativo; nao deve apresentar curva de aprendizagem consistente.
- `Rule-based`: controle positivo somente se a regra for construida independentemente do agente.
- Um baseline de aprendizagem pertinente ao tipo de tarefa, escolhido antes dos resultados.

Controles nao podem ser ajustados depois de observar resultados de submissao.

## Protocolo proposto

1. Inicializar o ambiente e o agente com seed registrada.
2. Executar o numero de interacoes definido no preregistro.
3. Registrar cada recompensa, observacao publica, acao, terminacao e timestamp.
4. Entregar `Transition` somente quando `online_learning` estiver declarado.
5. Repetir o protocolo para todas as seeds preregistradas.
6. Executar a variante selada somente depois do freeze.

O ambiente nao entrega ground truth, hint ou historico extra ao agente. O adapter apenas converte o protocolo.

## Metricas

Primarias propostas:

- Retorno por episodio e por interacao.
- AUC da curva de aprendizagem.
- Passos ate o limiar de desempenho.
- Variabilidade entre seeds.

Secundarias:

- Retorno inicial.
- Retorno final.
- Taxa de convergencia.
- Falhas e terminacoes anormais.

As definicoes matematicas, limiar, janela de suavizacao e tratamento de runs incompletos devem ser fixados antes da execucao.

## Estatistica

- Reportar media, mediana, desvio padrao, IC95, tamanho de efeito e distribuicao completa.
- Usar comparacoes pareadas por seed quando aplicavel.
- Preregister exclusoes, outliers, criterio de parada e teste estatistico.
- Nao publicar somente uma media agregada.

## Seeds e budget

- Seeds finais: `PENDENTE - seladas somente apos aprovacao e freeze`.
- Numero de seeds: `PENDENTE`.
- Interacoes por seed: `PENDENTE`.
- Timeout por episodio: definido no manifest e confirmado pelo runner.
- Budget computacional: `PENDENTE`.

Nenhuma seed final pode ser usada durante desenvolvimento da variante selada.

## Shortcuts e leakage

Antes da aprovacao, testar pelo menos:

- Politica fixa que explora uma sequencia conhecida.
- Memorizacao de seed, ID ou ordem de instancia.
- Recompensa ou observacao que revele a acao correta.
- Inconsistencia de `reset` que permita acumular estado indevido.
- Informacao de teste em metadados, paths, logs ou timing.
- Solucao que maximize a metrica sem aprender a contingencia.

Qualquer shortcut relevante bloqueia a validade da bateria e exige `TEST_INVALID` ou revisao do construto.

## Critério de validade

A bateria so pode ser considerada valida se demonstrar sensibilidade, especificidade, discriminacao, confiabilidade e ausencia de shortcut/leakage relevante. Caso contrario, o status e `TEST_INVALID`, independentemente do desempenho do agente.

## Critério de aceite da proposta

- [ ] Tarefa concreta e familia de instancias aprovadas.
- [ ] Hipotese e limiar definidos antes dos resultados.
- [ ] Controles implementaveis e independentes.
- [ ] Seeds, budget e paradas definidos.
- [ ] Metricas e analise estatistica preregistradas.
- [ ] Testes de shortcut e leakage planejados.
- [ ] Variante selada definida sem expor seus parametros.
- [ ] Responsavel cientifico e revisor registrados.

## Proximo passo

O conselho cientifico deve preencher os campos `PENDENTE`, revisar a validade de construto e aprovar ou rejeitar esta proposta. Somente depois a engenharia deve implementar o ambiente C1 e sua bateria de testes.
