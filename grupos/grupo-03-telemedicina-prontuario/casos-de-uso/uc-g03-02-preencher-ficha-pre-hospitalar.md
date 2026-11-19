# UC-G03-02 Preencher Ficha Pré-Hospitalar

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-02 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | EquipeIntervencao |
| **Atores secundários** | Sistema de Despacho (G02, origem do C2), Sistema de Estoque (G05, destino do C4), Sistema de Auditoria (G06) |
| **Objetivo** | Registrar em campo o quadro clínico: sinais vitais, procedimentos e fármacos administrados |
| **Requisitos rastreados** | RF-G03-02, RF-G03-03, RF-G03-06, RF-G03-07, RF-G03-09, RF-G03-12, RF-G03-15, RNF-G03-01 a RNF-G03-04, RNF-G03-06, RNF-G03-08 |
| **Prioridade** | essencial |

## Pontos de extensão

- **PE-1 Recusa do paciente:** estendido por UC-G03-04.
- **PE-2 Conexão indisponível:** estendido por UC-G03-07.

## Pré-condições

- Despacho ativo (contrato C2) com equipe vinculada.
- Ficha (`Prontuario`) aberta pelo sistema ao receber o C2.
- Usuário autenticado, integrante da equipe do despacho.

## Pós-condições

- **Sucesso:** registros gravados com autor e horário de coleta, histórico preservado; consumo de fármaco publicado a G05 (C4); acesso registrado.
- **Falha:** dados já digitados ficam preservados no dispositivo; nenhum dado clínico é perdido (RNF-G03-02).

## Fluxo principal

1. A equipe de intervenção abre a ficha do atendimento no tablet.
2. O sistema verifica o perfil do usuário e registra o acesso (UC-G03-08, incluído).
3. O sistema exibe a ficha com os registros existentes.
4. A equipe registra um conjunto de sinais vitais com o horário de coleta.
5. O sistema valida o formato e os limites de entrada dos campos (proteção contra erro de digitação, sem interpretação clínica) e grava o registro com autor e horário de coleta.
6. A equipe registra os procedimentos realizados (tipo, horário e executor).
7. A equipe registra cada fármaco administrado (item da maleta, lote, quantidade, via, horário e responsável).
8. O sistema grava o consumo e publica o contrato C4 `consumo_farmaco` a G05.
9. A equipe repete os passos 4 a 7 conforme a evolução do atendimento.
10. O sistema confirma a gravação de cada registro somente depois de gravá-lo no armazenamento do dispositivo.

## Fluxos alternativos

### FA-01 Sinal vital não aferível

- **Condição:** a equipe não consegue aferir um parâmetro (por exemplo, em parada cardiorrespiratória).
- **Passos:** 1. A equipe marca o parâmetro como "não aferível". 2. A equipe informa a justificativa. 3. O sistema grava o valor como ausente justificado.
- **Reconvergência:** retorna ao passo 6 do fluxo principal.

### FA-02 Correção de registro

- **Condição:** a equipe identifica erro em um registro já gravado.
- **Passos:** 1. A equipe seleciona o registro e informa o valor correto e a justificativa. 2. O sistema mantém o registro original e grava uma nova versão com autor e horário (RF-G03-15).
- **Reconvergência:** retorna ao passo 9 do fluxo principal.

### FA-03 Paciente recusa o atendimento (PE-1)

- **Condição:** paciente consciente declara recusar o atendimento.
- **Passos:** 1. O sistema aciona UC-G03-04 (`<<extend>>`).
- **Reconvergência:** ao concluir UC-G03-04, retorna ao passo 3.

### FA-04 Conexão indisponível (PE-2)

- **Condição:** o tablet perde a conexão durante o atendimento.
- **Passos:** 1. A equipe continua registrando localmente. 2. Na reconexão, o sistema aciona UC-G03-07 (`<<extend>>`).
- **Reconvergência:** retorna ao passo em que o usuário estava.

## Fluxos de exceção

### FE-01 Usuário sem necessidade de atendimento

- **Condição:** perfil não autorizado para a ficha (RN-11).
- **Passos:** 1. O sistema nega o acesso, sem exibir conteúdo. 2. O sistema registra a tentativa negada (UC-G03-08).
- **Estado final:** nada exibido; evento de acesso com resultado `NEGADO`.

### FE-02 Falha ao gravar no dispositivo

- **Condição:** erro de armazenamento local.
- **Passos:** 1. O sistema não confirma a gravação. 2. O sistema mantém os dados na tela e alerta a equipe. 3. A equipe tenta novamente.
- **Estado final:** o sistema nunca confirma um registro que não gravou.

### FE-03 Lote do fármaco não identificado

- **Condição:** o lote está ilegível ou ausente na embalagem.
- **Passos:** 1. O sistema não bloqueia o registro clínico (premissa P-04). 2. A equipe registra o marcador "lote não identificado" e a justificativa. 3. O C4 segue a G05 com o marcador.
- **Estado final:** administração registrada; a conciliação do estoque cabe a G05 (RN-07 e RN-08).

### FE-04 G05 indisponível

- **Condição:** falha na publicação do C4.
- **Passos:** 1. O registro clínico permanece gravado. 2. O consumo fica pendente e é reentregue com o mesmo identificador.
- **Estado final:** consumo pendente de entrega; atendimento não bloqueado.

## Regras de negócio aplicadas

| Regra | Aplicação neste caso de uso |
| --- | --- |
| RN-11 | passo 2 e FE-01: dado clínico só para papel com necessidade de atendimento |
| RN-09 | passo 2: o acesso gera evento; a correção preserva o histórico |
| RN-12 | passos 5 e 8: horários do fato alimentam os indicadores de tempo |

## Relacionamentos

- `<<include>>` **UC-G03-08 Controlar e Registrar Acesso ao Prontuário**: obrigatório, porque todo acesso à ficha precisa de verificação de perfil e de evento (RN-11, LGPD art. 37).
- `<<extend>>` **UC-G03-04 Registrar Recusa de Atendimento**: opcional, só ocorre se paciente consciente recusa o atendimento.
- `<<extend>>` **UC-G03-07 Sincronizar Ficha na Reconexão**: opcional, só ocorre se houve período sem conexão.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Prontuario | ficha do atendimento | este módulo |
| RegistroSinaisVitais | parâmetros, horário de coleta, autor, justificativa de não aferição | este módulo |
| Procedimento | tipo, horário, executor | este módulo |
| ConsumoFarmaco | `item_id`, `lote`, `quantidade`, `via`, `horario`, `responsavel_id`, `prontuario_id` | este módulo (C4 para G05) |
| Despacho | `despacho_id`, `equipe_id` | contrato C2 (G02) |

## Critérios de aceite

- [ ] Cada registro de sinais vitais tem horário de coleta e autor.
- [ ] Um novo registro não apaga o anterior; o último é identificável.
- [ ] Correção preserva o original e identifica quem corrigiu.
- [ ] O sistema nunca confirma gravação que não ocorreu.
- [ ] Registro de fármaco com lote não identificado não é bloqueado e segue marcado.
- [ ] Todo consumo gera um C4 com os seis campos obrigatórios.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-02 | `RegistroSinaisVitais` | pendente (M2) | pendente (M3) |
| RF-G03-03 | `Procedimento` | pendente (M2) | pendente (M3) |
| RF-G03-09 | `ConsumoFarmaco` | pendente (M2) | pendente (M3) |
| RF-G03-12 | `ConsumoFarmaco` | pendente (M2) | pendente (M3) |
| RF-G03-15 | `Prontuario` | pendente (M2) | pendente (M3) |
