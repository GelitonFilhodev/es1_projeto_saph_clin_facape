# Definição do Projeto — SAPH-Clin (2026.2)

> Documento oficial da disciplina. Versão PDF: [`definicao-projeto.pdf`](definicao-projeto.pdf).
> Este arquivo é a base contratual do escopo: o que não estiver aqui precisa de
> justificativa aprovada em ADR e registrada no PR.

## Visão Geral do Projeto

* **Nome do Sistema Sugerido:** **SAPH-Clin** (Sistema Integrado de Atendimento Pré-Hospitalar e Gestão Hospitalar Crítica)
* **Propósito:** Integrar a regulação e despacho de socorro móvel de emergência ao fluxo de recepção intra-hospitalar de uma clínica/hospital de média e alta complexidade, gerindo leitos críticos, insumos controlados e teleorientação em tempo real.
* **Problema a Resolver:** Eliminar o hiato de informação entre a equipe de rua e a equipe hospitalar, automatizar o controle de fármacos controlados consumidos em trânsito e otimizar o tempo de resposta em chamados críticos.

---

## Módulos do Sistema

### 1. Módulo de Regulação e Despacho de Urgência (Pré-Hospitalar)

* **Atendimento e Acolhimento:** Registro inicial da chamada (solicitante, localização, queixa principal).
* **Triagem Clínica e Priorização:** Classificação de risco pelo Protocolo de Manchester (Vermelho, Laranja, Amarelo, Verde, Azul).
* **Despacho Operacional:** Alocação de viaturas (USB – Unidade de Suporte Básico vs. USA – Unidade de Suporte Avançado/UTI móvel) conforme gravidade e proximidade.
* **Monitoramento de Estados:** Rastreio do ciclo de vida da ocorrência e dos veículos.

### 2. Módulo de Telemedicina Regulada e Prontuário Integrado

* **Teleorientação Pré-Chegada:** Registro de orientações dadas pelo médico regulador ao acompanhante/socorrista antes da viatura chegar.
* **Ficha Pré-Hospitalar Digital:** Preenchimento de sinais vitais, procedimentos e medicações ministradas no local do sinistro/trânsito.
* **Pré-Admissão Automática:** Transmissão dos dados pré-hospitalares para a recepção da clínica, reservando leito (Sala Vermelha ou Observação) antes da ambulância cruzar os portões.

### 3. Módulo de Gestão de Recursos Críticos e Estoque Finitivo

* **Gestão de Leitos Críticos:** Mapeamento em tempo real de leitos vagos, ocupados, em higienização ou bloqueados.
* **Dispensação e Reposição em Maletas:** Baixa de insumos e medicamentos controlados (sedativos, opioides) utilizados na viatura.
* **Controle de Validade e Lote:** Travamento de insumos vencidos ou sob suspeita sanitária.

### 4. Módulo de Auditoria, Rastreabilidade e Conformidade

* **Trilha de Auditoria (*Audit Trail*):** Log imutável de todas as ações sensíveis (quem regulou, quem despachou, quem aplicou morfina e quem liberou o leito).
* **Assinatura Digital de Termos:** Assinatura do médico regulador em condutas excepcionais e recusa de atendimento por parte de pacientes conscientes.
* **Indicadores de Desempenho:** Relatórios de tempo de resposta (*response time*), taxa de ocupação e consumo de fármacos.

---

## Principais Atores e Papéis

* **TASI (Telefonista Auxiliar de Regulação Médica):** Abre o chamado e coleta geolocalização e dados básicos.
* **Médico Regulador:** Decide a prioridade clínica, define o tipo de viatura, presta teleorientação e reserva o leito hospitalar.
* **Equipe de Intervenção (Médico/Enfermeiro/Condutor Socorrista):** Executa o atendimento em campo, registra sinais vitais e administra medicações.
* **Farmacêutico Hospitalar:** Audita o consumo das maletas de emergência e autoriza a reposição de itens controlados.
* **Recepção / Enfermagem da Sala Vermelha:** Recebe o alerta de transferência e prepara a equipe receptora.
* **Auditor / Administrador:** Acessa logs, métricas operacionais e relatórios regulatórios.

---

## Entregáveis do Projeto (Foco em ES1)

### Entregável 1: Engenharia de Requisitos

* **Documento de Visão e Escopo:** Limites do sistema, premissas e restrições legais (CFM e ANVISA).
* **Catálogo de Requisitos:** Lista de Requisitos Funcionais (RF) e Requisitos Não-Funcionais (RNF — desempenho, conformidade LGPD, segurança e disponibilidade).
* **Diagrama de Casos de Uso (Geral e Específicos):**
* Uso intensivo de `<<include>>` (ex: *Despachar Viatura* `<<include>>` *Verificar Disponibilidade de Equipe*).
* Uso intensivo de `<<extend>>` (ex: *Registrar Atendimento Móvel* `<<extend>>` *Acionar Suporte Avançado* caso haja PCR).

* **Especificação Textual de Casos de Uso:** Passo a passo detalhado (Fluxo Principal, Alternativo e de Exceção) de pelo menos 3 fluxos críticos.

### Entregável 2: Modelagem Estrutural

* **Diagrama de Classes de Domínio:** Entidades (`Viatura`, `Chamado`, `Triagem`, `Prontuario`, `ItemEstoque`, `Leito`), atributos, multiplicidades e heranças (ex: `ViaturaUSA` herda de `Viatura`).
* **Dicionário de Dados:** Descrição semântica das classes e seus relacionamentos.

### Entregável 3: Modelagem Comportamental e Dinâmica

* **Diagramas de Sequência:**

1. *Fluxo de Regulação e Despacho de Emergência* (TASI $\rightarrow$ Médico Regulador $\rightarrow$ Despachante $\rightarrow$ Viatura).
2. *Fluxo de Pré-Alocação de Leito e Passagem de Plantão Digital* (Viatura $\rightarrow$ Sistema $\rightarrow$ Sala Vermelha).

* **Diagrama de Máquina de Estados:**

1. Ciclo de vida da **Viatura** (`Disponível`, `Deslocando para Sinistro`, `No Local`, `Em Trânsito p/ Hospital`, `Em Descontaminação/Reposição`).
2. Ciclo de vida do **Chamado** (`Aberto`, `Em Triagem`, `Viatura Despachada`, `Em Atendimento`, `Encerrado`, `Cancelado`).

* **Diagrama de Atividades:** O fluxo de decisão da Triagem de Risco (Manchester) e desvio para telemedicina em caso de indisponibilidade de viatura.

### Entregável 4: Rastreabilidade e Validação Teórica

* **Matriz de Rastreabilidade:** Mapeamento ligando Requisitos Funcionais $\rightarrow$ Casos de Uso $\rightarrow$ Classes $\rightarrow$ Diagramas de Sequência.
* **Protótipos de Baixa Fidelidade (Wireframes/Mockups Conceituais):** Telas da Central de Regulação (painel de viaturas) e Ficha Móvel de Atendimento em tablet.
