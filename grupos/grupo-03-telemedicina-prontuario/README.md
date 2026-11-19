# G03: Telemedicina e Prontuário Pré-Hospitalar

> Grupo responsável pelo subprocesso **Teleorientação, ficha pré-hospitalar digital e pré-admissão** do SAPH-Clin.
> Módulo: M2, Telemedicina Regulada e Prontuário Integrado.

## Integrantes

| Nome | Matrícula |
| --- | --- |
| Tulio Alves Torres | 26831 |
| Geliton Fernandes de Almeida Filho | 26643 |
| Luccas Amaro de Castro Alencar | (matrícula) |

---

## E1. Visão e escopo do módulo

### Problema que o módulo resolve

A informação clínica produzida na rua não chega estruturada ao hospital: a recepção redigita tudo na chegada e o leito crítico é aberto tarde. O G03 resolve o trecho **clínico** desse hiato: registra a orientação médica a distância, mantém a ficha pré-hospitalar digital preenchida pela equipe em campo e dispara a pré-fase de admissão, para que o hospital se prepare antes de a viatura chegar.

### Onde começa e onde termina

- **Começa** quando recebe o contrato **C2 `despacho_ativo`** (de G02): há uma equipe em atendimento e a ficha é aberta.
- **Termina** quando entrega o contrato **C3 `pedido_pre_admissao`** (a G04) e registra o retorno (reservado ou negado), deixando a ficha disponível para a EquipeReceptora. Termina também com o contrato **C4 `consumo_farmaco`** (a G05) e com os eventos a G06 (C5).

### Entidades donas do módulo

`Teleorientacao`, `Prontuario`, `RegistroSinaisVitais`, `Procedimento`, `ConsumoFarmaco`, `PreAdmissao`. Candidata adicional, a confirmar no E4: `RecusaAtendimento`.

> `Prontuario` neste módulo significa **ficha pré-hospitalar**, não o prontuário hospitalar definitivo (fora de escopo).

### Dentro do escopo

- Registro de teleorientação do médico regulador.
- Ficha pré-hospitalar: sinais vitais, procedimentos e fármacos administrados.
- Pedido de pré-admissão com prioridade herdada e registro do retorno.
- Recusa de atendimento com assinatura e testemunha.
- Uso da ficha sem conexão e sincronização posterior.
- Restrição de acesso por perfil e registro de cada acesso.

### Fora do escopo

- Decidir despacho (G02).
- Calcular ou reclassificar prioridade (G01).
- Aceitar ou negar reserva de leito (G04).
- Dar baixa em estoque, validar lote e validade (G05).
- Manter trilha de auditoria, assinatura digital e indicadores (G06).
- Prontuário hospitalar definitivo, prescrição intra-hospitalar, faturamento.
- Implementação de código, API ou banco de dados (o produto é modelagem).

### Contratos

| Contrato | Sentido | Uso no G03 |
| --- | --- | --- |
| C2 `despacho_ativo` | G02 para G03 | abre a ficha e habilita UC-G03-01 e UC-G03-02 |
| C3 `pedido_pre_admissao` | G03 para G04 | UC-G03-03; retorno `reservado` ou `negado` com motivo |
| C4 `consumo_farmaco` | G03 para G05 | UC-G03-02, ao registrar cada fármaco administrado |
| C5 `evento_sensivel` | G03 para G06 | `TELEORIENTACAO_REGISTRADA`, `PRONTUARIO_ACESSADO`, `RECUSA_ASSINADA` |

### Premissas adotadas

| ID | Premissa |
| --- | --- |
| P-01 | A ficha pré-hospitalar é o registro clínico da fase pré-hospitalar, sem substituir o prontuário hospitalar. |
| P-02 | A teleorientação é vinculada a chamado com despacho ativo (C2); o caso sem viatura fica em Q-01. |
| P-03 | A prioridade é lida do chamado (dono: G01) por `chamado_id`; o G03 nunca calcula, digita nem altera (RN-02). |
| P-04 | O registro clínico nunca é bloqueado por regra de estoque: o G03 registra o que foi administrado e o G05 concilia (RN-07 e RN-08 são de G05). |
| P-05 | O MedicoRegulador decide a necessidade de leito e emite o pedido; a EquipeIntervencao fornece os dados da ficha. |
| P-06 | Auditor e Administrador não acessam conteúdo clínico, apenas a trilha de acessos em G06 (interpretação de RN-11). |
| P-07 | Há um hospital integrado; o desvio após leito negado é decisão humana do médico regulador, registrada como justificativa na ficha, sem integração com outro serviço. |
| P-08 | A recusa exige assinatura do paciente, testemunha (RN-10) e confirmação do médico regulador (definição do projeto, módulo 4). |
| P-09 | Só o tablet da equipe opera offline; a central do médico regulador é considerada sempre conectada. |
| P-10 | Eventos carregam o horário do fato, não do envio (arquitetura modular, seção 6). |

### Perguntas em aberto (para o professor ou ADR no M2)

| ID | Pergunta | Destino |
| --- | --- | --- |
| Q-01 | Como registrar teleorientação quando não há viatura? O C2 cobre esse caso ou o contrato precisa de ADR com G02? (pergunta de domínio 3) | professor, G02 |
| Q-02 | O C2 não traz `prioridade`, mas o C3 exige. Aceita-se a leitura por `chamado_id` (P-03) ou o C2 é ampliado? | professor, G01, G02 |
| Q-03 | O C3 exige `eta_hospital`, que nenhum contrato fornece. Assume-se informado pela equipe ou pelo regulador. Está correto? | professor |
| Q-04 | Na recusa, RN-10 fala em assinatura e testemunha; a definição cita assinatura do médico regulador. Quem assina o quê? (P-08 reúne os três) | professor |
| Q-05 | Recusa de menor ou incapaz, com representante legal, entra no escopo? | professor |
| Q-06 | Qual o prazo de guarda da ficha? Exige verificação da norma vigente antes de virar requisito. | professor |
| Q-07 | Qual o conjunto mínimo obrigatório de sinais vitais? (proposta no RF-G03-02) | professor |
| Q-08 | Como alterar ou cancelar um pedido ativo (por exemplo, mudar de Observação para Sala Vermelha) sem reserva dupla? Exige contrato com G04. | G04 |
| Q-09 | O C3 não tem identificador do pedido. Reenvio idempotente exige `pre_admissao_id`; propor ADR de alteração de contrato? | G04 |
| Q-10 | A telessaúde exige consentimento livre e esclarecido do paciente ou do representante legal (Lei 14.510/2022, que inseriu o art. 26-G, I, na Lei 8.080/1990; Res. CFM 2.314/2022). Em emergência, com paciente inconsciente, registra-se o consentimento ou a justificativa de impossibilidade? | professor |

### Restrições normativas (a confirmar na redação vigente)

- **Res. CFM 2.314/2022** (telemedicina): o atendimento por telemedicina consta de registro em prontuário, com guarda, integridade, veracidade, confidencialidade, privacidade e irrefutabilidade.
- **Lei 14.510/2022**: base legal da telessaúde; exige consentimento livre e esclarecido do paciente ou do representante legal (ver Q-10).
- **LGPD (Lei 13.709/2018)**: dado de saúde é dado pessoal sensível (art. 5º, II); minimização (art. 6º, III); registro das operações de tratamento (art. 37).

---

## E2. Catálogo de requisitos

Os requisitos âncora do professor foram refinados: os compostos foram divididos e o que a análise revelou foi acrescentado. As origens estão na coluna **Fonte**.

### Requisitos funcionais

| ID | Ator | Descrição | Critério de aceite | UC | Fonte |
| --- | --- | --- | --- | --- | --- |
| RF-G03-01 | MedicoRegulador | Registrar teleorientação com autor, horário do fato, horário do registro, destinatário e conteúdo, vinculada a chamado e despacho | Não grava sem os cinco campos; exige despacho ativo; guarda os dois horários separados | UC-G03-01 | âncora RF-01; definição (Teleorientação Pré-Chegada); Res. CFM 2.314/2022 |
| RF-G03-02 | EquipeIntervencao | Registrar sinais vitais em campo com horário de coleta; permitir "não aferível" com justificativa. Conjunto mínimo proposto: frequência cardíaca, frequência respiratória, pressão arterial, saturação de oxigênio, temperatura e nível de consciência (Q-07) | Cada registro tem autor e horário de coleta; novo registro não apaga o anterior; o último é identificável | UC-G03-02 | âncora RF-02; definição (Ficha Pré-Hospitalar) |
| RF-G03-03 | EquipeIntervencao | Registrar procedimentos realizados em campo (tipo, horário, executor) | Todo procedimento tem os três campos e fica vinculado à ficha | UC-G03-02 | âncora RF-03 (parte procedimentos) |
| RF-G03-04 | MedicoRegulador | Emitir pedido de pré-admissão com prioridade herdada da triagem, necessidade de leito, último sinal vital e ETA ao hospital | Prioridade do C3 igual à vigente do chamado e não editável; sem sinal vital ou ETA o envio é bloqueado; um pedido ativo por chamado | UC-G03-03, UC-G03-05 | âncora RF-04; RN-02; contrato C3 |
| RF-G03-05 | EquipeIntervencao | Registrar recusa de atendimento de paciente consciente com assinatura do paciente, testemunha e confirmação do médico regulador | Sem as três evidências a recusa fica `Incompleta` e não gera `RECUSA_ASSINADA`; revogação preserva a recusa | UC-G03-04 | âncora RF-05; RN-10; definição (Assinatura Digital) |
| RF-G03-06 | EquipeIntervencao | Manter a ficha disponível para registro sem conexão | Todos os registros possíveis online são possíveis offline; a confirmação ocorre só após gravar localmente | UC-G03-02, UC-G03-04, UC-G03-07 | âncora RF-06 (parte offline); pergunta "se a rede cair no local" |
| RF-G03-07 | Sistema | Restringir o acesso à ficha por perfil com necessidade de atendimento | Perfil sem necessidade recebe negação; Auditor não vê conteúdo clínico (P-06) | UC-G03-08, UC-G03-02, UC-G03-06 | âncora RF-07 (parte restrição); RN-11; LGPD |
| RF-G03-08 | Sistema | Publicar a G06 os eventos `TELEORIENTACAO_REGISTRADA`, `PRONTUARIO_ACESSADO` e `RECUSA_ASSINADA` pelo contrato C5 | Cada fato gera um evento com `evento_id` único, horário do fato e resultado; reenvio não duplica | UC-G03-01, UC-G03-04, UC-G03-08 | âncora RF-08 (a âncora omite `RECUSA_ASSINADA`, listado nos eventos do módulo); RN-09 |
| RF-G03-09 | EquipeIntervencao | Registrar cada fármaco administrado (item da maleta, lote, quantidade, via, horário, responsável) | Os seis campos são obrigatórios; lote ilegível é registrado como "lote não identificado" com justificativa, sem bloquear (P-04) | UC-G03-02 | âncora RF-03 (parte fármacos); contrato C4 |
| RF-G03-10 | Sistema | Registrar cada acesso à ficha (leitura e alteração, permitido ou negado) com ator, papel, horário e resultado | Todo acesso gera registro; tentativa negada também | UC-G03-08, UC-G03-06 | âncora RF-07 (parte registro); RN-11; LGPD art. 37 |
| RF-G03-11 | Sistema | Sincronizar automaticamente os registros pendentes na reconexão, sem duplicar e preservando o horário do fato | Reenvio do mesmo registro não cria duplicata; registro rejeitado é retido, nunca descartado | UC-G03-07 | âncora RF-06 (parte sincronização); arquitetura modular, seção 6 |
| RF-G03-12 | Sistema | Publicar o consumo de fármaco a G05 pelo contrato C4 a cada administração registrada | C4 contém os campos obrigatórios; falha de G05 mantém o consumo pendente e reentrega, sem bloquear o atendimento | UC-G03-02 | contrato C4; arquitetura modular, seção 6 |
| RF-G03-13 | Sistema | Registrar o retorno de G04 ao pedido (reservado ou negado com motivo) e alertar o regulador em caso de negativa, permitindo novo pedido ligado ao anterior | Todo pedido tem desfecho registrado e contável; negada exibe o motivo | UC-G03-03 | contrato C3 (falha de contrato); indicador "taxa de reserva negada" |
| RF-G03-14 | EquipeReceptora | Consultar a ficha em modo leitura (passagem de plantão digital) após a pré-admissão | Mostra sinais vitais, procedimentos, fármacos, teleorientações, recusa e pedido; sem edição | UC-G03-06 | definição (sequência de passagem de plantão digital) |
| RF-G03-15 | EquipeIntervencao | Corrigir registro da ficha preservando o original, o autor e o horário da correção | Original permanece consultável; a correção exige justificativa | UC-G03-02 | decisão do grupo (a formalizar em ADR no M2); integridade e irrefutabilidade (Res. CFM 2.314/2022); RN-09 |

### Requisitos não funcionais

| ID | Categoria | Requisito (métrica e alvo) | Como será verificado | Fonte |
| --- | --- | --- | --- | --- |
| RNF-G03-01 | desempenho | Ficha sincronizada em até 5 s (percentil 95) após a reconexão, com até 30 registros pendentes | caso de teste de fronteira com 30 registros pendentes | âncora RNF-01; cenário de carga proposto pelo grupo |
| RNF-G03-02 | disponibilidade | 0 (zero) registros clínicos perdidos em queda de conexão durante o registro; a gravação local ocorre antes de confirmar ao usuário | caso de teste que simula queda em cada etapa; contagem de perdas igual a 0 | âncora RNF-02 (reclassificada de "confiabilidade", categoria fora da lista da disciplina) |
| RNF-G03-03 | segurança | 100% dos campos clínicos marcados como protegidos no dicionário de dados são criptografados em repouso, inclusive no armazenamento local do tablet | inspeção do dicionário de dados (E4), sem exceções | âncora RNF-03; LGPD (dado sensível) |
| RNF-G03-04 | usabilidade | Ficha utilizável em tablet com uma mão, com alvos de toque de pelo menos 44 px | inspeção dos wireframes (E7) | âncora RNF-04 |
| RNF-G03-05 | conformidade | 100% das teleorientações registradas em prontuário com autor identificado (nome e CRM), horário e vínculo ao chamado, sem edição sem versão | checklist de conformidade aplicado aos casos de teste de UC-G03-01; revisão da redação vigente da Res. CFM 2.314/2022 | âncora RNF-05, reescrita com métrica (a âncora não tinha) |
| RNF-G03-06 | segurança | Sessão da ficha bloqueada após no máximo 2 min de inatividade, com reautenticação para reabrir | caso de teste com sessão ociosa | decisão do grupo (RN-11; tablet em campo pode ser perdido) |
| RNF-G03-07 | desempenho | Pedido de pré-admissão disponível para G04 em até 3 s após a confirmação do regulador, com conexão e carga de 20 pedidos por minuto | análise do fluxo crítico e caso de teste de fronteira | decisão do grupo (RN-12; objetivo do módulo) |
| RNF-G03-08 | usabilidade | Registro de um conjunto de sinais vitais concluído em até 45 s por usuário treinado | teste com protótipo (E7) com ao menos 3 pessoas | decisão do grupo (uso em emergência) |

> Os números de RNF-G03-01, 06, 07 e 08 são alvos propostos pelo grupo e devem ser revistos com o professor.

---

## E3. Casos de uso

Diagrama (fonte em `diagramas/diagrama-casos-de-uso-g03.puml`, exportação em `.png` e `.svg`):

![Diagrama de casos de uso do G03](diagramas/diagrama-casos-de-uso-g03.png)

| ID | Caso de uso | Ator primário | Papel |
| --- | --- | --- | --- |
| UC-G03-01 | [Registrar Teleorientação](casos-de-uso/uc-g03-01-registrar-teleorientacao.md) | MedicoRegulador | principal |
| UC-G03-02 | [Preencher Ficha Pré-Hospitalar](casos-de-uso/uc-g03-02-preencher-ficha-pre-hospitalar.md) | EquipeIntervencao | principal |
| UC-G03-03 | [Solicitar Pré-Admissão](casos-de-uso/uc-g03-03-solicitar-pre-admissao.md) | MedicoRegulador | principal, **fluxo crítico completo** |
| UC-G03-04 | [Registrar Recusa de Atendimento](casos-de-uso/uc-g03-04-registrar-recusa-de-atendimento.md) | EquipeIntervencao | extensão de UC-G03-02 |
| UC-G03-05 | [Validar Prioridade](casos-de-uso/uc-g03-05-validar-prioridade.md) | (sistema) | incluído por UC-G03-03 |
| UC-G03-06 | [Consultar Ficha Pré-Hospitalar](casos-de-uso/uc-g03-06-consultar-ficha-pre-hospitalar.md) | EquipeReceptora | principal |
| UC-G03-07 | [Sincronizar Ficha na Reconexão](casos-de-uso/uc-g03-07-sincronizar-ficha-na-reconexao.md) | EquipeIntervencao | extensão de UC-G03-02 |
| UC-G03-08 | [Controlar e Registrar Acesso ao Prontuário](casos-de-uso/uc-g03-08-controlar-e-registrar-acesso-ao-prontuario.md) | (sistema) | incluído por UC-G03-02, 03 e 06 |

Os oito casos de uso têm fluxo principal, alternativos e de exceção. Todos têm especificação textual, acima do mínimo de 4 casos de uso e 2 especificações.

### Justificativa dos relacionamentos

| Relacionamento | Justificativa |
| --- | --- |
| UC-G03-03 `<<include>>` UC-G03-05 | Sem a prioridade vigente o C3 é inválido; a validação é obrigatória e isola a regra RN-02. |
| UC-G03-03, UC-G03-02, UC-G03-06 `<<include>>` UC-G03-08 | Todo acesso à ficha exige verificação de perfil e evento (RN-11, LGPD art. 37); o include evita repetir a regra em três casos de uso. |
| UC-G03-04 `<<extend>>` UC-G03-02 | A recusa é opcional e condicionada a paciente consciente que recusa; ocorre dentro do preenchimento da ficha. |
| UC-G03-07 `<<extend>>` UC-G03-02 | A sincronização só ocorre se houve período sem conexão. |

---

## Eventos que o módulo publica para G06

- `TELEORIENTACAO_REGISTRADA`
- `PRONTUARIO_ACESSADO`
- `RECUSA_ASSINADA`

## Riscos de modelagem conhecidos

- Transformar a ficha em prontuário hospitalar completo (fora de escopo).
- Recusa sem evidência de assinatura.
- Pré-admissão recalculando prioridade em vez de herdar.
- Bloquear o registro clínico por regra de estoque (P-04).
- Sobrescrever registros em vez de versionar (RF-G03-15).

## Estado da entrega

| Artefato | M1 (Aula 18) | M2 (Aula 24) | M3 (Aula 27) |
| --- | --- | --- | --- |
| E1 Visão e escopo | v1.0 entregue | | |
| E2 Catálogo RF/RNF | v1.0 entregue | | |
| E3 Casos de uso | v1.0 entregue | | |
| E4 Classes + dicionário | | pendente | |
| E5 Sequência + estados | | pendente | |
| E6 ADRs, matriz e testes | | parcial | pendente |
| E7 Protótipos + relatório | | | pendente |

## Referências

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). **Diário Oficial da União**: seção 1, Brasília, DF, 15 ago. 2018.

BRASIL. Lei nº 14.510, de 27 de dezembro de 2022. Altera a Lei nº 8.080, de 19 de setembro de 1990, para autorizar e disciplinar a prática da telessaúde em todo o território nacional, e a Lei nº 13.146, de 6 de julho de 2015; e revoga a Lei nº 13.989, de 15 de abril de 2020. **Diário Oficial da União**: seção 1, Brasília, DF, 28 dez. 2022.

CONSELHO FEDERAL DE MEDICINA (Brasil). Resolução CFM nº 2.314, de 20 de abril de 2022. Define e regulamenta a telemedicina, como forma de serviços médicos mediados por tecnologias de comunicação. **Diário Oficial da União**: seção 1, n. 84, p. 227-228, Brasília, DF, 5 maio 2022.

SILVA, Mateus. **Definição do Projeto: SAPH-Clin (2026.2)**. Petrolina: FACAPE, 2026. Disponível em: https://github.com/mateusamorim96/es1_projeto_saph_clin_facape. Acesso em: 14 nov. 2026.

SILVA, Mateus. **Contexto do Sistema** e **Arquitetura Modular**: SAPH-Clin (2026.2). Petrolina: FACAPE, 2026. Disponível em: https://github.com/mateusamorim96/es1_projeto_saph_clin_facape. Acesso em: 14 nov. 2026.

## Como rodar a validação local

```bash
python3 scripts/check_entrega.py --grupo grupo-03-telemedicina-prontuario --marco M1
```

## Estrutura da pasta

```text
grupo-03-telemedicina-prontuario/
├── README.md                  ← escopo, requisitos, estado
├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT
├── casos-de-uso/              ← UC-G03-NN-*.md
├── diagramas/                 ← fonte (.puml) + export (.png/.svg)
├── prototipos/                ← wireframes (fonte + imagem)
├── adr/                       ← ADR-G03-NN-*.md
└── testes/                    ← CT-G03-NN-*.md
```
