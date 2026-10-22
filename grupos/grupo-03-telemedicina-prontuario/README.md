# G03 — Telemedicina e Prontuário Pré-Hospitalar

> Grupo responsável pelo subprocesso **Teleorientação, ficha pré-hospitalar digital e pré-admissão** do SAPH-Clin.
> Módulo: M2 — Telemedicina Regulada e Prontuário Integrado

## Integrantes

| Nome | Matrícula | Papel no grupo |
| --- | --- | --- |
| *preencher* | | requisitos |
| *preencher* | | modelagem estrutural |
| *preencher* | | modelagem comportamental |
| *preencher* | | testes e rastreabilidade |

## Escopo do módulo (E1)

- **Subprocesso:** Teleorientação, ficha pré-hospitalar digital e pré-admissão.
- **Atores envolvidos:** MedicoRegulador, EquipeIntervencao, EquipeReceptora.
- **Entidades de domínio (donas do módulo):** `Teleorientacao`, `Prontuario`, `RegistroSinaisVitais`, `Procedimento`, `ConsumoFarmaco`, `PreAdmissao`.
- **Entrada:** Contrato C2 `despacho_ativo` (G2).
- **Saída:** Contrato C3 `pedido_pre_admissao` (G4) e C4 `consumo_farmaco` (G5).

### Fora do escopo do grupo

- decidir despacho (G2).
- aceitar ou negar reserva de leito (G4).
- dar baixa em estoque (G5).

> Se algo do escopo acima for necessário, consuma o **contrato** descrito em
> `docs/arquitetura-modular.md` — não modele a entidade do vizinho.

## Casos de uso esperados (E3)

- UC-G03-01 Registrar Teleorientação
- UC-G03-02 Preencher Ficha Pré-Hospitalar
- UC-G03-03 Solicitar Pré-Admissão (`<<include>>` Validar Prioridade)
- UC-G03-04 Registrar Recusa de Atendimento (`<<extend>>`, exige assinatura)

Use `docs/templates/caso-de-uso.md`. Mínimo: 4 casos de uso, sendo 2
especificados textualmente e pelo menos um `<<include>>` e um `<<extend>>`
justificados.

## Requisitos âncora (ponto de partida, não de chegada)

| ID | Requisito funcional | Caso de uso |
| --- | --- | --- |
| RF-G03-01 | Registrar teleorientação com autor, horário e destinatário | UC-G03-01 |
| RF-G03-02 | Registrar sinais vitais em campo com horário de coleta | UC-G03-02 |
| RF-G03-03 | Registrar procedimentos e fármacos administrados | UC-G03-02 |
| RF-G03-04 | Emitir pedido de pré-admissão com prioridade herdada da triagem | UC-G03-03 |
| RF-G03-05 | Registrar recusa de atendimento com assinatura e testemunha (RN-10) | UC-G03-04 |
| RF-G03-06 | Manter ficha disponível sem conexão e sincronizar depois | UC-G03-02 |
| RF-G03-07 | Restringir acesso à ficha por perfil e registrar cada acesso | UC-G03-02 |
| RF-G03-08 | Publicar eventos `TELEORIENTACAO_REGISTRADA` e `PRONTUARIO_ACESSADO` | UC-G03-01 |

| ID | Requisito não funcional (com métrica) | Categoria |
| --- | --- | --- |
| RNF-G03-01 | Ficha sincronizada em ≤ 5 s após reconexão | desempenho |
| RNF-G03-02 | Nenhum dado clínico perdido em queda de conexão durante o registro | confiabilidade |
| RNF-G03-03 | Dado clínico criptografado em repouso (LGPD) | segurança |
| RNF-G03-04 | Ficha utilizável em tablet com uma mão, alvos de toque ≥ 44 px | usabilidade |
| RNF-G03-05 | Telessaúde aderente à Res. CFM 2.314/2022 | conformidade |

> Estes requisitos são **sementes** extraídas do contexto. O grupo deve
> refiná-los, dividir os compostos e acrescentar o que a análise revelar.
> Requisito copiado sem análise perde nota em profundidade.

## Eventos que o módulo publica para G06

- `TELEORIENTACAO_REGISTRADA`
- `PRONTUARIO_ACESSADO`
- `RECUSA_ASSINADA`

## Riscos de modelagem conhecidos

- transformar a ficha em prontuário hospitalar completo (fora de escopo).
- recusa sem evidência de assinatura.
- pré-admissão recalculando prioridade em vez de herdar.

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
python3 scripts/check_entrega.py --grupo grupo-03-telemedicina-prontuario
```

## Estrutura da pasta

```text
grupo-03-telemedicina-prontuario/
├── README.md                  ← este arquivo (escopo, requisitos, estado)
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G0X-NN-*.md
├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G0X-NN-*.md
└── testes/                    ← CT-G0X-NN-*.md
```
