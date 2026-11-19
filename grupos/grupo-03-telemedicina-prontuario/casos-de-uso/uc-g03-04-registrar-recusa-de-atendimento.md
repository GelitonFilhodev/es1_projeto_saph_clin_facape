# UC-G03-04 Registrar Recusa de Atendimento

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-04 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | EquipeIntervencao |
| **Atores secundários** | MedicoRegulador (confirmação, premissa P-08), Sistema de Auditoria (G06) |
| **Participantes presenciais, sem acesso ao sistema** | Paciente (ou representante legal) e testemunha, que assinam no dispositivo |
| **Objetivo** | Registrar a recusa de atendimento por paciente consciente, com evidência de assinatura e testemunha |
| **Requisitos rastreados** | RF-G03-05, RF-G03-08 (evento `RECUSA_ASSINADA`), RF-G03-06 (coleta offline) |
| **Prioridade** | essencial |

## Pré-condições

- Ficha aberta (UC-G03-02 em andamento) com despacho ativo.
- Paciente declara recusar o atendimento.

## Pós-condições

- **Sucesso:** `RecusaAtendimento` gravada com declaração de consciência, ciência dos riscos, assinatura do paciente, assinatura da testemunha e confirmação do médico regulador; evento `RECUSA_ASSINADA` publicado a G06.
- **Falha:** recusa gravada como `Incompleta`, com o motivo da falta de evidência; nenhum evento `RECUSA_ASSINADA` é publicado.

## Fluxo principal

1. A equipe registra que o paciente declara recusar o atendimento e o motivo declarado, se houver.
2. O sistema solicita a declaração da equipe de que o paciente está consciente e orientado.
3. A equipe declara a consciência do paciente e registra que os riscos da recusa foram explicados.
4. O sistema exibe o termo de recusa com os dados do atendimento.
5. O paciente assina o termo no dispositivo.
6. A testemunha informa seu nome e assina no dispositivo.
7. O sistema solicita a confirmação do médico regulador.
8. O médico regulador confirma e assina.
9. O sistema grava a recusa com autor, horário e referências às assinaturas (`AssinaturaDigital`, de G06).
10. O sistema publica o evento `RECUSA_ASSINADA` (contrato C5) a G06 e informa a conclusão à equipe.

## Fluxos alternativos

### FA-01 Paciente reconsidera

- **Condição:** o paciente aceita o atendimento antes da conclusão ou depois dela.
- **Passos:** 1. A equipe registra a revogação com horário. 2. O sistema preserva a recusa e anexa a revogação (histórico imutável).
- **Reconvergência:** retorna ao passo 3 de UC-G03-02.

### FA-02 Sem conexão com a central

- **Condição:** o tablet está offline (PE-2 de UC-G03-02).
- **Passos:** 1. O sistema coleta e guarda localmente as assinaturas do paciente e da testemunha. 2. A confirmação do médico regulador fica pendente. 3. Na reconexão, UC-G03-07 sincroniza e o passo 7 é retomado.
- **Reconvergência:** retorna ao passo 7.

## Fluxos de exceção

### FE-01 Paciente sem consciência declarada

- **Condição:** a equipe declara que o paciente não está consciente ou orientado.
- **Passos:** 1. O sistema impede o registro de recusa (RN-10 vale para paciente consciente). 2. O sistema orienta seguir a conduta clínica e informa o médico regulador.
- **Estado final:** nenhuma recusa registrada.

### FE-02 Paciente não assina

- **Condição:** o paciente recusa assinar o termo.
- **Passos:** 1. O sistema grava a recusa como `Incompleta`, com o motivo. 2. O sistema não publica `RECUSA_ASSINADA`. 3. O sistema alerta o médico regulador.
- **Estado final:** a recusa verbal fica registrada como fato, mas não vale como recusa assinada.

### FE-03 Testemunha indisponível

- **Condição:** não há testemunha presente.
- **Passos:** igual a FE-02, com motivo "sem testemunha".
- **Estado final:** recusa `Incompleta`.

### FE-04 Falha na captura da assinatura

- **Condição:** erro do dispositivo ao capturar a assinatura.
- **Passos:** 1. O sistema informa a falha. 2. A equipe tenta novamente.
- **Estado final:** sem assinatura capturada, a recusa não é concluída.

### FE-05 Médico regulador não confirma

- **Condição:** o médico regulador está indisponível ou rejeita a confirmação.
- **Passos:** 1. A recusa permanece `Aguardando confirmação`. 2. O sistema registra o motivo da rejeição, se houver, e notifica o médico regulador.
- **Estado final:** sem confirmação, o evento `RECUSA_ASSINADA` não é publicado.

## Regras de negócio aplicadas

| Regra | Aplicação neste caso de uso |
| --- | --- |
| RN-10 | passos 2 a 6 e FE-01 a FE-03: assinatura e testemunha são exigidas |
| RN-09 | passo 10: recusa assinada gera evento imutável |
| RN-11 | os dados da recusa seguem o acesso restrito da ficha |

## Relacionamentos

- `<<extend>>` **UC-G03-02 Preencher Ficha Pré-Hospitalar** (ponto de extensão PE-1): opcional, porque só ocorre quando paciente consciente recusa o atendimento; a maioria dos atendimentos não passa por ele.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| RecusaAtendimento (candidata, ver E4) | motivo, declaração de consciência, ciência dos riscos, estado (`Aguardando confirmação`, `Concluída`, `Incompleta`, `Revogada`) | este módulo |
| AssinaturaDigital | `assinatura_id` do paciente, da testemunha e do médico regulador | G06, por referência |
| Prontuario | `prontuario_id` | este módulo |

## Critérios de aceite

- [ ] Não existe recusa concluída sem as três evidências (paciente, testemunha, confirmação do regulador).
- [ ] Recusa sem assinatura é registrada como `Incompleta` e não gera `RECUSA_ASSINADA`.
- [ ] A revogação não apaga a recusa anterior.
- [ ] A recusa não é aceita quando a equipe declara paciente sem consciência.
- [ ] Assinaturas coletadas offline são preservadas e sincronizadas.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-05 | `RecusaAtendimento` | pendente (M2) | pendente (M3) |
| RF-G03-06 | `RecusaAtendimento` | pendente (M2) | pendente (M3) |
| RF-G03-08 | `RecusaAtendimento` | pendente (M2) | pendente (M3) |
