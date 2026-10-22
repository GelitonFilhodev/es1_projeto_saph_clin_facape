# Requisitos de Entrega — AV2 (SAPH-Clin, 2026.2)

Este documento traduz a [definição do projeto](definicao-projeto.md) em
**diretrizes de execução**: o que cada grupo entrega, como é avaliado e quais
marcos existem. O domínio está em [`contexto-do-sistema.md`](contexto-do-sistema.md);
as fronteiras entre grupos, em [`arquitetura-modular.md`](arquitetura-modular.md).

---

## 1. Organização do Trabalho

**Formato:** 6 grupos, 6 subprocessos, desenvolvimento **modular e paralelo**.
Cada grupo é responsável por **um módulo completo** — não por uma etapa de um
processo sequencial.

Consequências práticas:

- Nenhum grupo espera outro entregar para começar (contrato fechado em
  [`arquitetura-modular.md`](arquitetura-modular.md)).
- O resultado final é a **soma coerente** dos seis módulos, não seis trabalhos
  independentes sobre o mesmo sistema.
- Coerência entre módulos é avaliada: contrato violado sem ADR = perda de nota dos
  dois grupos envolvidos.

### Estrutura obrigatória da pasta do grupo

```text
grupos/grupo-XX-nome/
├── README.md                  ← estado atual, integrantes, decisões resumidas
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G0X-NN-*.md (um arquivo por caso de uso)
├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G0X-NN-*.md
└── testes/                    ← CT-G0X-NN-*.md
```

A CI (`scripts/check_entrega.py`) valida essa estrutura antes de o professor
revisar.

---

## 2. Entregáveis Obrigatórios (7 por grupo)

### E1 · Visão e Escopo do Módulo

Uma página em `README.md` respondendo: qual problema do SAPH-Clin este módulo
resolve, onde ele **começa** e **termina** (fronteiras), o que está fora do
escopo e quais premissas foram adotadas.

### E2 · Catálogo de Requisitos

- Mínimo **8 RF** com identificador `RF-G0X-NN`, ator, descrição e critério de aceite.
- Mínimo **5 RNF** com identificador `RNF-G0X-NN`, **métrica e alvo** (não adjetivo).
  Exemplo: "reserva de leito confirmada em ≤ 2 s no pico de 20 req/min".
- Classificação de cada RNF: desempenho, segurança, disponibilidade, usabilidade,
  conformidade ou manutenibilidade.

### E3 · Casos de Uso e Especificação Textual

- Diagrama de casos de uso do módulo (fonte + export).
- **Mínimo 4 casos de uso**, com pelo menos **um `<<include>>`** e **um `<<extend>>`**
  justificados.
- **Mínimo 2 casos de uso especificados textualmente** (fluxo principal,
  alternativos e de exceção, pré e pós-condições, RFs rastreados).
- Cada grupo precisa de **pelo menos um fluxo crítico completo** — o conjunto dos
  seis grupos cobre os três fluxos exigidos pela definição do projeto.

### E4 · Modelagem Estrutural

- Diagrama de classes de domínio do módulo (fonte + export), com atributos,
  multiplicidades e herança quando houver (ex.: `ViaturaUSA` herda de `Viatura`).
- **Dicionário de dados**: para cada classe, significado, atributos relevantes,
  restrições e relacionamentos.
- Entidades compartilhadas aparecem no módulo **dono**; os demais referenciam por
  identificador (não duplicam a classe).

### E5 · Modelagem Comportamental

- **Mínimo 2 diagramas de sequência** (um deles obrigatoriamente um fluxo de
  exceção ou de indisponibilidade).
- **Máquina de estados** do ciclo de vida central do módulo (Chamado, Viatura,
  Leito, Lote — conforme o grupo).
- **Diagrama de atividades** quando o módulo tiver decisão de fluxo
  (ex.: triagem de risco, conciliação de estoque).

### E6 · Decisões, Rastreabilidade e Testes

- **Mínimo 2 ADRs** (`ADR-G0X-NN`) no formato contexto → decisão → alternativas →
  consequências.
- **Matriz de rastreabilidade** completa: `RF → UC → Classe → Sequência → CT`.
  Requisito sem rastreio é requisito não entregue.
- **Mínimo 4 casos de teste** (`CT-G0X-NN`), incluindo **1 caso de fronteira**
  (limite, duplicidade ou concorrência).

### E7 · Protótipos e Relatório Técnico

- **Mínimo 2 wireframes de baixa fidelidade** (fonte editável + imagem).
- Relatório técnico curto no `README.md`: decisões, dificuldades, limitações
  conhecidas e o que faria diferente com mais tempo.

---

## 3. Critérios de Avaliação (rubrica)

| Critério | Peso | O que é observado |
| --- | --- | --- |
| Engenharia de requisitos (E1–E3) | 20% | RF claros, RNF mensuráveis, casos de uso com include/extend justificados |
| Modelagem estrutural (E4) | 20% | classes de domínio (não técnicas), multiplicidades corretas, dicionário |
| Modelagem comportamental (E5) | 20% | sequência coerente com o texto, estados completos, exceções modeladas |
| Rastreabilidade e testes (E6) | 15% | matriz sem buracos, testes com fronteira, ADRs com consequências |
| Protótipos e relatório (E7) | 10% | wireframe fixa estrutura e não estética; limitações declaradas |
| Qualidade da entrega no Git | 10% | commits padronizados, PR completo, escopo respeitado, CI verde |
| Coerência entre módulos | 5% | contrato respeitado ou alteração via ADR |

**Bônus (até 0,5 ponto):** módulo com rastreio até indicador de G6 (o requisito
aparece em um indicador operacional real).

---

## 4. Marcos

| Marco | Aula | Entrega esperada | Consequência de não entregar |
| --- | --- | --- | --- |
| **M1** | 18 | E1, E2, E3 v1.0 (escopo, RF/RNF, casos de uso) | Retrabalho de escopo; nota de requisitos comprometida |
| **M2** | 24 | E4, E5, E6 parcial (classes, sequência, estados, ADRs) | Modelagem estrutural não avaliada |
| **M3** | 27 | E6, E7 completos + PR final verde | Sem direito a ajuste antes da banca |
| **M4** | 29–30 | Defesa pública do módulo | Nota do projeto conforme rubrica |

Cada marco é um **PR separado** com título `[G0X] Entrega M1 — <nome do módulo>`.

---

## 5. Penalidades Explícitas

| Situação | Efeito |
| --- | --- |
| Arquivo fora de `grupos/grupo-XX-*/` | PR reprovado pela CI (bloqueia merge) |
| Diagrama sem fonte editável | artefato não conta |
| Requisito sem rastreio na matriz | item desconsiderado na avaliação |
| RNF sem métrica ("deve ser rápido") | RNF não pontua |
| Caso de uso sem fluxo de exceção | perde profundidade em E3 |
| Plágio entre grupos (mesmo diagrama com outro nome) | nota zero para ambos no item |
| Commit de outro integrante sem contribuição real | avaliado como não participação |

---

## 6. Regras de Coerência entre Grupos

1. **Identificador de entidade compartilhada** é definido pelo grupo dono
   (ex.: `chamado_id` é de G1). Outros grupos referenciam, não redefinem.
2. **Mudança de contrato** exige ADR e menção no PR dos grupos afetados.
3. **Nome de ator** segue o glossário: `TASI`, `MedicoRegulador`, `EquipeIntervencao`,
   `FarmaceuticoHospitalar`, `EquipeReceptora`, `Auditor`.
4. **Prioridade clínica** é sempre do G1; ninguém "recalcula" prioridade.
5. **Auditoria** é sempre do G6; ninguém cria trilha paralela.

---

## 7. Declaração de Uso de IA

Obrigatória no PR. Informe: artefatos apoiados, ferramenta e o que o grupo revisou.
Conteúdo normativo (`Portaria`, `RDC`, `Resolução`) exige **verificação humana** da
redação vigente — citar lei desatualizada é erro de requisito, não "erro da IA".

---

## 8. Perguntas Frequentes

**Podemos usar PlantUML, draw.io ou Astah?**
Sim. O requisito é fonte editável + exportação legível.

**Precisamos implementar o sistema?**
Não. O produto é modelagem, especificação, teste (casos) e protótipo.

**Podemos trocar de grupo?**
Somente antes do M1, com aviso ao professor e registro no README dos dois grupos.

**O módulo pode ter mais de um diagrama de classes?**
Sim, se houver subdomínios distintos (ex.: estoque e maleta). Mantenha a
coerência interna e a rastreabilidade.

**Um grupo pode entregar artefato de outro módulo?**
Não. Se o artefato pertence a outro grupo, abra issue com a evidência.
