# Templates de Artefato

Modelos obrigatórios da disciplina. Copie para a pasta do seu grupo e preencha;
não crie formato novo sem justificativa em ADR.

| Template | Use para | Vai em |
| --- | --- | --- |
| [`caso-de-uso.md`](caso-de-uso.md) | especificação textual de caso de uso | `casos-de-uso/UC-G0X-NN-nome.md` |
| [`adr.md`](adr.md) | decisão arquitetural / de modelagem | `adr/ADR-G0X-NN-nome.md` |
| [`caso-de-teste.md`](caso-de-teste.md) | caso de teste derivado de requisito | `testes/CT-G0X-NN-nome.md` |
| [`matriz-rastreabilidade.md`](matriz-rastreabilidade.md) | elo requisito → modelo → teste | raiz do grupo |

Referência de nível de detalhe esperado:
[`../exemplos/uc-g02-01-despachar-viatura.md`](../exemplos/uc-g02-01-despachar-viatura.md)
(caso de uso completo, com fluxos alternativos, exceções e rastreabilidade).

## Regras de preenchimento

- **Identificador sempre com o número do grupo:** `RF-G02-01`, `UC-G02-03`,
  `CT-G02-02`, `ADR-G02-01`.
- **Nada de "TBD" no M3.** Placeholder é aceitável no M1, nunca na entrega final.
- **Toda afirmação de domínio cita a fonte:** `definicao-projeto.md`,
  `contexto-do-sistema.md` (RN-XX), norma ou ADR.
- **Português com acentuação.** Nome de arquivo, não: nome de arquivo é ASCII kebab-case.

## Sequência recomendada de trabalho

```text
1. contexto + temas-grupos  →  escopo do módulo (E1)
2. escopo                   →  RF/RNF (E2)
3. RF                       →  casos de uso (E3)
4. casos de uso             →  classes + dicionario (E4)
5. classes + casos de uso   →  sequencia + estados (E5)
6. tudo                     →  ADRs, matriz, testes (E6)
7. casos de uso             →  wireframes (E7)
```

Se o passo 4 exigir uma classe que o passo 3 não menciona, o caso de uso está
incompleto — volte ao passo 3. Essa é a checagem de consistência mais barata do
projeto.
