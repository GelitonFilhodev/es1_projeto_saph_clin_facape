# Matriz de Rastreabilidade — G04

> Preencha conforme o modelo em `docs/templates/matriz-rastreabilidade.md`.
> Célula vazia é pendência: use `pendente` explicitamente.

## Requisitos funcionais

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G04-01 | Manter estado explícito de cada leito (vago, reservado, ocupado, em higienização, bloqueado) | UC-G04-01 | | | | pendente |
| RF-G04-02 | Reservar leito vinculado ao chamado e ao prontuário | UC-G04-02 | | | | pendente |
| RF-G04-03 | Impedir duas reservas ativas no mesmo leito (RN-05) | UC-G04-02 | | | | pendente |
| RF-G04-04 | Expirar reserva não confirmada após o prazo do ETA | UC-G04-05 | | | | pendente |
| RF-G04-05 | Bloquear leito com motivo obrigatório e autor | UC-G04-03 | | | | pendente |
| RF-G04-06 | Não ofertar leito em higienização ou bloqueado (RN-06) | UC-G04-01 | | | | pendente |
| RF-G04-07 | Alertar equipe receptora no aceite da reserva | UC-G04-02 | | | | pendente |
| RF-G04-08 | Publicar eventos `LEITO_RESERVADO` e `LEITO_NEGADO` | UC-G04-02 | | | | pendente |

## Requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G04-01 | Reserva confirmada em ≤ 2 s no pico de 20 req/min | | pendente |
| RNF-G04-02 | Zero reserva dupla em qualquer cenário de concorrência | | pendente |
| RNF-G04-03 | Painel de leitos com defasagem máxima de 30 s | | pendente |
| RNF-G04-04 | Bloqueio sanitário visível em todos os pontos de consulta | | pendente |
| RNF-G04-05 | Histórico de ocupação disponível para indicadores (G6) | | pendente |

## Contratos consumidos

| Contrato | Origem | Campo crítico |
| --- | --- | --- |
| — | Contrato C3 `pedido_pre_admissao` (G3) | — |

## Contratos fornecidos

| Contrato | Destino | Campo crítico |
| --- | --- | --- |
| — | Reserva ativa + alerta à equipe receptora | — |

## Pendências

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| | | |
