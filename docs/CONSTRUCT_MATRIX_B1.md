# Matriz de construtos B1

Status: `APPROVED AS INITIAL FRAMEWORK - 2026-08-31`

Registro de aprovacao: `docs/reviews/B0_B1_GATE_REVIEW_2026-08-31.md`  
CHANGE-ID: `CHG-2026-08-31-B0-B1-APPROVAL`

Esta matriz impede que uma bateria seja implementada antes de definir o que ela mede. Campos como tarefa, seed, budget e limiar permanecem pendentes ate preregistro e aprovacao cientifica.

## Contrato de preenchimento

Cada linha precisa responder: qual capacidade observavel e medida, qual hipotese sera testada, quais controles distinguem a capacidade de um shortcut, quais dados serao publicados, como a incerteza sera calculada e em que condicao o teste e `TEST_INVALID`.

| ID | Construto operacional | Hipotese preregistrada | Tarefa publica | Variante selada | Controles | Metricas primarias | Metricas secundarias | Seeds/budget | Shortcut/leakage | Criterio TEST_INVALID | Responsavel/status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | adquirir politica util por experiencia | PENDENTE | PENDENTE | PENDENTE | random; rule-based; baseline pertinente | retorno; AUC; passos ate limiar | estabilidade entre seeds | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C2 | aprender com menos interacoes ambientais | PENDENTE | PENDENTE | PENDENTE | baseline de interacao | retorno/interacao; interacoes ate limiar | custo por ganho | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C3 | generalizar para instancias e estruturas nao vistas | PENDENTE | PENDENTE | PENDENTE | treino; ID-heldout; OOD | gap; zero-shot; adaptacao few-shot | recuperacao | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C4 | adaptar-se a mudanca nao anunciada | PENDENTE | PENDENTE | PENDENTE | politica persistente; adaptador de controle | latencia de deteccao; latencia de adaptacao; regret | recovery rate | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C5 | usar informacao passada quando nao esta observavel | PENDENTE | PENDENTE | PENDENTE | memoria sem interferencia; controle sem pista | retencao; precisao | resistencia a interferencia | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C6 | escolher acao por consequencias atrasadas | PENDENTE | PENDENTE | PENDENTE | myopic; planejamento pertinente | retorno; regret; horizonte efetivo | replanejamento | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C7 | aprender sequencias sem destruir competencias | PENDENTE | PENDENTE | PENDENTE | treino isolado; ordem alternativa | forgetting; backward/forward transfer | plasticidade; retencao | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C8 | manter degradacao mensuravel sob perturbacao | PENDENTE | PENDENTE | PENDENTE | sem ruido; controle de falha | curva de degradacao | recuperabilidade | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C9 | transferir para familias de problemas distintas | PENDENTE | PENDENTE | PENDENTE | agente congelado por dominio | zero-shot; few-shot; desempenho final | velocidade de adaptacao | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| C10 | produzir incerteza calibrada quando suportada | PENDENTE | PENDENTE | PENDENTE | predictor nao calibrado; baseline | Brier; ECE; selective accuracy | curva de calibracao | PENDENTE | PENDENTE | PENDENTE | `NOT_SUPPORTED` quando nao houver confianca explicita |
| C11 | entregar capacidade por custo computacional | PENDENTE | PENDENTE | PENDENTE | hardware e ambiente controlados | tempo; CPU/GPU; RAM/VRAM | energia; parametros; interacoes | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

## Regras de revisao

- `PENDENTE` nao e criterio de aprovacao; e um bloqueio de B1.
- Nenhuma linha pode definir uma arquitetura interna necessaria.
- Controles devem testar sensibilidade e especificidade do construto.
- A variante selada deve ser gerada e armazenada fora do core publico.
- Seeds, budgets, pesos e limiares finais devem ser preregistrados antes do freeze.
- Alteracoes posteriores exigem CHANGE-ID e analise de comparabilidade.

## Saida esperada de B1

Uma linha aprovada por capacidade, com protocolo preregistrado, controles executaveis, plano estatistico, testes de shortcut/leakage e criterio objetivo de invalidacao.
