# UC-G03-03 Solicitar Pré-Admissão

> Fluxo crítico completo do módulo G03 (exigência de ao menos um fluxo crítico por grupo, em `requisitos-entrega-av2.md`, E3).

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-03 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | MedicoRegulador |
| **Atores secundários** | Sistema de Leitos (G04), Sistema de Regulação (G01, dono da prioridade) |
| **Objetivo** | Solicitar a reserva antecipada de leito crítico, com os dados pré-hospitalares e a prioridade herdada da triagem |
| **Requisitos rastreados** | RF-G03-04, RF-G03-13, RNF-G03-07 |
| **Prioridade** | essencial |

## Pré-condições

- Despacho ativo e ficha aberta para o chamado.
- Ficha com ao menos um registro de sinais vitais (valores ou "não aferível" justificado).
- Nenhum pedido de pré-admissão ativo para o mesmo chamado.

## Pós-condições

- **Sucesso:** `PreAdmissao` gravada e enviada a G04 pelo contrato C3; retorno "reservado" registrado; ficha disponível para a EquipeReceptora.
- **Falha:** nenhuma reserva criada; o pedido fica registrado com o desfecho (`Negada` ou `Pendente de envio`) e o motivo; o médico regulador é alertado para decidir o desvio.

## Fluxo principal

1. O médico regulador seleciona o atendimento em curso na central.
2. O sistema exibe o resumo clínico da ficha (último registro de sinais vitais, procedimentos, fármacos) e registra o acesso (UC-G03-08, incluído).
3. O médico regulador define a necessidade de leito (`SALA_VERMELHA` ou `OBSERVACAO`).
4. O médico regulador informa ou confirma o ETA ao hospital estimado pela equipe.
5. O médico regulador confirma a solicitação.
6. O sistema valida a prioridade (UC-G03-05, incluído) e obtém a prioridade vigente do chamado.
7. O sistema monta o contrato C3 `pedido_pre_admissao`: `prontuario_id`, `chamado_id`, `prioridade` herdada, `necessidade`, último registro de `sinais_vitais` e `eta_hospital`.
8. O sistema envia o C3 a G04 e grava a `PreAdmissao` com horário de envio e desfecho `Enviada`.
9. G04 responde "reservado".
10. O sistema registra o desfecho `Reservada`, informa o médico regulador e deixa a ficha disponível para consulta da EquipeReceptora (UC-G03-06).

## Fluxos alternativos

### FA-01 Chamado reclassificado antes do envio

- **Condição:** G01 reclassificou o chamado (RN-02).
- **Passos:** 1. UC-G03-05 devolve a prioridade mais recente e o horário da classificação. 2. O sistema exibe ao médico regulador a prioridade que será usada. 3. O campo não é editável neste módulo.
- **Reconvergência:** retorna ao passo 7.

### FA-02 Último sinal vital antigo

- **Condição:** o último registro recebido da ficha é antigo (equipe pode estar sem conexão).
- **Passos:** 1. O sistema exibe o horário de coleta do último registro recebido. 2. O médico regulador decide enviar assim mesmo ou aguardar.
- **Reconvergência:** retorna ao passo 3.

### FA-03 Deterioração após o envio

- **Condição:** a equipe registra novos sinais vitais depois do envio.
- **Passos:** 1. O sistema grava os novos registros na ficha. 2. A EquipeReceptora os vê na consulta (UC-G03-06). 3. O C3 não é reemitido; uma mudança de necessidade depende da decisão Q-08 do README.
- **Reconvergência:** fim do fluxo.

## Fluxos de exceção

### FE-01 Ficha sem sinais vitais

- **Condição:** nenhum registro de sinais vitais (nem "não aferível" justificado).
- **Passos:** 1. O sistema bloqueia o envio. 2. O sistema orienta o registro via UC-G03-02.
- **Estado final:** nenhum pedido criado.

### FE-02 Prioridade indisponível

- **Condição:** chamado sem prioridade, valor inválido ou G01 sem resposta (falha em UC-G03-05).
- **Passos:** 1. O sistema não emite o pedido. 2. O sistema alerta o médico regulador. 3. O sistema não aceita prioridade digitada neste módulo (RN-02).
- **Estado final:** nenhum pedido criado; a reclassificação, se necessária, ocorre em G01.

### FE-03 Leito negado por G04

- **Condição:** G04 devolve `negado` com motivo (contrato C3).
- **Passos:** 1. O sistema registra o desfecho `Negada` com o motivo. 2. O sistema alerta o médico regulador. 3. O médico regulador decide o desvio (outro serviço ou teleorientação ampliada) e registra a decisão como justificativa na ficha (premissa P-07). 4. Se desejar, o médico regulador emite novo pedido, ligado ao anterior.
- **Estado final:** pedido `Negada` preservado; decisão registrada. O pedido negado entra no indicador "taxa de reserva negada" de G06.

### FE-04 Pedido duplicado

- **Condição:** já existe pedido ativo para o chamado.
- **Passos:** 1. O sistema impede o segundo pedido. 2. O sistema exibe o pedido existente e seu desfecho.
- **Estado final:** nenhum pedido novo criado.

### FE-05 G04 indisponível ou sem resposta

- **Condição:** falha de envio ou ausência de retorno.
- **Passos:** 1. O sistema grava o pedido como `Pendente de envio`. 2. O sistema alerta o médico regulador para contingência por canal fora do sistema. 3. O sistema reenvia o pedido quando G04 responder (idempotência, ver Q-09).
- **Estado final:** pedido pendente e visível; atendimento não bloqueado.

## Regras de negócio aplicadas

| Regra | Aplicação neste caso de uso |
| --- | --- |
| RN-02 | passo 6, FA-01 e FE-02: prioridade herdada, nunca recalculada nem digitada |
| RN-05 | FE-04: o módulo evita pedido duplicado; a unicidade da reserva é de G04 |
| RN-11 | passo 2: acesso à ficha restrito e registrado |
| RN-12 | passos 4 e 8: horários e ETA alimentam o tempo porta-leito |

## Relacionamentos

- `<<include>>` **UC-G03-05 Validar Prioridade**: obrigatório, porque sem a prioridade vigente o C3 é inválido e RN-02 seria violada.
- `<<include>>` **UC-G03-08 Controlar e Registrar Acesso ao Prontuário**: obrigatório, porque o resumo da ficha é dado clínico (RN-11).

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Chamado | `chamado_id`, `prioridade` vigente (somente leitura) | G01, por referência |
| Prontuario | `prontuario_id`, último registro de sinais vitais | este módulo |
| PreAdmissao | `necessidade`, `eta_hospital`, horário de envio, desfecho, motivo | este módulo |
| Leito/Reserva | resultado `reservado` ou `negado` com motivo | contrato C3 (G04) |

## Critérios de aceite

- [ ] A prioridade do C3 é igual à vigente no chamado e não é editável no módulo.
- [ ] O C3 só é enviado com `necessidade`, `eta_hospital` e último sinal vital.
- [ ] Cada pedido e seu desfecho (reservado, negado, pendente) ficam registrados e contáveis.
- [ ] Não existem dois pedidos ativos para o mesmo chamado.
- [ ] Pedido negado exibe o motivo e permite novo pedido ligado ao anterior.
- [ ] Falha de G04 não bloqueia o atendimento e deixa o pedido visível como pendente.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-04 | `PreAdmissao` | pendente (M2) | pendente (M3) |
| RF-G03-13 | `PreAdmissao` | pendente (M2) | pendente (M3) |
