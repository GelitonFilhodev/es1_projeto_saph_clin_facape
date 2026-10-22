# G06 — Auditoria, Compliance e Indicadores

> Grupo responsável pelo subprocesso **Modelo de evento imutável, assinatura, indicadores e acesso a dado sensível** do SAPH-Clin.
> Módulo: M4 — Auditoria, Rastreabilidade e Conformidade

## Integrantes

| Nome | Matrícula | Papel no grupo |
| --- | --- | --- |
| *preencher* | | requisitos |
| *preencher* | | modelagem estrutural |
| *preencher* | | modelagem comportamental |
| *preencher* | | testes e rastreabilidade |

## Escopo do módulo (E1)

- **Subprocesso:** Modelo de evento imutável, assinatura, indicadores e acesso a dado sensível.
- **Atores envolvidos:** Auditor, Administrador, MedicoRegulador.
- **Entidades de domínio (donas do módulo):** `EventoAuditoria`, `AssinaturaDigital`, `Indicador`, `PerfilAcesso`, `AlertaCompliance`.
- **Entrada:** Contrato C5 `evento_sensivel` (G1 a G5).
- **Saída:** Trilha imutável, relatórios e alertas de conformidade.

### Fora do escopo do grupo

- executar a regulação, o despacho ou a reserva (módulos de origem).
- armazenar conteúdo clínico completo (só referência por identificador).
- definir stack tecnológica de armazenamento.

> Se algo do escopo acima for necessário, consuma o **contrato** descrito em
> `docs/arquitetura-modular.md` — não modele a entidade do vizinho.

## Casos de uso esperados (E3)

- UC-G06-01 Registrar Evento Sensível
- UC-G06-02 Consultar Trilha de Auditoria
- UC-G06-03 Assinar Conduta Excepcional
- UC-G06-04 Calcular Indicadores Operacionais
- UC-G06-05 Auditar Acesso a Prontuário

Use `docs/templates/caso-de-uso.md`. Mínimo: 4 casos de uso, sendo 2
especificados textualmente e pelo menos um `<<include>>` e um `<<extend>>`
justificados.

## Requisitos âncora (ponto de partida, não de chegada)

| ID | Requisito funcional | Caso de uso |
| --- | --- | --- |
| RF-G06-01 | Registrar evento imutável com ator, entidade, horário e resultado | UC-G06-01 |
| RF-G06-02 | Rejeitar qualquer alteração ou exclusão de evento registrado | UC-G06-01 |
| RF-G06-03 | Consultar trilha por chamado, ator e período | UC-G06-02 |
| RF-G06-04 | Assinar digitalmente condutas excepcionais e recusas | UC-G06-03 |
| RF-G06-05 | Calcular tempo de resposta e tempo porta-leito (RN-12) | UC-G06-04 |
| RF-G06-06 | Registrar todo acesso a prontuário como evento sensível (LGPD) | UC-G06-05 |
| RF-G06-07 | Emitir alerta de divergência de estoque e de reserva negada | UC-G06-04 |
| RF-G06-08 | Garantir idempotência por `evento_id` no reenvio | UC-G06-01 |

| ID | Requisito não funcional (com métrica) | Categoria |
| --- | --- | --- |
| RNF-G06-01 | Consulta de trilha de 30 dias em ≤ 5 s | desempenho |
| RNF-G06-02 | Evento gravado não pode ser alterado por nenhum perfil | integridade |
| RNF-G06-03 | Retenção mínima de 5 anos para eventos sensíveis | conformidade |
| RNF-G06-04 | Indicadores atualizados em janela de 15 min | desempenho |
| RNF-G06-05 | Acesso a dado sensível auditável e minimizado (LGPD art. 6º) | conformidade |

> Estes requisitos são **sementes** extraídas do contexto. O grupo deve
> refiná-los, dividir os compostos e acrescentar o que a análise revelar.
> Requisito copiado sem análise perde nota em profundidade.

## Eventos que o módulo publica para G06

- `TRILHA_CONSULTADA`
- `ASSINATURA_REGISTRADA`
- `ALERTA_COMPLIANCE`

## Riscos de modelagem conhecidos

- modelar auditoria como log de texto sem estrutura.
- deixar de definir o que não pode ser registrado (minimização).
- compilar indicador que não fecha com os eventos de origem.

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
python3 scripts/check_entrega.py --grupo grupo-06-auditoria-compliance
```

## Estrutura da pasta

```text
grupo-06-auditoria-compliance/
├── README.md                  ← este arquivo (escopo, requisitos, estado)
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G0X-NN-*.md
├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G0X-NN-*.md
└── testes/                    ← CT-G0X-NN-*.md
```
