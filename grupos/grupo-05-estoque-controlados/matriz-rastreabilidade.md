# Matriz de Rastreabilidade — G05

> Preencha conforme o modelo em `docs/templates/matriz-rastreabilidade.md`.
> Célula vazia é pendência: use `pendente` explicitamente.

## Requisitos funcionais

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G05-01 | Controlar estoque por item, lote e validade | UC-G05-01 | | | | pendente |
| RF-G05-02 | Registrar dispensação com autor e vínculo ao prontuário | UC-G05-02 | | | | pendente |
| RF-G05-03 | Bloquear dispensação de lote vencido ou travado (RN-08) | UC-G05-02 | | | | pendente |
| RF-G05-04 | Exigir autorização farmacêutica para controlado (RN-07) | UC-G05-02 | | | | pendente |
| RF-G05-05 | Gerar solicitação de reposição após consumo | UC-G05-03 | | | | pendente |
| RF-G05-06 | Apontar divergência entre consumo registrado e estoque | UC-G05-05 | | | | pendente |
| RF-G05-07 | Travessar item sob suspeita sanitária com motivo | UC-G05-04 | | | | pendente |
| RF-G05-08 | Publicar eventos `CONTROLADO_DISPENSADO` e `ITEM_TRAVADO` | UC-G05-02 | | | | pendente |

## Requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G05-01 | Baixa de controlado registrada em ≤ 3 s em campo | | pendente |
| RNF-G05-02 | Rastreabilidade lote → paciente → profissional preservada | | pendente |
| RNF-G05-03 | Nenhuma dispensação sem autorização registrada | | pendente |
| RNF-G05-04 | Alerta de vencimento com 30 dias de antecedência | | pendente |
| RNF-G05-05 | Dados aderentes à Portaria SVS/MS 344/1998 e RDC 22/2014 | | pendente |

## Contratos consumidos

| Contrato | Origem | Campo crítico |
| --- | --- | --- |
| — | Contrato C4 `consumo_farmaco` (G3) | — |

## Contratos fornecidos

| Contrato | Destino | Campo crítico |
| --- | --- | --- |
| — | Baixa por lote, solicitação de reposição e trava de item | — |

## Pendências

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| | | |
