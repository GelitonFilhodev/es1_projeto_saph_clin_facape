# UC-G03-08 Controlar e Registrar Acesso ao Prontuário

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-08 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | nenhum humano (acionado por UC-G03-02, UC-G03-03 e UC-G03-06 por `<<include>>`) |
| **Atores secundários** | Sistema de Auditoria (G06) |
| **Objetivo** | Decidir se o perfil pode acessar a ficha e registrar cada acesso, permitido ou negado |
| **Requisitos rastreados** | RF-G03-07, RF-G03-10, RF-G03-08 (evento `PRONTUARIO_ACESSADO`), RNF-G03-03, RNF-G03-06 |
| **Prioridade** | essencial |

## Pré-condições

- Usuário autenticado tenta abrir ou alterar a ficha.

## Pós-condições

- **Sucesso:** acesso autorizado ou negado e registrado; evento `PRONTUARIO_ACESSADO` publicado a G06.
- **Falha:** o registro do acesso fica pendente e é reentregue.

## Fluxo principal

1. O sistema recebe o usuário (`ator_id`, `papel`), a ficha (`prontuario_id`) e o tipo de acesso (`LEITURA` ou `ALTERACAO`).
2. O sistema verifica se o perfil tem necessidade de atendimento para a ficha.
3. O sistema grava o registro de acesso com horário e resultado.
4. O sistema publica `PRONTUARIO_ACESSADO` (contrato C5, tipo `ACESSO`) com `evento_id` único.
5. O sistema devolve a autorização ao caso de uso chamador.

## Perfis com necessidade de atendimento (premissa P-06)

| Perfil | Acesso |
| --- | --- |
| MedicoRegulador | atendimentos que regula |
| EquipeIntervencao | ficha do próprio despacho |
| EquipeReceptora | atendimentos com pré-admissão para o hospital |
| Auditor | sem acesso ao conteúdo clínico; consulta só a trilha de acessos em G06 |

## Fluxos alternativos

### FA-01 Acesso offline no tablet

- **Condição:** sem conexão.
- **Passos:** 1. O registro de acesso é gravado localmente. 2. UC-G03-07 o sincroniza depois.
- **Reconvergência:** retorna ao passo 5.

## Fluxos de exceção

### FE-01 Perfil sem necessidade

- **Condição:** o perfil não consta na tabela acima para esta ficha.
- **Passos:** 1. O sistema nega o acesso. 2. O sistema registra a tentativa com resultado `NEGADO`.
- **Estado final:** nenhum conteúdo exibido.

### FE-02 G06 indisponível

- **Condição:** falha na publicação.
- **Passos:** 1. O acesso permitido continua, por continuidade do atendimento. 2. O evento fica pendente e é reentregue com o mesmo `evento_id`.
- **Estado final:** acesso registrado localmente; evento pendente (candidata a ADR no M2).

## Regras de negócio aplicadas

| Regra | Aplicação |
| --- | --- |
| RN-11 | passo 2: só papel com necessidade de atendimento |
| RN-09 | passo 4: acesso sensível gera evento imutável |
| LGPD art. 37 | registro das operações de tratamento de dados |

## Relacionamentos

- Incluído por **UC-G03-02**, **UC-G03-03** e **UC-G03-06** (`<<include>>`): reaproveita a mesma regra de acesso e de evento em três casos de uso.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Registro de acesso | `ator_id`, `papel`, `prontuario_id`, tipo, horário, resultado | este módulo (evento para G06) |

## Critérios de aceite

- [ ] Cada acesso, permitido ou negado, gera um evento com `evento_id` único.
- [ ] Perfil sem necessidade recebe negação e a tentativa é registrada.
- [ ] Falha de G06 não bloqueia o atendimento e não perde o evento.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-07 | `Prontuario` | pendente (M2) | pendente (M3) |
| RF-G03-10 | `Prontuario` | pendente (M2) | pendente (M3) |
| RF-G03-08 | `Prontuario` | pendente (M2) | pendente (M3) |
