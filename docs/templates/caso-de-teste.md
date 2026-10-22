# CT-G0X-NN — Nome do Caso de Teste

> Template. Copie para `testes/ct-XX-NN-nome.md`. Um caso de teste deriva de um
> requisito; se você não sabe qual RF ele cobre, o teste não deveria existir.

## Identificação

| Campo | Valor |
| --- | --- |
| **ID** | CT-G0X-NN |
| **Requisito rastreado** | RF-G0X-NN (ou RNF-G0X-NN) |
| **Caso de uso** | UC-G0X-NN |
| **Tipo** | funcional / fronteira / exceção / não funcional |
| **Prioridade** | alta / média / baixa |

## Objetivo

*O que este teste prova, em uma frase. Ex.: "garante que o leito não aceita duas
reservas ativas".*

## Pré-condições

- *estado necessário do sistema e dos dados*

## Dados de entrada

| Campo | Valor |
| --- | --- |
| `prioridade` | LARANJA |
| `necessidade` | SALA_VERMELHA |

## Passos

1. *ação executada*
2. *ação executada*
3. *verificação*

## Resultado esperado

- *saída observável e verificável*

## Resultado obtido

*Preencher apenas após executar a verificação sobre a modelagem (matriz, diagrama
ou protótipo). Deixe `não executado` no M1/M2.*

## Critério de aceite

*Condição binária: passou ou falhou. Nada de "parcialmente".*

## Observações

*Ambiguidade encontrada, decisão tomada, ADR relacionado.*

---

## Exemplo de referência — CT-G04-02: duas reservas simultâneas no mesmo leito

**Requisito:** RF-G04-03 (impedir reserva dupla) · **Tipo:** fronteira/concorrência.

**Pré-condição:** leito `LV-01` (Sala Vermelha) com estado `Vago`.

**Passos:**
1. Solicitar pré-admissão A para `LV-01` (prioridade VERMELHO, ETA 8 min).
2. Solicitar pré-admissão B para `LV-01` (prioridade LARANJA, ETA 5 min).
3. Consultar estado de `LV-01`.

**Resultado esperado:** A é aceita (`Reservado`); B é negada com motivo
`LEITO_INDISPONIVEL`; evento `LEITO_NEGADO` registrado por G6; B permanece na fila
com prioridade preservada.

**Critério de aceite:** existe exatamente **uma** reserva ativa por leito em todo
o modelo (verificável na máquina de estados e na matriz).
