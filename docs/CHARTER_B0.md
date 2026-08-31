# Charter B0 - Governanca e escopo

Status: `APPROVED - 2026-08-31`

Registro de aprovacao: `docs/reviews/B0_B1_GATE_REVIEW_2026-08-31.md`  
CHANGE-ID: `CHG-2026-08-31-B0-B1-APPROVAL`

Este charter operacionaliza o plano diretor sem substitui-lo. A aprovacao de B0 deve ser registrada em `docs/DECISIONS.md` com responsavel, data e CHANGE-ID quando aplicavel.

## Missao

Construir uma plataforma independente para medir capacidades funcionais observaveis de agentes e arquiteturas de IA/ML sob protocolos controlados, reproduziveis e auditaveis.

## Escopo da versao inicial

A v1 estudara onze dimensoes: aprendizagem, eficiencia amostral, generalizacao, adaptacao a mudanca, dependencia temporal, planejamento, continual learning, robustez, transferencia multidominio, calibracao de incerteza e eficiencia computacional.

O resultado primario sera um perfil multidimensional por capacidade. Um score unico nao sera publicado como resultado cientifico primario.

## Fora de escopo

- Inferir consciencia, inteligencia geral ou mecanismos internos.
- Comparar arquiteturas candidatas antes de B14/B15.
- Criar tarefas, metricas ou pesos para favorecer uma arquitetura.
- Incluir dados, codigo, seeds ou hints de candidatos no core.
- Alterar a v1 depois de observar uma submissao; correcao material abre nova versao.

## Separacao de responsabilidades

| Funcao | Responsabilidade | Restricao |
| --- | --- | --- |
| Conselho cientifico | construtos, hipoteses, metricas, estatistica e aprovacao de mudancas | nao otimizar tarefas para candidatos |
| Engenharia do benchmark | API, ambientes, runner, registry, testes e reproducao | nao criar adapters de candidatos antes da barreira |
| Validacao/red team | shortcuts, leakage, reward hacking, degenerescencia e validade | nao alterar o benchmark sem registro |
| Auditoria externa | reconstruir, executar baselines, conferir hashes e conclusoes | independente da implementacao principal |
| Agentes de desenvolvimento | executar tarefas, registrar evidencias e propor skills | nao aprovar a propria mudanca cientifica |

## Regras de evidencia

Toda afirmacao deve apontar para versao, codigo ou config, hash, seed, `run_id`, hardware, software e artefato bruto quando aplicavel. Resultados negativos e testes invalidos permanecem registrados.

## Gates e barreira

B0-B13 constroem e validam o benchmark. B14 congela a release candidate. B15 requer replicacao independente. Somente depois dessa barreira B16 pode aceitar submissions.

## Criterios de saida B0

- [ ] Missao, escopo, fora de escopo e perfil de resultado aprovados.
- [ ] Papeis e conflito de interesse registrados.
- [ ] Politica de neutralidade arquitetural aceita.
- [ ] Separacao core/submissions/sealed aceita.
- [ ] Politica de mudanca, versionamento e CHANGE-ID aceita.
- [ ] Politica de preregistro, auditoria e resultados negativos aceita.
- [ ] Responsaveis por B1 e mecanismo de aprovacao definidos.

## Decisoes pendentes

- Responsaveis nominais pelo conselho, engenharia, red team e auditoria.
- Licenca e politica de contribuicao.
- Mecanismo formal de preregistro.
- Controle de acesso e storage do repositorio sealed.
- Data e criterio para declarar B0 aprovado.
