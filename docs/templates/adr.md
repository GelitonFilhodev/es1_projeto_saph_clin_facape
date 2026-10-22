# ADR-G0X-NN — Título curto da decisão

> Template de *Architecture Decision Record*. Copie para `adr/`.
> Um ADR registra **uma** decisão. Se você escreveu "e também decidimos...", são dois ADRs.

## Status

`proposto` · `aceito` · `substituído por ADR-G0X-NN` · `depreciado`

Data: AAAA-MM-DD
Decisores: *nomes dos integrantes*

## Contexto

*Qual é a força que exige uma decisão? Descreva a situação em 3 a 6 linhas, com
números quando existirem (tempo, volume, limite legal). Cite a fonte: norma,
definição do projeto, regra de negócio, contrato de módulo.*

## Decisão

*O que foi decidido, em uma frase afirmativa, no presente: "O sistema modela X como Y".*

## Alternativas consideradas

| Alternativa | Prós | Contras | Por que foi descartada |
| --- | --- | --- | --- |
| A | | | |
| B | | | |

## Consequências

**Positivas**

- *o que fica mais fácil*

**Negativas / custos**

- *o que fica mais difícil, e quem paga esse custo*

**Impactos em outros grupos**

- *contrato alterado? qual grupo precisa saber?*

## Como verificar

*Que artefato ou caso de teste prova que a decisão está implementada na modelagem?*

---

## Exemplo de referência — ADR-G04-01: reserva de leito é transacional

**Status:** aceito · **Contexto:** em pico, duas solicitações de pré-admissão
chegam para o único leito de Sala Vermelha (RN-05). O controle por telefone
permite reserva dupla, e o paciente em maca espera indefinidamente.

**Decisão:** a reserva de leito é um **vínculo com identificador único, prazo de
expiração e verificação de conflito no momento da criação** — o leito só aceita
uma reserva ativa.

**Alternativas:** (a) controle manual pela enfermagem — descartada por não impedir
dupla reserva; (b) fila de espera por prioridade — descartada porque não resolve a
corrida na criação.

**Consequências:** o leito passa a ter estado explícito (`Vago`, `Reservado`,
`Ocupado`, `EmHigienizacao`, `Bloqueado`); G3 precisa enviar `eta_hospital` para
calcular a expiração; G6 deve registrar `LEITO_RESERVADO` e `LEITO_NEGADO`.

**Verificação:** CT-G04-02 (duas reservas simultâneas — a segunda deve ser negada).
