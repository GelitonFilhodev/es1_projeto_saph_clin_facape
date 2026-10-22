# UC-G02-01 — Despachar Viatura

> **Exemplo completo** (não é template). Use como referência de nível de detalhe
> esperado. Pertence ao G02; entidades de outros grupos aparecem apenas por
> referência.

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | UC-G02-01 |
| **Módulo** | G02 — Despacho e Frota de Viaturas |
| **Ator primário** | MedicoRegulador |
| **Atores secundários** | EquipeIntervencao, Sistema de Auditoria (G06) |
| **Objetivo** | Alocar a viatura adequada a um chamado classificado e registrar o despacho |
| **Requisitos rastreados** | RF-G02-01, RF-G02-02, RF-G02-03, RF-G02-04, RF-G02-07 |
| **Prioridade** | essencial |

## Pré-condições

- Chamado existente com `prioridade` definida (contrato C1, de G1).
- Chamado ainda sem despacho ativo.

## Pós-condições

- **Sucesso:** `Despacho` criado em estado `Ativo`, viatura em
  `Deslocando para Sinistro`, evento `VIATURA_DESPACHADA` publicado em G06.
- **Falha:** nenhum despacho criado; chamado permanece na fila com prioridade
  preservada e motivo registrado.

## Fluxo principal

1. O médico regulador seleciona um chamado classificado na fila de regulação.
2. O sistema exibe as viaturas compatíveis com a prioridade, ordenadas por
   proximidade e tempo estimado de chegada.
3. O médico regulador seleciona a viatura e confirma o despacho.
4. O sistema **verifica disponibilidade de equipe** (caso de uso incluído).
5. O sistema cria o despacho, altera o estado da viatura e registra o autor e a
   justificativa da escolha.
6. O sistema publica o contrato C2 `despacho_ativo` para G3 e o evento
   `VIATURA_DESPACHADA` para G6.
7. O sistema confirma ao médico regulador com o ETA estimado.

## Fluxos alternativos

### FA-01 — Suporte avançado necessário durante o despacho

- **Condição:** prioridade VERMELHO ou equipe de campo relata deterioração.
- **Passos:** 1. Sistema sugere USA. 2. Médico regulador aciona suporte avançado
  (`UC-G02-02`, `<<extend>>`). 3. Despacho é criado já com composição de USA.
- **Reconvergência:** retorna ao passo 5 do fluxo principal.

### FA-02 — Nenhuma viatura compatível disponível

- **Condição:** não há USA disponível para chamado VERMELHO.
- **Passos:** 1. Sistema informa indisponibilidade com o motivo por viatura.
  2. Sistema propõe despacho de USB com apoio remoto de telemedicina (G3).
  3. Médico regulador decide e registra justificativa (RN-02 aplicada por analogia).
- **Reconvergência:** retorna ao passo 5 com a decisão registrada.

## Fluxos de exceção

### FE-01 — Viatura alocada por outro despacho no intervalo

- **Condição:** a viatura foi despachada por outro usuário entre a consulta e a
  confirmação (RN-04).
- **Passos:** 1. Sistema rejeita a confirmação com `VIATURA_INDISPONIVEL`.
  2. Sistema recarrega a lista e destaca a viatura removida.
  3. Chamado permanece na fila; nenhum estado parcial é gravado.
- **Estado final:** chamado em `Em Triagem`/`Aguardando Despacho`, evento
  `DESPACHO_REJEITADO` registrado.

### FE-02 — Equipe de suporte avançado incompleta

- **Condição:** USA selecionada sem equipe completa (RN-03).
- **Passos:** 1. Sistema bloqueia a confirmação. 2. Sistema informa qual
  qualificação falta. 3. Médico regulador escolhe outra viatura.
- **Estado final:** nenhum despacho criado.

## Regras de negócio aplicadas

| Regra | Aplicação neste caso de uso |
| --- | --- |
| RN-03 | passo 4 e FE-02 — USA exige equipe completa |
| RN-04 | FE-01 — viatura não pode estar em dois despachos ativos |
| RN-09 | passo 6 — despacho gera evento imutável |

## Relacionamentos

- `<<include>>` **UC-G02-05 Verificar Disponibilidade de Equipe** — toda
  confirmação de despacho exige a verificação; sem ela não há como garantir RN-03.
- `<<extend>>` **UC-G02-02 Acionar Suporte Avançado** — extensão opcional,
  disparada quando a prioridade ou a evolução clínica exigem USA.

## Dados manipulados

| Entidade | Dado | Origem |
| --- | --- | --- |
| Chamado | `chamado_id`, `prioridade` | contrato C1 (G1) |
| Despacho | `despacho_id`, `viatura_id`, `equipe_id`, `justificativa` | este módulo |
| Viatura | `estado` | este módulo |

## Critérios de aceite

- [ ] Despacho sempre referencia um chamado classificado e uma viatura disponível.
- [ ] Nenhum cenário permite duas viaturas iguais em despachos ativos.
- [ ] Despacho de USA sem equipe completa é impossível no modelo.
- [ ] Toda confirmação gera evento `VIATURA_DESPACHADA` com autor e horário.

## Rastreabilidade

| RF | Classe | Sequência | Teste |
| --- | --- | --- | --- |
| RF-G02-01 | `Despacho` | DS-G02-01 | CT-G02-01 |
| RF-G02-02 | `Viatura` | DS-G02-01 | CT-G02-02 |
| RF-G02-03 | `ViaturaUSA`, `Equipe` | DS-G02-03 | CT-G02-03 |
| RF-G02-04 | `Despacho` | DS-G02-01 | CT-G02-01 |
| RF-G02-07 | `Despacho` | DS-G02-02 | CT-G02-04 |
