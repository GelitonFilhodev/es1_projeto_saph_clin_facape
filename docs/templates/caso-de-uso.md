# UC-G0X-NN — Nome do Caso de Uso

> Template. Copie para `grupos/grupo-XX-*/casos-de-uso/uc-XX-NN-nome.md`.
> Apague as instruções em itálico antes de entregar.

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G0X-NN |
| **Módulo** | G0X — nome do subprocesso |
| **Ator primário** | *ex.: MedicoRegulador* |
| **Atores secundários** | *ex.: Sistema de Leitos (G4)* |
| **Objetivo** | *o que o ator quer alcançar, em uma frase* |
| **Requisitos rastreados** | RF-G0X-NN, RF-G0X-NN |
| **Prioridade** | essencial / importante / desejável |

## Pré-condições

- *estado do sistema antes do início (ex.: chamado com prioridade definida)*

## Pós-condições

- **Sucesso:** *estado observável ao final*
- **Falha:** *estado quando o fluxo principal não se completa*

## Fluxo principal

1. O ator *ação objetiva no sistema*.
2. O sistema *resposta verificável*.
3. ...

> Escreva no presente do indicativo, uma ação por passo, sem detalhe de interface.

## Fluxos alternativos

### FA-01 — *nome do desvio*

- **Condição:** *quando ocorre*
- **Passos:** 1. ... 2. ...
- **Reconvergência:** retorna ao passo *N* do fluxo principal.

## Fluxos de exceção

### FE-01 — *nome da falha*

- **Condição:** *ex.: leito indisponível*
- **Passos:** 1. ... 2. ...
- **Estado final:** *o que fica registrado e com qual status*

## Regras de negócio aplicadas

| Regra | Descrição |
| --- | --- |
| RN-XX | *regra do contexto-do-sistema.md ou derivada (com fonte)* |

## Relacionamentos

- `<<include>>` *UC-G0X-NN* — obrigatório porque *justificativa*.
- `<<extend>>` *UC-G0X-NN* — opcional porque *justificativa e condição de extensão*.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Chamado | `prioridade` | G1 |

## Critérios de aceite

- [ ] *condição verificável 1*
- [ ] *condição verificável 2*

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G0X-NN | *Classe* | DS-G0X-NN | CT-G0X-NN |
