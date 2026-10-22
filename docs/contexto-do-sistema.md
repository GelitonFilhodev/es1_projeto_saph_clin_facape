# Contexto do Sistema — SAPH-Clin

> Documento-base de domínio para o projeto da disciplina.
> Consolida problema, escopo, atores, regras de negócio e restrições normativas
> derivados da definição do projeto ([`definicao-projeto.md`](definicao-projeto.md)).
> É referência **conceitual comum** aos seis grupos — não é o documento de
> planejamento da execução (esse é [`requisitos-entrega-av2.md`](requisitos-entrega-av2.md)).

## Como usar este documento

- Use para entender **o serviço real** que o sistema apoia.
- Use [`glossario-base.md`](glossario-base.md) para alinhar vocabulário entre grupos.
- Use [`temas-grupos.md`](temas-grupos.md) para saber onde o seu módulo começa e termina.
- Use [`arquitetura-modular.md`](arquitetura-modular.md) para os contratos de dados.
- Regra de negócio sem fonte aqui (ou em norma citada) é **suposição**: registre como ADR.

---

## 1. Visão Geral

O SAPH-Clin apoia a operação de um serviço de atendimento pré-hospitalar móvel
(SAMU municipal ou privado) integrado a um hospital de média/alta complexidade.
O serviço funciona 24 horas, com demanda imprevisível e **custo assimétrico de
erro**: subestimar a gravidade de um chamado mata; superestimar consome a única
viatura disponível e atrasa outro atendimento.

O sistema acompanha a ocorrência do primeiro toque no telefone até a entrega do
paciente ao leito hospitalar:

```text
Ligação → Acolhimento → Triagem (Manchester) → Despacho → Atendimento em campo
   → Teleorientação → Ficha pré-hospitalar → Pré-admissão → Leito
```

Em cada etapa existem três perguntas de engenharia:

1. **Quem decide?** (competência e responsabilidade legal)
2. **O que precisa estar registrado?** (evidência auditável)
3. **O que acontece se falhar?** (fluxo de exceção explícito)

---

## 2. Problema Central

| Gargalo atual | Impacto operacional | Efeito no sistema |
| --- | --- | --- |
| Informação clínica em papel/rádio | Recepção redigita tudo na chegada | Ficha pré-hospitalar digital e pré-admissão |
| Triagem informal por telefone | Prioridade inconsistente entre plantões | Classificação de risco registrada e auditável |
| Alocação de viatura por memória | USA enviada a caso leve; USB a caso grave | Despacho por gravidade × proximidade com justificativa |
| Leito reservado por telefone | Reserva dupla em pico; paciente esperando maca | Reserva transacional com estado explícito do leito |
| Consumo de controlado em papel | Divergência de estoque e risco sanitário | Baixa por lote com autorização do farmacêutico |
| Sem trilha de decisão | Impossível provar quem autorizou o quê | Audit trail imutável de eventos sensíveis |

---

## 3. Escopo

### ✅ Dentro do escopo

- Registro e classificação de risco do chamado (Protocolo de Manchester).
- Despacho de viaturas USB/USA com rastreio do ciclo de vida.
- Teleorientação do médico regulador e ficha pré-hospitalar digital.
- Pré-admissão: reserva de leito crítico antes da chegada.
- Gestão de leitos (Sala Vermelha, Observação) com estados e bloqueios.
- Controle de maletas, lotes, validade e dispensação de controlados.
- Trilha de auditoria, assinatura de condutas excepcionais e indicadores.
- Protótipos de baixa fidelidade das telas críticas.

### ❌ Fora do escopo

- Prontuário hospitalar definitivo e prescrição intra-hospitalar.
- Faturamento, convênios e faturamento SUS.
- Escala de plantão e folha de pagamento.
- Motor de otimização logística em tempo real (roteirização avançada).
- Integração efetiva com sistemas externos (o contrato é **modelado**, não implementado).
- Aplicativo nativo: o alvo é a modelagem e o protótipo conceitual.

> **Fronteira importante:** tudo que é "integração" nesta disciplina é modelado
> como **contrato de interface** (entrada, saída, erros), não como código funcional.

---

## 4. Atores e Responsabilidades

| Ator | Responsabilidade | Decisão crítica |
| --- | --- | --- |
| **TASI** (Telefonista Auxiliar de Regulação Médica) | Abre o chamado, coleta localização e queixa | Nenhuma decisão clínica |
| **Médico Regulador** | Classifica risco, define viatura, teleorienta, reserva leito | Gravidade e destino |
| **Equipe de Intervenção** (médico/enfermeiro/condutor) | Atende em campo, registra sinais vitais, administra fármacos | Conduta no local |
| **Farmacêutico Hospitalar** | Audita consumo das maletas, autoriza reposição | Liberação de controlado |
| **Recepção / Enfermagem da Sala Vermelha** | Recebe alerta de transferência, prepara equipe | Aceite do leito |
| **Auditor / Administrador** | Consulta logs, indicadores e conformidade | Acesso a dado sensível |

---

## 5. Regras de Negócio (base do catálogo de requisitos)

| ID | Regra | Consequência se violada |
| --- | --- | --- |
| RN-01 | Todo chamado recebe classificação de risco em até 4 minutos do acolhimento. | Perda de prioridade e risco de óbito evitável |
| RN-02 | A prioridade é do protocolo, nunca sobrescrita silenciosamente. Reclassificação exige justificativa e autor. | Triagem arbitrária, não auditável |
| RN-03 | Viatura USA só é despachada com equipe de suporte avançado completa. | Despacho ilegal/inseguro |
| RN-04 | Uma viatura não pode estar em dois despachos ativos. | Dupla alocação; chamado sem socorro |
| RN-05 | Um leito não pode ter duas reservas ativas. | Reserva dupla em pico |
| RN-06 | Leito em higienização ou bloqueado não é ofertado. | Infecção cruzada / uso indevido |
| RN-07 | Fármaco controlado só é dispensado com lote válido e autorização registrada. | Risco sanitário e legal |
| RN-08 | Item vencido ou sob suspeita sanitária é travado para uso imediato. | Evento adverso grave |
| RN-09 | Toda ação sensível gera evento imutável (autor, ação, entidade, horário). | Perda de prova legal |
| RN-10 | Recusa de atendimento por paciente consciente exige assinatura e testemunha. | Questionamento jurídico |
| RN-11 | Dado clínico só é acessível a papel com necessidade de atendimento (LGPD). | Vazamento de dado sensível |
| RN-12 | Indicadores usam tempo de resposta do chamado ao leito, não apenas do chamado à chegada. | Métrica enganosa de qualidade |

---

## 6. Restrições Normativas

| Referência | Efeito no sistema |
| --- | --- |
| Portaria MS/GM 2.048/2002 | Estrutura de regulação médica, classificação de risco e transporte |
| Protocolo de Manchester | Cores e critérios de priorização clínica |
| LGPD (Lei 13.709/2018) | Dado de saúde é sensível: minimização, finalidade, registro de acesso |
| Lei 14.510/2022 + Res. CFM 2.314/2022 | Base legal para teleorientação/telemedicina |
| Portaria SVS/MS 344/1998 + RDC ANVISA 22/2014 | Controle especial de fármacos e notificação (SNGPC) |
| RDC ANVISA 301/2019 | Boas práticas de transporte e conservação de medicamentos |

> Verifique a redação vigente antes de transformar a norma em requisito.
> Um requisito normativo mal citado contamina todo o trabalho a jusante.

---

## 7. Restrições de Projeto

- **Prazo:** marcos M1–M4 definidos em [`requisitos-entrega-av2.md`](requisitos-entrega-av2.md).
- **Escopo paralelo:** seis grupos independentes — o sistema é decomposto por
  **fronteiras de módulo**, não por etapas sequenciais.
- **Sem código de produção:** o produto é modelagem, especificação e protótipo.
- **Ferramentas livres** (draw.io, PlantUML, Astah, Figma, Excalidraw), desde que
  a **fonte editável** acompanhe a exportação.
- **Ambiguidade é esperada:** a resposta correta é registrar a decisão em ADR,
  nunca inventar regra silenciosamente.

---

## 8. Perguntas de Domínio em Aberto

Estas perguntas devem ser respondidas pelo grupo no relatório técnico (com ADR
quando a decisão for estrutural):

1. Qual o tempo máximo aceitável entre acolhimento e despacho para caso Vermelho?
2. Quem pode cancelar um chamado em atendimento e qual evidência fica registrada?
3. Se não houver viatura, como o desvio para teleorientação é registrado?
4. O que acontece quando a viatura chega e o leito reservado foi bloqueado?
5. Como o consumo de um controlado é conciliado com o estoque da maleta?
6. Quem tem autoridade para reclassificar prioridade e como isso é auditado?
7. Que eventos precisam ser provados três anos depois de uma ocorrência?
