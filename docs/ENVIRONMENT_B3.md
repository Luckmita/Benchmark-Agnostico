# Ambiente de referencia B3

Status: `REFERENCE ENVIRONMENT - 2026-09-02`

CHANGE-ID: `CHG-2026-09-02-B3-REPRODUCIBLE-RUNS`

## Versoes

- Python de referencia: 3.14.7, registrado em `.python-version`.
- Compatibilidade declarada do pacote: Python >=3.12 e <3.15.
- Dependencias de desenvolvimento: pins exatos em `requirements-dev.lock`.
- Dependencias runtime do core: nenhuma alem da standard library.

O ambiente de referencia permite reproduzir o gate B3 local. Suporte a outras versoes dentro da faixa declarada e compatibilidade, nao identidade do ambiente.

## Criacao limpa

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m pip install -e . --no-build-isolation --no-deps
.\.venv\Scripts\python.exe -m pytest -q
```

Antes de usar o ambiente como evidencia, conferir `python --version` contra `.python-version`. Um executor com outra patch/minor deve registrar a divergencia em `software`.

## Run publico de verificacao

```powershell
.\.venv\Scripts\python.exe -m benchmark_core.cli run-public-c1 `
  --output-root artifacts/public-demo `
  --run-id demo-c1-seed-42 `
  --seed 42
```

O run precisa produzir registry JSONL e os grupos `raw`, `derived`, `logs`, `metrics` e `manifest`. O `run_metadata` deve conter hash do source tree, config, manifest, tempos, hardware e software.

## Limites

- O lock nao substitui imagem por digest para B14.
- Medicao de energia, GPU e isolamento de host exigem infraestrutura posterior.
- `.venv` e artifacts sao locais e ignorados pelo Git.
- Nenhum dado sealed ou candidato pertence a este ambiente publico.
