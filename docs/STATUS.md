# Status do projeto

- Data de referencia: 2026-08-31
- Fonte recebida: `PLANO_DIRETOR_MESTRE_BENCHMARK_IA_ML.pdf`
- Gate atual: B2/B3 em implementacao inicial; B0 e B1 aprovados em 2026-08-31
- Estado: infraestrutura executavel e tarefa publica C1 em desenvolvimento; nenhum benchmark final congelado
- Skills: `gate-review` ativa; validador, promotor e exportador iniciais implementados
- Regra de entrada: nenhuma arquitetura candidata antes da barreira B14/B15

## Concluido

- Missao, neutralidade, API conceitual, 11 capacidades e gates extraidos do plano diretor.
- Estrutura de documentos para execucao, tecnologia, Git, decisoes e handoff criada.
- Validacao automatica da presenca de arquivos, gates e regras essenciais executada com sucesso.
- Estrutura de skills criada com template, catalogo, ciclo de vida e validacao sem dependencias externas.
- Charter B0 e matriz de construtos B1 criados como rascunhos, sem declarar aprovacao cientifica.
- Contrato B2 implementado em `src/benchmark_core/protocol.py`, com validacao de ciclo de vida e testes focados.
- Manifest B2 implementado em `src/benchmark_core/manifest.py`, com schema JSON, timeout finito e verificacao de determinismo.
- Runner B3 inicial implementado com processo isolado, timeout real, estados de erro e registry JSONL append-only com hashes.
- Executor de episodios adicionado com estado persistente por episodio, validator de acao, timeout e rejeicao controlada de entradas nao serializaveis.
- Artefatos estruturados e CLI de hash canonico adicionados; sobrescrita de artefato e run_id inseguro sao rejeitados por padrao.
- Fluxo `execute_run` integrado: manifest, config, episodio, artefato bruto e registry agora sao exercitados ponta a ponta.
- Protocolo C1 aprovado para implementacao controlada; tarefa, seeds, budget e limiar continuam pendentes antes da execucao final.
- Tarefa publica C1 de desenvolvimento implementada com bandit estacionario, controles Random/EpsilonGreedy e testes de reproducibilidade e aprendizagem.
- Metricas e avaliacao multi-seed implementadas, preservando distribuicao e status por seed.
- Fechamento B0/B1 aprovado e registrado em `docs/reviews/B0_B1_GATE_REVIEW_2026-08-31.md` com CHANGE-ID.

## Proximo passo executavel

Completar B2/B3 com CLI de run e integração de relatório/artefatos. Validar a tarefa pública C1, preencher parâmetros pendentes com evidências de validade e preparar o primeiro experimento preregistrado. Depois aplicar o mesmo padrão às capacidades C2-C11, sem criar conjunto selado antes da validação e freeze. Ao fechar qualquer gate, executar `gate-review` e extrair skills adicionais se houver procedimento repetivel.

## Bloqueios conhecidos

- Ainda nao existem tarefas concretas preregistradas, runner, baselines ou ambiente sealed.
- Stack Python e registry sao propostas provisorias, nao decisoes cientificas congeladas.
- Licenca, armazenamento restrito, preregistro, responsaveis nominais e protocolos concretos B1 ainda precisam de definicao.
