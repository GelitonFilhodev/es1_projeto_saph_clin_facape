# G05 — Estoque de Fármacos Controlados

> Grupo responsável pelo subprocesso **Maletas de emergência, dispensação por lote, validade e reposição** do SAPH-Clin.
> Módulo: M3 — Gestão de Recursos Críticos e Estoque Finitivo

## Integrantes

| Nome | Matrícula | Papel no grupo |
| --- | --- | --- |
| *preencher* | | requisitos |
| *preencher* | | modelagem estrutural |
| *preencher* | | modelagem comportamental |
| *preencher* | | testes e rastreabilidade |

## Escopo do módulo (E1)

- **Subprocesso:** Maletas de emergência, dispensação por lote, validade e reposição.
- **Atores envolvidos:** EquipeIntervencao, FarmaceuticoHospitalar.
- **Entidades de domínio (donas do módulo):** `ItemEstoque`, `Lote`, `Maleta`, `MovimentacaoEstoque`, `AutorizacaoDispensacao`.
- **Entrada:** Contrato C4 `consumo_farmaco` (G3).
- **Saída:** Baixa por lote, solicitação de reposição e trava de item.

### Fora do escopo do grupo

- prescrever ou indicar conduta clínica (G3).
- controlar leitos (G4).
- compilar indicadores gerais (G6).

> Se algo do escopo acima for necessário, consuma o **contrato** descrito em
> `docs/arquitetura-modular.md` — não modele a entidade do vizinho.

## Casos de uso esperados (E3)

- UC-G05-01 Registrar Consumo em Campo
- UC-G05-02 Dispensar Controlado (`<<include>>` Validar Lote e Validade)
- UC-G05-03 Solicitar Reposição de Maleta
- UC-G05-04 Travar Item Suspeito ou Vencido
- UC-G05-05 Conciliar Estoque da Maleta

Use `docs/templates/caso-de-uso.md`. Mínimo: 4 casos de uso, sendo 2
especificados textualmente e pelo menos um `<<include>>` e um `<<extend>>`
justificados.

## Requisitos âncora (ponto de partida, não de chegada)

| ID | Requisito funcional | Caso de uso |
| --- | --- | --- |
| RF-G05-01 | Controlar estoque por item, lote e validade | UC-G05-01 |
| RF-G05-02 | Registrar dispensação com autor e vínculo ao prontuário | UC-G05-02 |
| RF-G05-03 | Bloquear dispensação de lote vencido ou travado (RN-08) | UC-G05-02 |
| RF-G05-04 | Exigir autorização farmacêutica para controlado (RN-07) | UC-G05-02 |
| RF-G05-05 | Gerar solicitação de reposição após consumo | UC-G05-03 |
| RF-G05-06 | Apontar divergência entre consumo registrado e estoque | UC-G05-05 |
| RF-G05-07 | Travessar item sob suspeita sanitária com motivo | UC-G05-04 |
| RF-G05-08 | Publicar eventos `CONTROLADO_DISPENSADO` e `ITEM_TRAVADO` | UC-G05-02 |

| ID | Requisito não funcional (com métrica) | Categoria |
| --- | --- | --- |
| RNF-G05-01 | Baixa de controlado registrada em ≤ 3 s em campo | desempenho |
| RNF-G05-02 | Rastreabilidade lote → paciente → profissional preservada | conformidade |
| RNF-G05-03 | Nenhuma dispensação sem autorização registrada | segurança |
| RNF-G05-04 | Alerta de vencimento com 30 dias de antecedência | usabilidade |
| RNF-G05-05 | Dados aderentes à Portaria SVS/MS 344/1998 e RDC 22/2014 | conformidade |

> Estes requisitos são **sementes** extraídas do contexto. O grupo deve
> refiná-los, dividir os compostos e acrescentar o que a análise revelar.
> Requisito copiado sem análise perde nota em profundidade.

## Eventos que o módulo publica para G06

- `CONTROLADO_DISPENSADO`
- `ITEM_TRAVADO`
- `ESTOQUE_CONCILIADO`

## Riscos de modelagem conhecidos

- modelar estoque apenas como quantidade (perde lote e validade).
- dispensação sem autorização registrada.
- não modelar o que acontece com sobra de controlado.

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
python3 scripts/check_entrega.py --grupo grupo-05-estoque-controlados
```

## Estrutura da pasta

```text
grupo-05-estoque-controlados/
├── README.md                  ← este arquivo (escopo, requisitos, estado)
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G0X-NN-*.md
├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G0X-NN-*.md
└── testes/                    ← CT-G0X-NN-*.md
```
