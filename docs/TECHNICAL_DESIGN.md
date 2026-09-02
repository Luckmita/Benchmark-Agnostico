# Desenho tecnico inicial

## Stack proposta

- Python 3.12 para core, ambientes, baselines, runner e analise.
- `uv` para ambiente e lock de dependencias.
- Pydantic v2 ou dataclasses com validacao explicita para contratos e manifests.
- Gymnasium apenas como referencia de ciclo de vida quando compatibilidade for util; o contrato publico do benchmark permanece proprio e agnostico.
- NumPy, SciPy e pandas para calculos; DuckDB ou Parquet para consultas de resultados.
- Pytest, Ruff, Mypy e pre-commit para qualidade.
- Docker para reproducao; imagens devem ser fixadas por digest no release.
- MLflow nao e requisito inicial: o registry local versionado deve ser a fonte auditavel, com exportacao simples.

A stack e uma decisao de engenharia provisoria. Ela nao pode introduzir dependencia de framework na avaliacao de candidatos.

## API conceitual

```python
class Agent:
    def reset(self, specification): ...
    def observe(self, observation): ...
    def act(self): ...
    def learn(self, transition): ...
    def save(self): ...
    def load(self): ...
```

O runtime deve aceitar agentes sem aprendizagem online e declarar capabilities opcionais no manifest. A API deve validar tipos, limites, timeout, reset e determinismo.

O primeiro contrato executavel esta em `src/benchmark_core/protocol.py`. `validate_agent` verifica os seis pontos do ciclo de vida, seed, capabilities e espacos opacos, e executa save/load quando `persistence` for declarado. `AgentManifest` em `src/benchmark_core/manifest.py` fornece metadados versionados; seu contrato JSON esta em `schemas/agent_manifest.schema.json`. A cobertura esta em `tests/test_protocol.py`; observacao e acao permanecem opacas ao core. Timeout real, limites de acao e isolamento de processo pertencem ao runner B3.

O contrato normativo executavel B2 esta documentado em `docs/contracts/UNIVERSAL_AGENT_API_V0.1.md`. Capabilities sao booleanas e devem coincidir entre manifest e specification. Persistencia exige estado serializavel. Agentes com `uncertainty=True` retornam `AgentDecision` com confianca finita em `[0,1]`; os demais continuam retornando a acao opaca diretamente.

O runner inicial esta em `src/benchmark_core/runner.py`: cada acao roda em processo `spawn`, recebe timeout duro e retorna `PASS`, `ERROR` ou `TIMEOUT`. `RunRegistry` em `src/benchmark_core/registry.py` grava JSONL append-only; `hash_json`, `hash_file`, `hash_paths` e `hash_source_tree` produzem hashes SHA-256 para rastreabilidade. A cobertura esta em `tests/test_runner.py`. Limites semanticos continuam pertencendo ao ambiente por `action_validator`.

`run_episode` em `src/benchmark_core/episode.py` executa um episodio inteiro em um unico processo isolado, mantendo o estado do agente entre passos e entregando `Transition` quando `online_learning` esta habilitado. O ambiente e o factory devem ser serializaveis para `spawn`; entradas nao serializaveis retornam `ERROR` de forma controlada. O ambiente fornece `action_validator` para impor limites semanticos sem acoplar o core a uma representacao de acao.

`ArtifactStore` em `src/benchmark_core/artifacts.py` cria grupos separados por `run_id` e recusa sobrescrita por padrao. A CLI `scripts/benchmark_cli.py hash-json` aceita JSON como argumento ou stdin e produz hash canonico para uso em pipelines.

`execute_run` em `src/benchmark_core/run.py` e o orquestrador ponta a ponta: grava manifest, config e metadados com hashes; executa um episodio isolado; preserva a sequencia de acoes, recompensas e latencias em `raw`; grava metrica e log separados; e anexa o `RunRecord` com tempos reais. O fluxo e coberto em `tests/test_run.py`.

`python -m benchmark_core.cli run-public-c1` oferece um run publico reproduzivel para verificar B2/B3 sem acessar sealed ou candidatos. O teste `tests/test_cli.py` confirma a criacao de registry e dos cinco grupos de artefatos.

B3 usa IDs portaveis com claim atomico por registry, rejeita duplicatas, cria novos JSONs de forma exclusiva e proibe overwrite de raw. Registros validam status, timestamps, seed e hashes; JSON nao finito e rejeitado. Em falha de ambiente/acao, passos ja concluidos permanecem no resultado quando o processo consegue responder.

A primeira tarefa publica de desenvolvimento C1 esta em `src/benchmark_core/tasks/c1_learning.py`. Ela e uma familia de bandits estacionarios configuraveis, com controles aleatorio e epsilon-greedy. A tarefa nao representa ainda o conjunto final selado e nao deve ser tratada como benchmark congelado.

`src/benchmark_core/metrics.py` fornece resumo descritivo, IC95 aproximado, efeito pareado, win rate, AUC e passos ate limiar. `src/benchmark_core/evaluation.py` executa um agente por seeds explicitas e retorna a distribuicao completa, status por seed e resumo estatistico. Nenhum resultado derivado substitui os artefatos brutos de cada run.

Os prototipos publicos em `src/benchmark_core/tasks/c_batteries.py` seguem a taxonomia normativa: C2 checkpoints de eficiencia amostral, C3 particoes de generalizacao, C4 drift, C5 delayed cue, C6 retorno atrasado, C7 matriz de continual learning, C8 wrapper de perturbacao e C9 contrato multidominio. C10 possui metricas probabilisticas em `metrics.py`; C11 possui instrumentacao local limitada em `resources.py`. Esses componentes sao testes de contrato e desenvolvimento, nao baterias validadas.

Os scripts historicos que declaravam freeze ou `PASS` generico falham de forma fechada. O historico executavel permanece recuperavel pelo Git, mas nao pode sobrescrever artefatos nem produzir novos claims invalidos.

## Componentes

- `benchmark_core`: contratos, ambientes, tarefas, metricas e validadores.
- `benchmark_runner`: planejamento de runs, isolamento, timeout, coleta e finalizacao.
- `benchmark_baselines`: controles tecnicamente pertinentes.
- `benchmark_analysis`: estatistica, tabelas e relatorios sem sobrescrever raw.
- `benchmark_registry`: schema de runs e indexacao de artefatos.
- `benchmark_sanitizer`: procura de seeds seladas, paths, condicionais por submission e dependencias proibidas.
- `submission_sdk`: somente depois de B14, com adapter, manifest e testes de conformidade.

## Layout de repositorios

O plano diretor pede separacao fisica. A implementacao deve preservar isso:

```text
ai-benchmark-core/
  src/benchmark_core/
  tests/
  configs/public/
  docs/
  schemas/
  scripts/
ai-benchmark-submissions/
  submissions/<submission_id>/adapter/
  submissions/<submission_id>/manifest/
  submissions/<submission_id>/hashes/
ai-benchmark-sealed/
  tasks/
  seeds/
  perturbations/
```

O repositorio sealed deve ter acesso restrito e nunca ser dependencia de desenvolvimento publico. Nenhum dado de candidato entra no core.

## Registry minimo

Cada run deve registrar `run_id`, timestamp, benchmark_version, environment, scenario, seed, submission, model_hash, adapter_hash, config_hash, hardware, software, start_time, end_time e status. Artefatos devem separar `raw/`, `derived/`, `logs/`, `metrics/` e `manifest/`.

## Reproducibilidade

Uma execucao reproduzivel exige lockfile, imagem ou ambiente identificado, config imutavel, seed explicita, hash do codigo e artefatos brutos. O relatorio deve apontar para o run_id; dados derivados nunca substituem os brutos.
