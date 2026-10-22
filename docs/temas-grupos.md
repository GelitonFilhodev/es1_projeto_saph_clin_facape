# Temas e Grupos — SAPH-Clin (6 grupos)

Cada grupo modela **um subprocesso completo** do SAPH-Clin. Subprocesso não é
"uma tela": é um conjunto de decisões, entidades e ciclos de vida que pode ser
especificado de ponta a ponta sem depender de outra equipe terminar.

## Mapa dos grupos

| Grupo | Pasta | Módulo | Subprocesso | Entrada recebida | Saída entregue |
| --- | --- | --- | --- | --- | --- |
| **G1** | `grupo-01-regulacao-triagem` | M1 | Chamado e classificação de risco | Ligação do solicitante | Chamado classificado (prioridade Manchester) |
| **G2** | `grupo-02-despacho-viaturas` | M1 | Despacho e frota | Chamado classificado | Despacho + estado da viatura |
| **G3** | `grupo-03-telemedicina-prontuario` | M2 | Teleorientação e prontuário pré-hospitalar | Despacho ativo | Ficha pré-hospitalar + pedido de pré-admissão |
| **G4** | `grupo-04-leitos-criticos` | M3 | Leitos críticos e reserva | Pedido de pré-admissão | Leito reservado/negado + alerta à equipe receptora |
| **G5** | `grupo-05-estoque-controlados` | M3 | Maletas e fármacos controlados | Consumo registrado em campo | Baixa por lote + solicitação de reposição |
| **G6** | `grupo-06-auditoria-compliance` | M4 | Auditoria, rastreabilidade e indicadores | Eventos de G1–G5 | Trilha imutável + relatórios + alertas |

> **G6 é transversal:** não é "o grupo do log". Ele define o **modelo de evento**
> que todos os outros grupos usam e é dono dos indicadores de operação.

---

## G1 — Regulação e Triagem

**Escopo:** acolhimento do chamado, coleta de dados mínimos, classificação de risco
e ciclo de vida do Chamado.

**Entidades centrais:** `Chamado`, `Triagem`, `Solicitante`, `ClassificacaoRisco`.

**Casos de uso esperados:** *Registrar Chamado*, *Classificar Risco*,
*Reclassificar Chamado* (`<<extend>>` de *Classificar Risco*),
*Cancelar Chamado*.

**Ciclo de vida a modelar:** `Chamado` — Aberto → Em Triagem → Viatura Despachada →
Em Atendimento → Encerrado, com transição alternada para Cancelado.

**Perguntas que o grupo deve responder:** Quem pode reclassificar e como?
O que acontece com chamado duplicado da mesma ocorrência? Como registrar
solicitante anônimo?

**Riscos:** modelar triagem como simples atributo de cor (perde histórico de
reclassificação); ignorar que a prioridade é decisão de médico regulador.

---

## G2 — Despacho e Frota de Viaturas

**Escopo:** escolha de viatura (USB/USA) por gravidade e proximidade, alocação de
equipe, rastreio do ciclo de vida da viatura e do atendimento.

**Entidades centrais:** `Viatura` (abstrata), `ViaturaUSB`, `ViaturaUSA`,
`Equipe`, `Despacho`, `Base`.

**Casos de uso esperados:** *Despachar Viatura* (`<<include>>` *Verificar
Disponibilidade de Equipe*), *Acionar Suporte Avançado* (`<<extend>>` de
*Despachar Viatura*), *Encerrar Atendimento*, *Sinalizar Indisponibilidade*.

**Ciclo de vida a modelar:** `Viatura` — Disponível → Deslocando para Sinistro →
No Local → Em Trânsito para Hospital → Em Descontaminação/Reposição.

**Perguntas que o grupo deve responder:** E se não houver viatura compatível?
Como justificar a escolha de USB em caso Amarelo? Quem confirma a chegada?

**Riscos:** modelar "viatura" sem herança e duplicar atributos de USA; não tratar
dupla alocação (RN-04).

---

## G3 — Telemedicina e Prontuário Pré-Hospitalar

**Escopo:** teleorientação do médico regulador, preenchimento da ficha
pré-hospitalar em campo e disparo da pré-admissão.

**Entidades centrais:** `Teleorientacao`, `Prontuario`, `RegistroSinaisVitais`,
`Procedimento`, `ConsumoFarmaco`, `PreAdmissao`.

**Casos de uso esperados:** *Registrar Teleorientação*, *Preencher Ficha
Pré-Hospitalar*, *Solicitar Pré-Admissão* (`<<include>>` *Validar Prioridade*),
*Registrar Recusa de Atendimento* (`<<extend>>`, exige assinatura).

**Perguntas que o grupo deve responder:** O que é obrigatório registrar antes da
chegada? O que fazer se a rede cair no local? Como garantir sigilo na ficha?

**Riscos:** transformar a ficha em prontuário hospitalar completo (fora de
escopo); deixar a recusa sem evidência de assinatura (RN-10).

---

## G4 — Leitos Críticos e Reserva

**Escopo:** oferta de leito, reserva vinculada ao chamado, bloqueios sanitários e
alerta à equipe receptora.

**Entidades centrais:** `Leito`, `Setor` (Sala Vermelha, Observação),
`ReservaLeito`, `Higienizacao`, `AlertaTransferencia`.

**Casos de uso esperados:** *Consultar Disponibilidade*, *Reservar Leito*
(`<<include>>` *Verificar Conflito de Reserva*), *Bloquear Leito*, *Liberar Leito*,
*Cancelar Reserva*.

**Ciclo de vida a modelar:** `Leito` — Vago → Reservado → Ocupado → Em Higienização
→ Vago; bloqueio como estado alternativo com motivo.

**Perguntas que o grupo deve responder:** Como impedir reserva dupla em pico?
Qual o prazo de expiração de uma reserva? Quem aceita o paciente na porta?

**Riscos:** tratar leito como número inteiro ("4 vagos") em vez de entidade com
estado; ignorar expiração de reserva.

---

## G5 — Estoque de Fármacos Controlados

**Escopo:** composição da maleta, dispensação por lote, validade, travamento de
item suspeito e reposição autorizada pelo farmacêutico.

**Entidades centrais:** `ItemEstoque`, `Lote`, `Maleta`, `MovimentacaoEstoque`,
`AutorizacaoDispensacao`, `Farmaceutico`.

**Casos de uso esperados:** *Registrar Consumo em Campo*, *Dispensar Controlado*
(`<<include>>` *Validar Lote e Validade*), *Solicitar Reposição*, *Travar Item
Suspeito*, *Conciliar Estoque*.

**Perguntas que o grupo deve responder:** Quem responde pelo controlado consumido?
Como conciliar sobra/falta de opioide? O que fazer com lote vencido na maleta?

**Riscos:** modelar estoque só como quantidade (perde lote/validade); permitir
dispensação sem autorização registrada (RN-07).

---

## G6 — Auditoria, Compliance e Indicadores

**Escopo:** modelo de evento imutável, assinatura de condutas excepcionais,
indicadores operacionais e regras de acesso a dado sensível.

**Entidades centrais:** `EventoAuditoria`, `AssinaturaDigital`, `Indicador`,
`PerfilAcesso`, `AlertaCompliance`.

**Casos de uso esperados:** *Registrar Evento Sensível*, *Consultar Trilha*,
*Assinar Conduta Excepcional*, *Calcular Indicadores*, *Auditar Acesso a Prontuário*.

**Perguntas que o grupo deve responder:** Quais eventos são sensíveis (e por quê)?
Como garantir imutabilidade sem inventar tecnologia fora do escopo? Quais
indicadores provam qualidade do serviço?

**Riscos:** modelar auditoria como "log de texto" sem estrutura; deixar de definir
o que **não** pode ser registrado (minimização LGPD).

---

## Dependências e paralelismo

```text
G1 (chamado classificado)
  └─> G2 (despacho) ──> G3 (ficha + pré-admissão) ──> G4 (leito)
                                  │
                                  └─> G5 (consumo de controlados)

G6 recebe eventos de G1, G2, G3, G4 e G5 (transversal)
```

**Regra de paralelismo:** cada grupo pode avançar sozinho porque o contrato de
entrada/saída está fechado em [`arquitetura-modular.md`](arquitetura-modular.md).
Nenhum grupo espera o outro terminar para modelar o próprio módulo.
