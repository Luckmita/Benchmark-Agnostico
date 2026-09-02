# Plano de orientacao e revisao corretiva

Data: 2026-09-01  
Branch: `fix/chg-2026-09-01-gate-realignment`  
Estado inicial: revisao documental e tecnica; nenhuma submissao candidata autorizada  
CHANGE-ID principal: `CHG-2026-09-01-GATE-REALIGNMENT`

## Objetivo

Realinhar o repositorio com o plano diretor, restaurar a correspondencia entre gates e evidencias, corrigir a taxonomia C1-C11 e deixar o proximo passo cientifico executavel sem antecipar o conjunto selado ou a entrada de candidatos.

Este plano nao declara gates aprovados. Cada gate somente pode receber `PASS` quando todos os seus criterios de saida apontarem para evidencia reproduzivel. Falhas de validade devem ser registradas como `BLOCKED` ou `TEST_INVALID`, nunca reinterpretadas como aprovacao.

## Diagnostico de partida

1. `docs/STATUS.md` declara C1-C11 congeladas e sugere inscricao em B14/B15, mas o plano diretor reserva B14 ao release candidate, B15 a replicacao independente e B16 a primeira submissao.
2. O conjunto selado pertence a B13 e deve existir antes do freeze B14; ele nao pode ser criado depois da abertura a candidatos.
3. A matriz B1 ainda contem campos `PENDENTE` que o proprio contrato define como bloqueadores.
4. Os identificadores C3-C11 usados nas baterias recentes divergem da taxonomia normativa. Interpretabilidade, composicionalidade, coordenacao multiagente e transparencia nao substituem as capacidades C3-C11 do plano diretor.
5. Os documentos de freeze misturam `FROZEN`, `VALIDATED` e `READY`, apesar de concluirem que todas as capacidades foram validadas.
6. Os resultados existentes sao resumos de desenvolvimento. Eles nao formam a cadeia completa `run_id` -> manifest/config/hashes -> raw -> derived/metrics/logs.
7. A validacao em lote declara um teste estatistico que nao e calculado e usa diferenca de medias como `PASS` sem criterio de aceite executavel.
8. A suite exige configuracao manual de `PYTHONPATH`; a reproducao documentada e o ambiente fixado ainda precisam ser completados.

## Regras durante a correcao

- Preservar documentos e resultados historicos; adicionar revisoes corretivas em vez de reescrever a historia experimental.
- Nao criar, inspecionar ou aceitar arquitetura candidata.
- Nao armazenar seeds finais, tarefas ocultas, perturbacoes seladas ou ground truth no core publico.
- Toda mudanca em construto, ambiente, reward, metrica, scoring, seed, budget ou protocolo recebe CHANGE-ID e analise de comparabilidade.
- Adapters permanecem conversores de protocolo, sem features, memoria, hints ou correcoes.
- O resultado cientifico permanece um vetor de capacidades, sem ranking unico.

## Fases de trabalho

### R0 - Preservacao e governanca

Entregaveis:

- registrar este plano e o CHANGE-ID;
- corrigir `README.md`, `docs/STATUS.md` e `docs/DECISIONS.md` para um unico gate atual;
- marcar aprovacoes conflitantes como historicas e superadas por revisao corretiva, sem apaga-las;
- criar uma matriz de gates B0-B15 com evidencia, resultado e bloqueadores.

Criterio de aceite: nenhuma documentacao ativa afirma que candidatos entram em B14/B15 ou que B13 esta concluido sem repositorio selado separado.

### R1 - Taxonomia e preregistro

Entregaveis:

- restaurar a taxonomia normativa: C1 aprendizagem; C2 eficiencia amostral; C3 generalizacao; C4 adaptacao; C5 dependencia temporal; C6 planejamento; C7 continual learning; C8 robustez; C9 transferencia multidominio; C10 incerteza; C11 eficiencia computacional;
- classificar os experimentos existentes como prototipos publicos exploratorios, sem validade de freeze;
- alinhar matriz, protocolos, nomes de classes, scripts e testes;
- exigir pergunta, hipotese, controles, tarefa publica, variante selada planejada, metricas, seeds/budget, estatistica, shortcuts/leakage e `TEST_INVALID` por bateria.

Criterio de aceite: nao existe colisao entre ID de capacidade, construto, protocolo, implementacao e relatorio.

### R2 - B2/B3 reproduziveis

Entregaveis:

- documentar instalacao e comando de testes sem `PYTHONPATH` manual;
- completar manifest e schema com metadados necessarios ao processo de submissao, sem liberar submissao;
- assegurar que cada run grave manifest, config, hashes, resultado bruto, tempos, hardware/software e registro append-only;
- fornecer CLI de execucao e teste ponta a ponta em diretorio temporario;
- documentar quais garantias exigem isolamento externo ou container.

Criterio de aceite: um terceiro instala o projeto, executa um run publico e rastreia um numero derivado ate seu artefato bruto usando `run_id`.

### R3 - B4 e baterias publicas

Entregaveis:

- selecionar controles positivos e negativos pertinentes a cada construto;
- implementar primeiro uma vertical C1 completa e validar sensibilidade, especificidade, discriminacao, confiabilidade, shortcut e leakage;
- expandir apenas depois para C2-C11, respeitando B5-B10;
- medir as metricas preregistradas, nao proxies escolhidos por conveniencia;
- preservar distribuicoes completas, incerteza, efeito, comparacoes pareadas e outliers.

Criterio de aceite: cada bateria possui evidencia por criterio de validade; qualquer falha critica produz `TEST_INVALID`.

### R4 - B11/B12

Entregaveis:

- executar validacao do benchmark sobre todas as baterias;
- realizar red team de shortcuts, leakage, reward hacking, falhas degeneradas e dependencia de seed;
- registrar incidentes, correcoes e repeticoes com CHANGE-ID quando aplicavel;
- obter revisao metodologica separada da implementacao.

Criterio de aceite: B11 e B12 possuem relatorios reproduziveis e nenhum bloqueador critico aberto.

### R5 - B13/B15 e barreira de submissao

Entregaveis futuros, fora do core publico:

- B13: criar storage/repositorio selado separado, acesso restrito, geracao auditavel e politica de custodia;
- B14: congelar release candidate, codigo, metricas, budgets, pesos e hashes;
- B15: obter replicacao independente por terceiro;
- B16: somente depois, abrir manifest, auditoria de adapter e avaliacao selada de candidatos.

Criterio de aceite: a primeira submissao somente entra depois de B14 e B15 aprovados.

## Estrategia de validacao

Aplicar, na menor unidade possivel:

1. teste unitario do contrato alterado;
2. teste de integracao do slice;
3. suite completa;
4. validadores documentais e de skills;
5. `gate-review` para todo gate ou marco grande;
6. verificacao de `git diff`, segredos, artefatos gerados e rastreabilidade antes de commit/push.

Comandos-base:

```powershell
python -m pip install -e .
python -m pytest -q
python scripts/skill_validator.py
git status --short
```

## Politica de commits e publicacao

- usar branch dedicada; nao fazer push direto em `main`;
- manter commits pequenos e coerentes;
- incluir `CHG-2026-09-01-GATE-REALIGNMENT` nos commits cientificos/corretivos;
- publicar a branch para preservar historico e permitir revisao;
- nao fazer merge, tag ou release sem aprovacao do responsavel e criterios verdes.

## Definicao de concluido desta correcao

Esta rodada termina quando:

- a documentacao ativa representa fielmente o gate real;
- a taxonomia normativa esta consistente no repositorio;
- os prototipos invalidos nao sao apresentados como benchmark congelado;
- B2/B3 possuem caminho reproduzivel e evidencia automatizada proporcional ao escopo implementado;
- existe uma auditoria de gates com bloqueadores objetivos e proximo passo executavel;
- testes e validadores passam;
- a branch e seus commits foram enviados ao remoto.

Fechar todos os gates ate B15 nao pode ser automatizado apenas por alteracoes neste repositorio: B12 requer auditoria adversarial separada, B13 requer infraestrutura de acesso restrito e B15 requer terceiro independente. Esses itens permanecerao explicitamente bloqueados ate existir evidencia externa valida.

## Resultado da execucao - 2026-09-02

Estado: `CORRECTIVE ENGINEERING MILESTONE COMPLETE; B1 BLOCKED`.

- R0 concluido: status, decisoes, historico e matriz de gates realinhados.
- R1 concluido como proposta: taxonomia canonica, protocolos corretivos e prototipos publicos consistentes; aprovacao cientifica continua externa.
- R2 concluido no escopo local: instalacao editavel, manifest/schema, hashes, tempos, CLI e artefatos por `run_id`; lock/container e executor separado continuam pendentes.
- R3 nao e declarado concluido como gate: controles e prototipos existem, mas a vertical C1 confirmatoria depende de preregistro aprovado.
- R4 e R5 permanecem bloqueados por revisao/red team separados, storage restrito e terceiro independente.

Validacao em ambiente virtual limpo: `45 passed, 3 skipped`; `scripts/check_governance.py` e `scripts/skill_validator.py` passaram; run publico C1 retornou `PASS` e gerou registry rastreavel.

Relatorio de fechamento: `docs/reviews/CORRECTIVE_MILESTONE_REVIEW_2026-09-02.md`.

Atualizacao: B1 foi aprovado posteriormente pelo responsavel do projeto em 2026-09-02, sob `CHG-2026-09-02-B1-CORRECTIVE-APPROVAL`. B2 passou a ser o gate atual; o escopo quantitativo continua condicionado a preregistro.
