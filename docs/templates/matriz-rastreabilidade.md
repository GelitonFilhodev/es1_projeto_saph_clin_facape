# Matriz de Rastreabilidade — G0X

> Template. Copie para a raiz da pasta do grupo como `matriz-rastreabilidade.md`.
> A matriz é a prova de que o módulo conta **uma** história: requisito que não
> chega ao teste está incompleto; teste sem requisito é ruído.

## Regra de preenchimento

- Uma linha por requisito funcional.
- `Classe` e `Sequência` são obrigatórias a partir do M2.
- `Caso de teste` é obrigatória no M3.
- Célula vazia = pendência: marque `pendente` em vez de deixar em branco.

## Matriz

| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-G0X-01 | | UC-G0X-01 | | DS-G0X-01 | CT-G0X-01 | pendente |
| RF-G0X-02 | | UC-G0X-02 | | DS-G0X-02 | CT-G0X-02 | pendente |
| RF-G0X-03 | | UC-G0X-01 | | | | pendente |

## Cobertura de requisitos não funcionais

| RNF | Métrica e alvo | Como é verificado | Status |
| --- | --- | --- | --- |
| RNF-G0X-01 | reserva confirmada em ≤ 2 s com 20 req/min | análise do fluxo de reserva + CT de fronteira | pendente |

## Contratos de módulo consumidos

| Contrato | Origem | Uso no módulo | Campo crítico |
| --- | --- | --- | --- |
| C1 `chamado_classificado` | G1 | entrada do despacho | `prioridade` |

## Contratos de módulo fornecidos

| Contrato | Destino | Campo crítico | Estabilidade |
| --- | --- | --- | --- |
| C2 `despacho_ativo` | G3 | `despacho_id` | estável |

## Pendências e riscos

| Item | Impacto | Prazo interno |
| --- | --- | --- |
| | | |

## Checklist final

- [ ] Todo RF tem caso de uso.
- [ ] Todo caso de uso tem classe.
- [ ] Todo fluxo crítico tem diagrama de sequência.
- [ ] Todo RF tem pelo menos um caso de teste.
- [ ] Nenhum `pendente` no M3.
- [ ] Contratos consumidos/fornecidos conferem com
      [`arquitetura-modular.md`](../arquitetura-modular.md).
