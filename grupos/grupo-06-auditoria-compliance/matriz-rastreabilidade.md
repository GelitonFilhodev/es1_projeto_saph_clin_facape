# Matriz de Rastreabilidade — G06

> Preencha conforme o modelo em `docs/templates/matriz-rastreabilidade.md`.
> Célula vazia é pendência: use `pendente` explicitamente.

## Requisitos funcionais

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G06-01 | Registrar evento imutável com ator, entidade, horário e resultado | UC-G06-01 | | | | pendente |
| RF-G06-02 | Rejeitar qualquer alteração ou exclusão de evento registrado | UC-G06-01 | | | | pendente |
| RF-G06-03 | Consultar trilha por chamado, ator e período | UC-G06-02 | | | | pendente |
| RF-G06-04 | Assinar digitalmente condutas excepcionais e recusas | UC-G06-03 | | | | pendente |
| RF-G06-05 | Calcular tempo de resposta e tempo porta-leito (RN-12) | UC-G06-04 | | | | pendente |
| RF-G06-06 | Registrar todo acesso a prontuário como evento sensível (LGPD) | UC-G06-05 | | | | pendente |
| RF-G06-07 | Emitir alerta de divergência de estoque e de reserva negada | UC-G06-04 | | | | pendente |
| RF-G06-08 | Garantir idempotência por `evento_id` no reenvio | UC-G06-01 | | | | pendente |

## Requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G06-01 | Consulta de trilha de 30 dias em ≤ 5 s | | pendente |
| RNF-G06-02 | Evento gravado não pode ser alterado por nenhum perfil | | pendente |
| RNF-G06-03 | Retenção mínima de 5 anos para eventos sensíveis | | pendente |
| RNF-G06-04 | Indicadores atualizados em janela de 15 min | | pendente |
| RNF-G06-05 | Acesso a dado sensível auditável e minimizado (LGPD art. 6º) | | pendente |

## Contratos consumidos

| Contrato | Origem | Campo crítico |
| --- | --- | --- |
| — | Contrato C5 `evento_sensivel` (G1 a G5) | — |

## Contratos fornecidos

| Contrato | Destino | Campo crítico |
| --- | --- | --- |
| — | Trilha imutável, relatórios e alertas de conformidade | — |

## Pendências

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| | | |
