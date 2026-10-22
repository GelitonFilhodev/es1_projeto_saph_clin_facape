# G02 — Despacho e Frota de Viaturas

> Grupo responsável pelo subprocesso **Despacho por gravidade/proximidade e ciclo de vida da Viatura** do SAPH-Clin.
> Módulo: M1 — Regulação e Despacho de Urgência

## Integrantes

| Nome | Matrícula | Papel no grupo |
| --- | --- | --- |
| *preencher* | | requisitos |
| *preencher* | | modelagem estrutural |
| *preencher* | | modelagem comportamental |
| *preencher* | | testes e rastreabilidade |

## Escopo do módulo (E1)

- **Subprocesso:** Despacho por gravidade/proximidade e ciclo de vida da Viatura.
- **Atores envolvidos:** MedicoRegulador, EquipeIntervencao.
- **Entidades de domínio (donas do módulo):** `Viatura` (abstrata), `ViaturaUSB`, `ViaturaUSA`, `Equipe`, `Despacho`, `Base`.
- **Entrada:** Contrato C1 `chamado_classificado` (G1).
- **Saída:** Contrato C2 `despacho_ativo` para G3.

### Fora do escopo do grupo

- classificar risco do chamado (G1).
- preencher ficha clínica (G3).
- controlar estoque da maleta (G5).

> Se algo do escopo acima for necessário, consuma o **contrato** descrito em
> `docs/arquitetura-modular.md` — não modele a entidade do vizinho.

## Casos de uso esperados (E3)

- UC-G02-01 Despachar Viatura (`<<include>>` Verificar Disponibilidade de Equipe)
- UC-G02-02 Acionar Suporte Avançado (`<<extend>>` de Despachar Viatura)
- UC-G02-03 Encerrar Atendimento
- UC-G02-04 Sinalizar Indisponibilidade da Viatura

Use `docs/templates/caso-de-uso.md`. Mínimo: 4 casos de uso, sendo 2
especificados textualmente e pelo menos um `<<include>>` e um `<<extend>>`
justificados.

## Requisitos âncora (ponto de partida, não de chegada)

| ID | Requisito funcional | Caso de uso |
| --- | --- | --- |
| RF-G02-01 | Selecionar viatura compatível com a prioridade clínica | UC-G02-01 |
| RF-G02-02 | Impedir dupla alocação da mesma viatura (RN-04) | UC-G02-01 |
| RF-G02-03 | Exigir equipe de suporte avançado completo para despachar USA (RN-03) | UC-G02-01 |
| RF-G02-04 | Registrar justificativa do despacho escolhido | UC-G02-01 |
| RF-G02-05 | Acionar suporte avançado durante atendimento em curso | UC-G02-02 |
| RF-G02-06 | Rastrear estados da viatura em tempo real | UC-G02-04 |
| RF-G02-07 | Devolver chamado à fila quando não houver viatura compatível | UC-G02-01 |
| RF-G02-08 | Publicar evento `VIATURA_DESPACHADA` para G6 | UC-G02-01 |

| ID | Requisito não funcional (com métrica) | Categoria |
| --- | --- | --- |
| RNF-G02-01 | Despacho concluído em ≤ 120 s após classificação | desempenho |
| RNF-G02-02 | Estimativa de chegada atualizada a cada 2 min | desempenho |
| RNF-G02-03 | Estado da viatura consistente entre despachos concorrentes | consistência |
| RNF-G02-04 | Painel legível em tablet de campo sob luz solar | usabilidade |
| RNF-G02-05 | Histórico de despacho retido por 5 anos para auditoria | conformidade |

> Estes requisitos são **sementes** extraídas do contexto. O grupo deve
> refiná-los, dividir os compostos e acrescentar o que a análise revelar.
> Requisito copiado sem análise perde nota em profundidade.

## Eventos que o módulo publica para G06

- `VIATURA_DESPACHADA`
- `SUPORTE_AVANCADO_ACIONADO`
- `ATENDIMENTO_ENCERRADO`

## Riscos de modelagem conhecidos

- modelar viatura sem herança e duplicar atributos de USA.
- ignorar indisponibilidade (viatura em higienização ainda aparece como livre).
- não modelar o que acontece quando não há viatura.

## Estado da entrega

| Artefato | M1 (Aula 18) | M2 (Aula 24) | M3 (Aula 27) |
| --- | --- | --- | --- |
| E1 Visão e escopo | pendente | — | — |
| E2 Catálogo RF/RNF | pendente | — | — |
| E3 Casos de uso | pendente | — | — |
| E4 Classes + dicionário | — | pendente | — |
| E5 Sequência + estados | — | pendente | — |
| E6 ADRs, matriz e testes | — | parcial | pendente |
| E7 Protótipos + relatório | — | — | pendente |

Atualize esta tabela a cada PR: é o primeiro lugar onde o professor olha.

## Como rodar a validação local

```bash
python3 scripts/check_entrega.py --grupo grupo-02-despacho-viaturas
```

## Estrutura da pasta

```text
grupo-02-despacho-viaturas/
├── README.md                  ← este arquivo (escopo, requisitos, estado)
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G0X-NN-*.md
├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G0X-NN-*.md
└── testes/                    ← CT-G0X-NN-*.md
```
