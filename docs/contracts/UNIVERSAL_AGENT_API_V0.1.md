# Contrato universal de agente v0.1

Status: `B2 CONTRACT CANDIDATE - 2026-09-02`

CHANGE-ID: `CHG-2026-09-02-B2-UNIVERSAL-API`

## Objetivo

Definir a fronteira black-box minima entre benchmark e agente sem exigir framework, algoritmo, modulo interno ou representacao especifica. O contrato descreve apenas comportamento observavel e metadados necessarios para executar e auditar uma implementacao.

## Lifecycle

Todo agente implementa:

```python
reset(specification) -> None
observe(observation) -> None
act() -> action | AgentDecision
learn(transition) -> None
save() -> state
load(state) -> None
```

Ordem por episodio:

1. validar manifest e specification;
2. criar uma instancia nova do agente;
3. chamar `reset` exatamente uma vez;
4. para cada passo, chamar `observe`, `act`, validar a acao e executar o ambiente;
5. chamar `learn` somente quando `online_learning=True`;
6. encerrar em termination, truncation, budget, erro ou timeout.

Agentes sem aprendizagem online, persistencia ou incerteza mantem os metodos da interface como no-op quando aplicavel e declaram as capabilities como `False`.

## Specification

`AgentSpecification` contem somente:

- `observation_space`: descritor opaco, publico e nao nulo;
- `action_space`: descritor opaco, publico e nao nulo;
- `seed`: inteiro nao negativo e nao booleano;
- `capabilities`: flags booleanas.

O core nao interpreta nem extrai features dos espacos. Limites semanticos da acao pertencem ao ambiente e ao `action_validator`.

## Capabilities opcionais

- `online_learning`: autoriza entrega de `Transition` apos a resposta do ambiente.
- `persistence`: exige que `save` produza estado serializavel e que `load` o aceite.
- `uncertainty`: exige que `act` retorne `AgentDecision(action, confidence)`, com confianca finita em `[0, 1]`. Sem essa capability, confianca nao pode ser fornecida. Ausencia da capability gera `NOT_SUPPORTED` em C10, nao falha geral.

As capabilities do manifest e da specification devem ser identicas para a execucao. Divergencia falha antes do run.

## Manifest

O formato JSON e definido por `schemas/agent_manifest.schema.json`. O loader rejeita campos ausentes, desconhecidos, dependencias vazias/duplicadas, tipos de capability incorretos, timeout nao positivo e hashes fora do formato permitido.

Sentinelas `not-applicable` e `not-provided` existem para controles publicos e fases anteriores a B16. Uma submissao futura podera impor hashes reais por politica adicional sem alterar a interface comportamental.

## Determinismo e seeds

O mesmo factory, specification, seed e observacao publica devem produzir a mesma primeira decisao quando o protocolo exigir determinismo. A checagem nao autoriza acesso a seeds seladas e nao afirma determinismo de hardware externo.

## Erros observaveis

- contrato/metadado invalido: `AgentProtocolError` antes da execucao;
- acao fora dos limites do ambiente: `INVALID_ACTION`;
- timeout: `TIMEOUT` com terminacao do processo;
- excecao interna ou saida invalida: `ERROR` sem reinterpretar como resultado cientifico;
- budget sem termination: `MAX_STEPS`.

## Regra de adapters

O adapter pode converter dtype, unidade, shape, serializacao, enum ou nomenclatura equivalente. Nao pode extrair features, adicionar memoria, selecionar informacao semanticamente, acessar ground truth, inserir hints ou corrigir a acao. Auditoria executavel de adapters pertence a B9/B16.

## Compatibilidade

Alteracao em lifecycle, significado de capability, envelope de acao ou regra de adapter exige CHANGE-ID e revisao do gate correspondente. O contrato v0.1 e pre-release e nao autoriza candidatos.
