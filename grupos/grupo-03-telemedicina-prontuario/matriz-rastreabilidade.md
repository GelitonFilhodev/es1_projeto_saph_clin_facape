# Matriz de Rastreabilidade: G03

> Segue o modelo de `docs/templates/matriz-rastreabilidade.md`. No M1 as colunas Classe, Sequência e Caso de teste ainda não existem; ficam marcadas como `pendente` e serão preenchidas no M2 e no M3.

## Requisitos funcionais

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G03-01 | Registrar teleorientação | UC-G03-01 | `Teleorientacao` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-02 | Registrar sinais vitais | UC-G03-02 | `RegistroSinaisVitais` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-03 | Registrar procedimentos | UC-G03-02 | `Procedimento` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-04 | Emitir pedido de pré-admissão com prioridade herdada | UC-G03-03, UC-G03-05 | `PreAdmissao` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-05 | Registrar recusa com assinatura e testemunha | UC-G03-04 | `RecusaAtendimento` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-06 | Ficha disponível sem conexão | UC-G03-02, UC-G03-04, UC-G03-07 | `Prontuario` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-07 | Restringir acesso por perfil | UC-G03-08, UC-G03-02, UC-G03-06 | `Prontuario` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-08 | Publicar eventos a G06 | UC-G03-01, UC-G03-04, UC-G03-08 | `Teleorientacao`, `RecusaAtendimento` (candidatas) | pendente | pendente | UC definido (M1) |
| RF-G03-09 | Registrar fármacos administrados | UC-G03-02 | `ConsumoFarmaco` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-10 | Registrar cada acesso à ficha | UC-G03-08, UC-G03-06 | `Prontuario` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-11 | Sincronizar na reconexão sem duplicar | UC-G03-07 | `Prontuario` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-12 | Publicar consumo a G05 (C4) | UC-G03-02 | `ConsumoFarmaco` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-13 | Registrar retorno de G04 ao pedido | UC-G03-03 | `PreAdmissao` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-14 | Consultar ficha (passagem de plantão digital) | UC-G03-06 | `Prontuario` (candidata) | pendente | pendente | UC definido (M1) |
| RF-G03-15 | Corrigir registro preservando o original | UC-G03-02 | `Prontuario` (candidata) | pendente | pendente | UC definido (M1) |

## Requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G03-01 | Sincronização em até 5 s (p95) com até 30 registros pendentes | CT de fronteira (UC-G03-07) | pendente |
| RNF-G03-02 | 0 (zero) registros perdidos em queda de conexão | CT de queda em cada etapa (UC-G03-02, UC-G03-07) | pendente |
| RNF-G03-03 | 100% dos campos protegidos criptografados em repouso | inspeção do dicionário de dados (E4) | pendente |
| RNF-G03-04 | Alvos de toque de pelo menos 44 px | inspeção dos wireframes (E7) | pendente |
| RNF-G03-05 | 100% das teleorientações com autor (nome e CRM), horário e vínculo | checklist nos CT de UC-G03-01 | pendente |
| RNF-G03-06 | Bloqueio de sessão em até 2 min de inatividade | CT de sessão ociosa | pendente |
| RNF-G03-07 | Pedido disponível a G04 em até 3 s a 20 pedidos por minuto | CT de fronteira (UC-G03-03) | pendente |
| RNF-G03-08 | Registro de sinais vitais em até 45 s | teste com protótipo (E7) | pendente |

## Contratos consumidos

| Contrato | Origem | Uso no módulo | Campo crítico |
| --- | --- | --- | --- |
| C2 `despacho_ativo` | G02 | abre a ficha e habilita UC-G03-01 e UC-G03-02 | `despacho_id`, `chamado_id`, `equipe_id` |
| Consulta de prioridade vigente (por referência a `chamado_id`) | G01 | UC-G03-05 | `prioridade` (ver Q-02) |
| Retorno do C3 (`reservado` ou `negado`) | G04 | UC-G03-03 | motivo da negativa |

## Contratos fornecidos

| Contrato | Destino | Campo crítico | Estabilidade |
| --- | --- | --- | --- |
| C3 `pedido_pre_admissao` | G04 | `prioridade`, `necessidade`, `eta_hospital` | em discussão (Q-03, Q-08, Q-09) |
| C4 `consumo_farmaco` | G05 | `lote`, `item_id`, `quantidade` | estável |
| C5 `evento_sensivel` | G06 | `evento_id`, `tipo`, `resultado` | estável |

## Rastreio a indicadores de G06 (bônus)

| RF | Indicador de G06 | Como o requisito alimenta o indicador |
| --- | --- | --- |
| RF-G03-13 | Taxa de reserva negada | cada pedido e seu desfecho ficam registrados e contáveis |
| RF-G03-04 | Tempo porta-leito | horário de envio do pedido e ETA ao hospital |
| RF-G03-01 | Tempo de resposta | horário do fato da teleorientação |
| RF-G03-10 | Auditoria de acesso a prontuário | cada acesso gera evento `PRONTUARIO_ACESSADO` |

## Pendências

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| Perguntas Q-01 a Q-10 do README | decidem contratos C2 e C3 e a recusa | antes do M2 |
| Definir classes, atributos e multiplicidades (E4) | habilita a coluna Classe | M2 |
| Diagramas de sequência e máquina de estados da PreAdmissao (E5) | habilita a coluna Sequência | M2 |
| Casos de teste, incluindo um de fronteira (E6) | habilita a coluna Caso de teste | M3 |
