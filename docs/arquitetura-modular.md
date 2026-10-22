# Arquitetura Modular — Contratos entre Módulos

Este documento fecha as **fronteiras** entre os seis módulos. Ele existe para que
seis grupos trabalhem em paralelo sem bloquear uns aos outros: se o contrato está
definido, cada equipe modela internamente como quiser.

> Regra: se um grupo precisa de um dado que não está no contrato, ele **propõe
> alteração de contrato via ADR** e avisa os afetados. Não se "resolve no código".

---

## 1. Princípios de decomposição

1. **Fronteira por decisão, não por tela.** Um módulo termina onde a
   responsabilidade de decisão muda de ator.
2. **Contrato explícito.** Todo dado que cruza fronteira tem nome, tipo e dono.
3. **Acoplamento por evento.** O módulo não chama o outro "no meio" do seu fluxo;
   ele publica um fato consumado.
4. **Auditoria transversal.** G6 observa todos os módulos, nenhum módulo
   implementa a própria trilha.
5. **Falha previsível.** Todo contrato define o que acontece quando o outro lado
   não responde.

---

## 2. Visão de módulos

```text
┌──────────────────────── M1 · Regulação ────────────────────────┐
│  G1 Chamado/Triagem  ──chamado_classificado──>  G2 Despacho    │
└────────────────────────────────────────────────────────────────┘
                                   │ despacho_ativo
                                   v
┌──────────────────────── M2 · Telemedicina ─────────────────────┐
│  G3 Teleorientação + Ficha + Pré-admissão                      │
└────────────────────────────────────────────────────────────────┘
              │ pedido_pre_admissao          │ consumo_farmaco
              v                             v
┌──────────── M3 · Recursos Críticos ────────────┐   ┌── G5 ────────┐
│  G4 Leitos: reserva, bloqueio, liberação       │   │  Estoque     │
└────────────────────────────────────────────────┘   └──────────────┘

┌──────────────── M4 · Auditoria (transversal) ───────────────────┐
│ G6: eventos de G1–G5, assinatura, indicadores, compliance       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Contratos de interface

### C1 · G1 → G2 `chamado_classificado`

| Campo | Tipo | Obrigatório | Observação |
| --- | --- | --- | --- |
| `chamado_id` | identificador | sim | gerado no acolhimento |
| `prioridade` | enum | sim | `VERMELHO`, `LARANJA`, `AMARELO`, `VERDE`, `AZUL` |
| `queixa_principal` | texto | sim | descrição do solicitante |
| `localizacao` | geo/texto | sim | endereço + referência |
| `solicitante` | referência | não | pode ser anônimo |
| `triagem_em` | data/hora | sim | base do cálculo de tempo de resposta |

**Falha de contrato:** sem `prioridade`, G2 não despacha — o chamado fica em
`Em Triagem` e alerta o regulador.

### C2 · G2 → G3 `despacho_ativo`

| Campo | Tipo | Obrigatório | Observação |
| --- | --- | --- | --- |
| `despacho_id` | identificador | sim | — |
| `chamado_id` | referência | sim | rastreabilidade |
| `viatura_id` / `tipo` | referência/enum | sim | `USB` ou `USA` |
| `equipe_id` | referência | sim | responsável pelo atendimento |
| `eta_local` | duração | não | preenchido após aceite |

### C3 · G3 → G4 `pedido_pre_admissao`

| Campo | Tipo | Obrigatório | Observação |
| --- | --- | --- | --- |
| `prontuario_id` | identificador | sim | ficha pré-hospitalar |
| `chamado_id` | referência | sim | — |
| `prioridade` | enum | sim | herdada da triagem, não recalculada |
| `necessidade` | enum | sim | `SALA_VERMELHA`, `OBSERVACAO` |
| `sinais_vitais` | resumo | sim | último registro |
| `eta_hospital` | duração | sim | base do prazo de reserva |

**Falha de contrato:** leito indisponível → G4 devolve `negado` com motivo; G3/G2
decidem desvio (outro hospital ou teleorientação ampliada).

### C4 · Campo → G5 `consumo_farmaco`

| Campo | Tipo | Obrigatório | Observação |
| --- | --- | --- | --- |
| `item_id` | referência | sim | item da maleta |
| `lote` | texto | sim | rastreio sanitário |
| `quantidade` | número | sim | unidade de medida do item |
| `via` / `horario` | enum/data-hora | sim | registro clínico |
| `responsavel_id` | referência | sim | quem administrou |
| `prontuario_id` | referência | sim | vínculo clínico |

### C5 · G1–G5 → G6 `evento_sensivel`

| Campo | Tipo | Obrigatório | Observação |
| --- | --- | --- | --- |
| `evento_id` | identificador | sim | imutável |
| `tipo` | enum | sim | `REGULACAO`, `DESPACHO`, `DISPENSACAO`, `RESERVA`, `ACESSO` |
| `ator_id` / `papel` | referência/enum | sim | quem executou |
| `entidade` / `entidade_id` | texto/referência | sim | o que sofreu a ação |
| `ocorrido_em` | data/hora | sim | horário do fato |
| `resultado` | enum | sim | `SUCESSO`, `NEGADO`, `ERRO` |
| `justificativa` | texto | condicional | obrigatória em exceção |

---

## 4. Catálogo de eventos sensíveis (mínimo)

| Evento | Origem | Por que é sensível |
| --- | --- | --- |
| `CHAMADO_CLASSIFICADO` | G1 | define prioridade clínica |
| `PRIORIDADE_RECLASSIFICADA` | G1 | muda fila de atendimento |
| `VIATURA_DESPACHADA` | G2 | compromete recurso escasso |
| `SUPORTE_AVANCADO_ACIONADO` | G2 | custo e risco elevados |
| `TELEORIENTACAO_REGISTRADA` | G3 | conduta médica a distância |
| `LEITO_RESERVADO` / `LEITO_NEGADO` | G4 | acesso a recurso crítico |
| `CONTROLADO_DISPENSADO` | G5 | exigência legal (SNGPC) |
| `ITEM_TRAVADO` | G5 | risco sanitário |
| `PRONTUARIO_ACESSADO` | G3/G6 | dado sensível (LGPD) |
| `RECUSA_ASSINADA` | G3 | proteção jurídica |

---

## 5. Indicadores do sistema (G6)

| Indicador | Definição | Fonte |
| --- | --- | --- |
| Tempo de resposta | chamado aberto → atendimento iniciado | C1 + C5 |
| Tempo porta-leito | chegada ao hospital → leito ocupado | C3 + C4 |
| Taxa de reserva negada | pedidos negados ÷ pedidos | C3 |
| Ocupação de Sala Vermelha | leitos ocupados ÷ leitos operacionais | G4 |
| Consumo por 1.000 atendimentos | dispensações ÷ atendimentos × 1.000 | C4 |
| Divergência de estoque | |consumido − baixado| por maleta | G5 + G6 |
| Reclassificações por plantão | contagem de eventos | G1 |

---

## 6. Regras de integração

- **Idempotência:** reenvio do mesmo `evento_id` não duplica registro.
- **Ordem:** eventos carregam timestamp do fato, não do envio.
- **Falha do consumidor:** evento fica pendente e é reentregue; o módulo de origem
  não bloqueia o atendimento.
- **Sem chamada síncrona entre módulos** para decisão clínica: a decisão é do ator,
  o sistema apenas registra e notifica.
- **Contrato versionado:** mudança de campo exige ADR + aviso no PR dos grupos afetados.

---

## 7. O que **não** é integração neste projeto

- Implementar API real, fila ou banco de dados.
- Definir stack tecnológica como requisito de arquitetura (é decisão de
  implementação, fora do escopo da disciplina).
- Modelar autenticação em detalhe: basta o **perfil de acesso** e o evento de acesso.
