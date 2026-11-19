# UC-G03-05 Validar Prioridade

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G03-05 |
| **Módulo** | G03: Telemedicina e Prontuário Pré-Hospitalar |
| **Ator primário** | nenhum humano (acionado por UC-G03-03 por `<<include>>`) |
| **Atores secundários** | Sistema de Regulação (G01, dono da prioridade) |
| **Objetivo** | Garantir que a pré-admissão use a prioridade vigente do chamado, sem recálculo |
| **Requisitos rastreados** | RF-G03-04 |
| **Prioridade** | essencial |

## Pré-condições

- `chamado_id` do atendimento disponível no contexto do UC-G03-03.

## Pós-condições

- **Sucesso:** prioridade vigente confirmada (`VERMELHO`, `LARANJA`, `AMARELO`, `VERDE` ou `AZUL`) e entregue ao caso de uso chamador, somente leitura.
- **Falha:** nenhuma prioridade entregue; o caso de uso chamador é interrompido.

## Fluxo principal

1. O sistema consulta, por `chamado_id`, a prioridade vigente no chamado (dono: G01).
2. O sistema verifica que o valor pertence ao conjunto do Protocolo de Manchester definido no contrato C1.
3. O sistema entrega ao chamador a prioridade e o horário da classificação, sem permitir alteração.

## Fluxos alternativos

### FA-01 Chamado reclassificado

- **Condição:** existe mais de uma classificação no histórico do chamado.
- **Passos:** 1. O sistema usa a mais recente. 2. O sistema informa o horário dela ao chamador.
- **Reconvergência:** retorna ao passo 3.

## Fluxos de exceção

### FE-01 Prioridade ausente ou inválida

- **Condição:** o chamado não tem prioridade ou o valor não pertence ao conjunto.
- **Passos:** 1. O sistema falha o caso de uso. 2. O sistema informa o motivo ao chamador.
- **Estado final:** nenhuma prioridade entregue; nenhum valor é digitado ou estimado neste módulo.

### FE-02 G01 sem resposta

- **Condição:** a consulta não retorna.
- **Passos:** igual a FE-01, com motivo "G01 indisponível". O sistema não usa valor antigo de memória.
- **Estado final:** pedido de pré-admissão não emitido (ver Q-02).

## Regras de negócio aplicadas

| Regra | Aplicação |
| --- | --- |
| RN-02 | a prioridade é do protocolo e de G01; este módulo só herda |

## Relacionamentos

- Incluído por **UC-G03-03** (`<<include>>`).

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Chamado | `chamado_id`, prioridade vigente, horário da classificação | G01, por referência |

## Critérios de aceite

- [ ] O valor entregue é idêntico ao vigente em G01.
- [ ] Nenhum caminho do módulo permite digitar ou recalcular prioridade.
- [ ] Prioridade ausente ou inválida interrompe o pedido.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G03-04 | `PreAdmissao` | pendente (M2) | pendente (M3) |
