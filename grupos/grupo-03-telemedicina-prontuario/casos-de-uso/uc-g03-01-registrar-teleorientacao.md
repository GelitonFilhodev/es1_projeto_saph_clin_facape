# UC-G03-01 Registrar Teleorientação

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-01 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | MedicoRegulador |
| **Atores secundários** | Sistema de Despacho (G02, origem do contrato C2), Sistema de Auditoria (G06) |
| **Objetivo** | Registrar a orientação dada a distância ao socorrista ou ao acompanhante enquanto a viatura se desloca ou atende no local |
| **Requisitos rastreados** | RF-G03-01, RF-G03-08 (evento `TELEORIENTACAO_REGISTRADA`), RNF-G03-05 |
| **Prioridade** | essencial |

## Pré-condições

- Chamado com despacho ativo (contrato C2 `despacho_ativo`, de G02).
- MedicoRegulador autenticado, com perfil de regulação.

## Pós-condições

- **Sucesso:** `Teleorientacao` gravada com autor, horário do fato, horário do registro, destinatário e conteúdo, vinculada a `chamado_id` e `despacho_id`; evento `TELEORIENTACAO_REGISTRADA` publicado a G06.
- **Falha:** nenhuma teleorientação gravada; o motivo da recusa do sistema é exibido ao médico regulador.

## Fluxo principal

1. O médico regulador seleciona, na central de regulação, o chamado com despacho ativo.
2. O sistema exibe os dados operacionais do chamado: prioridade vigente, queixa principal, viatura e equipe.
3. O médico regulador informa o destinatário da orientação (socorrista da equipe ou acompanhante).
4. O médico regulador informa o conteúdo da orientação e o horário em que ela foi dada.
5. O médico regulador confirma o registro.
6. O sistema grava a teleorientação com autor, horário do fato e horário do registro, vinculada ao chamado e ao despacho.
7. O sistema publica o evento `TELEORIENTACAO_REGISTRADA` (contrato C5) a G06.
8. O sistema confirma o registro ao médico regulador.

## Fluxos alternativos

### FA-01 Registro posterior ao fato

- **Condição:** a orientação foi dada por voz e o médico regulador registra depois.
- **Passos:** 1. O médico regulador informa o horário real da orientação no passo 4. 2. O sistema mantém os dois horários (fato e registro) sem sobrescrever nenhum.
- **Reconvergência:** retorna ao passo 5 do fluxo principal.

### FA-02 Destinatário é acompanhante sem cadastro

- **Condição:** quem recebe a orientação é um acompanhante ou solicitante.
- **Passos:** 1. O médico regulador informa apenas o nome e a relação com o paciente, em texto. 2. O sistema não cria cadastro de pessoa (minimização de dados, LGPD).
- **Reconvergência:** retorna ao passo 4 do fluxo principal.

## Fluxos de exceção

### FE-01 Despacho não ativo

- **Condição:** o chamado não tem despacho ativo ou o despacho já foi encerrado.
- **Passos:** 1. O sistema impede o registro. 2. O sistema informa o estado do chamado e do despacho.
- **Estado final:** nada gravado. O caso "chamado sem viatura" depende da decisão Q-01 do README.

### FE-02 Dado obrigatório ausente

- **Condição:** destinatário, conteúdo ou horário não informados.
- **Passos:** 1. O sistema bloqueia a confirmação. 2. O sistema destaca os campos pendentes.
- **Estado final:** nada gravado.

### FE-03 G06 indisponível

- **Condição:** falha na publicação do evento.
- **Passos:** 1. O sistema mantém a teleorientação gravada. 2. O evento fica pendente e é reentregue com o mesmo `evento_id` (idempotência).
- **Estado final:** teleorientação registrada; evento pendente. O atendimento não é bloqueado.

## Regras de negócio aplicadas

| Regra | Aplicação neste caso de uso |
| --- | --- |
| RN-09 | passo 7: conduta médica a distância gera evento imutável (autor, ação, entidade, horário) |
| RN-11 | o registro só é criado por perfil com necessidade de atendimento (MedicoRegulador) |
| Res. CFM 2.314/2022 | passo 6: o ato de telemedicina consta de registro em prontuário, com integridade e irrefutabilidade |
| Lei 14.510/2022 | consentimento do paciente para telessaúde: como registrá-lo em emergência é a pergunta Q-10 do README |

## Relacionamentos

- Sem `<<include>>` ou `<<extend>>`. O registro é independente do preenchimento da ficha em campo e não depende dele para ocorrer.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Chamado | `chamado_id`, prioridade vigente (somente leitura) | G01, referenciado por identificador |
| Despacho | `despacho_id`, `viatura_id`, `equipe_id` | contrato C2 (G02) |
| Teleorientacao | autor, horário do fato, horário do registro, destinatário, conteúdo | este módulo |

## Critérios de aceite

- [ ] Nenhuma teleorientação é gravada sem autor, horário, destinatário e conteúdo.
- [ ] Toda teleorientação referencia um chamado com despacho ativo.
- [ ] Horário do fato e horário do registro são guardados separadamente.
- [ ] Cada registro gera um evento `TELEORIENTACAO_REGISTRADA` com `evento_id` único.
- [ ] Falha de G06 não impede o registro nem o atendimento.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-01 | `Teleorientacao` | pendente (M2) | pendente (M3) |
| RF-G03-08 | `Teleorientacao` | pendente (M2) | pendente (M3) |
