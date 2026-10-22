# G04 — Leitos Críticos e Reserva

> Grupo responsável pelo subprocesso **Oferta, reserva, bloqueio e liberação de leitos críticos** do SAPH-Clin.
> Módulo: M3 — Gestão de Recursos Críticos e Estoque Finitivo

## Integrantes

| Nome | Matrícula | Papel no grupo |
| --- | --- | --- |
| *preencher* | | requisitos |
| *preencher* | | modelagem estrutural |
| *preencher* | | modelagem comportamental |
| *preencher* | | testes e rastreabilidade |

## Escopo do módulo (E1)

- **Subprocesso:** Oferta, reserva, bloqueio e liberação de leitos críticos.
- **Atores envolvidos:** MedicoRegulador, EquipeReceptora.
- **Entidades de domínio (donas do módulo):** `Leito`, `Setor` (Sala Vermelha, Observação), `ReservaLeito`, `Higienizacao`, `AlertaTransferencia`.
- **Entrada:** Contrato C3 `pedido_pre_admissao` (G3).
- **Saída:** Reserva ativa + alerta à equipe receptora.

### Fora do escopo do grupo

- decidir prioridade clínica (G1).
- preencher ficha pré-hospitalar (G3).
- controlar insumos da maleta (G5).

> Se algo do escopo acima for necessário, consuma o **contrato** descrito em
> `docs/arquitetura-modular.md` — não modele a entidade do vizinho.

## Casos de uso esperados (E3)

- UC-G04-01 Consultar Disponibilidade de Leitos
- UC-G04-02 Reservar Leito (`<<include>>` Verificar Conflito de Reserva)
- UC-G04-03 Bloquear Leito por Motivo Sanitário
- UC-G04-04 Liberar Leito após Alta/Higienização
- UC-G04-05 Cancelar Reserva Expirada

Use `docs/templates/caso-de-uso.md`. Mínimo: 4 casos de uso, sendo 2
especificados textualmente e pelo menos um `<<include>>` e um `<<extend>>`
justificados.

## Requisitos âncora (ponto de partida, não de chegada)

| ID | Requisito funcional | Caso de uso |
| --- | --- | --- |
| RF-G04-01 | Manter estado explícito de cada leito (vago, reservado, ocupado, em higienização, bloqueado) | UC-G04-01 |
| RF-G04-02 | Reservar leito vinculado ao chamado e ao prontuário | UC-G04-02 |
| RF-G04-03 | Impedir duas reservas ativas no mesmo leito (RN-05) | UC-G04-02 |
| RF-G04-04 | Expirar reserva não confirmada após o prazo do ETA | UC-G04-05 |
| RF-G04-05 | Bloquear leito com motivo obrigatório e autor | UC-G04-03 |
| RF-G04-06 | Não ofertar leito em higienização ou bloqueado (RN-06) | UC-G04-01 |
| RF-G04-07 | Alertar equipe receptora no aceite da reserva | UC-G04-02 |
| RF-G04-08 | Publicar eventos `LEITO_RESERVADO` e `LEITO_NEGADO` | UC-G04-02 |

| ID | Requisito não funcional (com métrica) | Categoria |
| --- | --- | --- |
| RNF-G04-01 | Reserva confirmada em ≤ 2 s no pico de 20 req/min | desempenho |
| RNF-G04-02 | Zero reserva dupla em qualquer cenário de concorrência | consistência |
| RNF-G04-03 | Painel de leitos com defasagem máxima de 30 s | desempenho |
| RNF-G04-04 | Bloqueio sanitário visível em todos os pontos de consulta | usabilidade |
| RNF-G04-05 | Histórico de ocupação disponível para indicadores (G6) | conformidade |

> Estes requisitos são **sementes** extraídas do contexto. O grupo deve
> refiná-los, dividir os compostos e acrescentar o que a análise revelar.
> Requisito copiado sem análise perde nota em profundidade.

## Eventos que o módulo publica para G06

- `LEITO_RESERVADO`
- `LEITO_NEGADO`
- `LEITO_BLOQUEADO`

## Riscos de modelagem conhecidos

- tratar leito como quantidade ("4 vagos") em vez de entidade com estado.
- ignorar expiração de reserva (leito fica preso).
- permitir bloqueio sem autor e motivo.

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
python3 scripts/check_entrega.py --grupo grupo-04-leitos-criticos
```

## Estrutura da pasta

```text
grupo-04-leitos-criticos/
├── README.md                  ← este arquivo (escopo, requisitos, estado)
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G0X-NN-*.md
├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G0X-NN-*.md
└── testes/                    ← CT-G0X-NN-*.md
```
