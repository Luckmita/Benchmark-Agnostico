# Revisao de fechamento B3

- Data: 2026-09-02
- Gate: B3 - Experimental Infrastructure
- Decisao: `PASS`
- CHANGE-ID: `CHG-2026-09-02-B3-REPRODUCIBLE-RUNS`
- Escopo: infraestrutura publica; nenhuma arquitetura candidata ou dado sealed

## Criterios de saida e evidencia

| Criterio | Evidencia | Resultado |
| --- | --- | --- |
| Ambiente reproduzivel | `.python-version`, `requirements-dev.lock`, `docs/ENVIRONMENT_B3.md` | PASS |
| Runner isolado e timeout duro | `runner.py`, `episode.py`, testes de timeout/processo | PASS |
| Lifecycle stateful | um processo por episodio; teste de aprendizagem online | PASS |
| `run_id` portavel e unico | regex comum, claim atomico e rejeicao de duplicata | PASS |
| Registry append-only | JSONL, validacao de registro, claim por ID, timestamps | PASS |
| Raw imutavel | criacao exclusiva; overwrite de `raw` proibido | PASS |
| Artefatos separados | `raw`, `derived`, `logs`, `metrics`, `manifest` | PASS |
| Rastreabilidade | hashes de source/config/manifest, seed, hardware/software, tempos | PASS |
| Preservacao de falha | status/erro e passos concluidos mantidos quando possivel | PASS |
| JSON canonico valido | NaN/Infinity rejeitados em config e artifacts | PASS |
| CLI ponta a ponta | `python -m benchmark_core.cli run-public-c1` | PASS |

## Reproducao limpa

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m pip install -e . --no-build-isolation --no-deps
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m benchmark_core.cli run-public-c1 --output-root .venv\b3-output --run-id b3-clean-run --seed 23 --max-steps 5
```

Resultado:

- versao verificada: Python 3.14.7;
- suite: `55 passed, 3 skipped`;
- run: `PASS`;
- registry incluiu `run_id`, code/config hashes, seed, timestamps, hardware/software e status;
- artifact tree incluiu claim do ID e arquivos em raw/logs/metrics/manifest; o grupo derived foi criado vazio, como esperado para run sem derivacao;
- ambiente temporario removido depois da verificacao.

## Limites

- Os tres skips sao testes de symlink indisponiveis no Windows atual; as protecoes continuam implementadas e sao cobertas quando o host permite criar symlinks.
- O lock fixa o ambiente local de desenvolvimento, mas B14 ainda exigira imagem por digest e freeze de release.
- Nao ha contabilizacao de GPU/energia nem sandbox de candidato; pertencem a B10/B16.
- Claims atomicos evitam duplicatas concorrentes simples; recuperacao operacional de claim orfao deve ser definida antes do servico multiworker.

## Skills

`gate-review` foi aplicada. Nenhuma skill nova foi promovida. O procedimento de ambiente limpo ainda pode evoluir antes de justificar uma skill separada.

## Proximo passo

Abrir B4 para selecionar controles negativos, positivos e baselines tecnicamente pertinentes por construto. Resultados exploratorios anteriores nao contam como validacao B4.
