# Matriz de Rastreabilidade — G03

> Preencha conforme o modelo em `docs/templates/matriz-rastreabilidade.md`.
> Célula vazia é pendência: use `pendente` explicitamente.

## Requisitos funcionais

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G03-01 | Registrar teleorientação com autor, horário e destinatário | UC-G03-01 | | | | pendente |
| RF-G03-02 | Registrar sinais vitais em campo com horário de coleta | UC-G03-02 | | | | pendente |
| RF-G03-03 | Registrar procedimentos e fármacos administrados | UC-G03-02 | | | | pendente |
| RF-G03-04 | Emitir pedido de pré-admissão com prioridade herdada da triagem | UC-G03-03 | | | | pendente |
| RF-G03-05 | Registrar recusa de atendimento com assinatura e testemunha (RN-10) | UC-G03-04 | | | | pendente |
| RF-G03-06 | Manter ficha disponível sem conexão e sincronizar depois | UC-G03-02 | | | | pendente |
| RF-G03-07 | Restringir acesso à ficha por perfil e registrar cada acesso | UC-G03-02 | | | | pendente |
| RF-G03-08 | Publicar eventos `TELEORIENTACAO_REGISTRADA` e `PRONTUARIO_ACESSADO` | UC-G03-01 | | | | pendente |

## Requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G03-01 | Ficha sincronizada em ≤ 5 s após reconexão | | pendente |
| RNF-G03-02 | Nenhum dado clínico perdido em queda de conexão durante o registro | | pendente |
| RNF-G03-03 | Dado clínico criptografado em repouso (LGPD) | | pendente |
| RNF-G03-04 | Ficha utilizável em tablet com uma mão, alvos de toque ≥ 44 px | | pendente |
| RNF-G03-05 | Telessaúde aderente à Res. CFM 2.314/2022 | | pendente |

## Contratos consumidos

| Contrato | Origem | Campo crítico |
| --- | --- | --- |
| — | Contrato C2 `despacho_ativo` (G2) | — |

## Contratos fornecidos

| Contrato | Destino | Campo crítico |
| --- | --- | --- |
| — | Contrato C3 `pedido_pre_admissao` (G4) e C4 `consumo_farmaco` (G5) | — |

## Pendências

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| | | |
