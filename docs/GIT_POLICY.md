# Politica de organizacao e Git

## Principios

- Um repositorio por fronteira de confianca: core publico, submissions e sealed.
- Um commit deve representar uma mudanca coerente e pequena.
- Nenhum segredo, seed final, peso de candidato ou dado selado no repositorio publico.
- Nenhum resultado historico e reescrito; correcao material cria nova versao.

## Pastas no core

```text
src/                 codigo de producao
 tests/              testes unitarios, contrato e integracao
configs/             configuracoes publicas e preregistros
schemas/             contratos versionados
docs/                metodologia, ADRs e protocolos
scripts/             comandos reproduziveis
artifacts/           ignorado por padrao; raw/derived/logs/metrics/manifest em storage de run
```

Nomes: `snake_case` para Python, `SCREAMING_SNAKE_CASE` para constantes, IDs estaveis para cenarios e `YYYYMMDD` somente em relatorios humanos. Nunca usar nomes como `final2`, `novo`, `teste_real` ou paths dependentes de uma maquina.

## Branches

- `main`: somente estado revisado e reproduzivel.
- `feature/<id>-<slug>`: implementacao de uma tarefa.
- `fix/<id>-<slug>`: correcao rastreada.
- `science/<id>-<slug>`: construto, metrica ou protocolo.
- `release/vX.Y`: preparacao de release e freeze.

## Commits

Formato: `<tipo>(<escopo>): <imperativo>`.

Tipos aceitos: `feat`, `fix`, `test`, `docs`, `refactor`, `build`, `ci`, `science`, `chore`.

Toda mudanca em reward, ambiente, distribuicao, metrica, scoring, adapter protocol, seeds ou budgets exige `CHANGE-ID` no corpo do commit e em `docs/DECISIONS.md`. Exemplo: `science(C1): preregister learning curve protocol`.

## Pull requests

Requerem descricao do problema, gate afetado, evidencias, impacto cientifico, risco de leakage/viés, testes executados e plano de rollback. Mudancas cientificas exigem revisao de metodologia; mudancas de runtime exigem revisao de engenharia. Merge somente com CI verde e revisores adequados.

## Push e pull

Antes de `pull`, preservar trabalho local em branch ou stash aprovado e verificar status. Depois de `pull`, rodar testes do slice afetado. Push direto em `main` e proibido. Tags de release devem ser assinadas quando a infraestrutura permitir.

## Checklist de commit

- [ ] Sem segredo ou artefato gerado.
- [ ] Testes e lint executados.
- [ ] Documentacao e schema atualizados.
- [ ] CHANGE-ID criado quando necessario.
- [ ] Nenhum teste depende de dado selado.
- [ ] Alteracao e reproduzivel por outro agente.
