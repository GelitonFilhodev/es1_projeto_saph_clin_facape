# UC-G03-06 Consultar Ficha Pré-Hospitalar

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-06 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | EquipeReceptora |
| **Atores secundários** | MedicoRegulador (também consulta), Sistema de Auditoria (G06) |
| **Objetivo** | Ler a ficha em modo somente leitura para preparar o recebimento do paciente (passagem de plantão digital) |
| **Requisitos rastreados** | RF-G03-07, RF-G03-10, RF-G03-14 |
| **Prioridade** | essencial |

## Pré-condições

- Existe pedido de pré-admissão emitido para o atendimento (para a EquipeReceptora).
- Usuário autenticado.

## Pós-condições

- **Sucesso:** ficha exibida em leitura; acesso registrado com evento `PRONTUARIO_ACESSADO`.
- **Falha:** nenhum conteúdo exibido; tentativa registrada com resultado `NEGADO`.

## Fluxo principal

1. O usuário seleciona o atendimento na lista de pacientes a caminho (EquipeReceptora) ou na central (MedicoRegulador).
2. O sistema verifica o perfil e a necessidade de atendimento (RN-11) e registra o acesso (UC-G03-08, incluído).
3. O sistema exibe a ficha em leitura: sinais vitais (histórico e último), procedimentos, fármacos, teleorientações, recusa (se houver) e o pedido de pré-admissão com o desfecho.

## Fluxos alternativos

### FA-01 Dados possivelmente defasados

- **Condição:** a equipe de campo pode estar sem conexão.
- **Passos:** 1. O sistema exibe o horário do último registro recebido. 2. O usuário considera a defasagem.
- **Reconvergência:** fim do fluxo.

## Fluxos de exceção

### FE-01 Perfil sem necessidade de atendimento

- **Condição:** o usuário não tem papel ou vínculo com o atendimento.
- **Passos:** 1. O sistema nega o acesso. 2. O sistema registra a tentativa (UC-G03-08).
- **Estado final:** nada exibido.

### FE-02 Falha do registro de acesso

- **Condição:** G06 indisponível.
- **Passos:** 1. O sistema mantém o acesso permitido, por continuidade do atendimento. 2. O evento fica pendente e é reentregue (arquitetura modular, seção 6).
- **Estado final:** acesso concedido; evento pendente.

## Regras de negócio aplicadas

| Regra | Aplicação |
| --- | --- |
| RN-11 | passo 2: só papel com necessidade de atendimento |
| RN-09 | passo 2: o acesso gera evento |

## Relacionamentos

- `<<include>>` **UC-G03-08**: obrigatório, porque toda leitura de dado clínico exige verificação e evento.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Prontuario e registros | conteúdo da ficha (somente leitura) | este módulo |
| PreAdmissao | pedido e desfecho | este módulo |

## Critérios de aceite

- [ ] A consulta é somente leitura.
- [ ] Perfis sem necessidade (por exemplo, Auditor) não veem conteúdo clínico (premissa P-06).
- [ ] Cada consulta, permitida ou negada, gera evento.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-07 | `Prontuario` | pendente (M2) | pendente (M3) |
| RF-G03-10 | `Prontuario` | pendente (M2) | pendente (M3) |
| RF-G03-14 | `Prontuario` | pendente (M2) | pendente (M3) |
