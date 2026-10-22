# Matriz de Rastreabilidade — G02

> Preencha conforme o modelo em `docs/templates/matriz-rastreabilidade.md`.
> Célula vazia é pendência: use `pendente` explicitamente.

## Requisitos funcionais

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G02-01 | Selecionar viatura compatível com a prioridade clínica | UC-G02-01 | | | | pendente |
| RF-G02-02 | Impedir dupla alocação da mesma viatura (RN-04) | UC-G02-01 | | | | pendente |
| RF-G02-03 | Exigir equipe de suporte avançado completo para despachar USA (RN-03) | UC-G02-01 | | | | pendente |
| RF-G02-04 | Registrar justificativa do despacho escolhido | UC-G02-01 | | | | pendente |
| RF-G02-05 | Acionar suporte avançado durante atendimento em curso | UC-G02-02 | | | | pendente |
| RF-G02-06 | Rastrear estados da viatura em tempo real | UC-G02-04 | | | | pendente |
| RF-G02-07 | Devolver chamado à fila quando não houver viatura compatível | UC-G02-01 | | | | pendente |
| RF-G02-08 | Publicar evento `VIATURA_DESPACHADA` para G6 | UC-G02-01 | | | | pendente |

## Requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G02-01 | Despacho concluído em ≤ 120 s após classificação | | pendente |
| RNF-G02-02 | Estimativa de chegada atualizada a cada 2 min | | pendente |
| RNF-G02-03 | Estado da viatura consistente entre despachos concorrentes | | pendente |
| RNF-G02-04 | Painel legível em tablet de campo sob luz solar | | pendente |
| RNF-G02-05 | Histórico de despacho retido por 5 anos para auditoria | | pendente |

## Contratos consumidos

| Contrato | Origem | Campo crítico |
| --- | --- | --- |
| — | Contrato C1 `chamado_classificado` (G1) | — |

## Contratos fornecidos

| Contrato | Destino | Campo crítico |
| --- | --- | --- |
| — | Contrato C2 `despacho_ativo` para G3 | — |

## Pendências

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| | | |
