# Glossário Base — SAPH-Clin

Vocabulário comum aos seis grupos. Termo usado com sentido diferente do glossário
é fonte de retrabalho: alinhe antes de modelar.

> Formato: **Termo** — definição operacional (como aparece no sistema) · sinônimos
> aceitos entre parênteses.

## Domínio pré-hospitalar

- **Chamado** (ocorrência, solicitação) — registro único iniciado no acolhimento;
  tem identificador, solicitante, localização e ciclo de vida próprio.
- **Acolhimento** — primeiro contato telefônico; coleta dados mínimos e vincula o
  chamado a um TASI.
- **TASI** — Telefonista Auxiliar de Regulação Médica; abre o chamado, não decide
  conduta clínica.
- **Regulação médica** — decisão do médico regulador sobre prioridade, viatura e
  destino do paciente.
- **Triagem / classificação de risco** — atribuição de prioridade clínica segundo
  protocolo; no SAPH-Clin segue o **Protocolo de Manchester**.
- **Manchester (cores)** — Vermelho (emergência), Laranja (muito urgente),
  Amarelo (urgente), Verde (pouco urgente), Azul (não urgente).
- **Despacho** — alocação de viatura e equipe a um chamado classificado.
- **USB** — Unidade de Suporte Básico; equipe mínima de socorro básico.
- **USA** — Unidade de Suporte Avançado (UTI móvel); exige suporte avançado.
- **ETA** (*Estimated Time of Arrival*) — tempo previsto até o local ou o hospital.
- **Teleorientação** — orientação do médico regulador ao socorrista ou acompanhante
  antes da chegada ao hospital.
- **Telemedicina** — prática médica mediada por tecnologia (respaldo normativo:
  Lei 14.510/2022 e Res. CFM 2.314/2022).
- **Ficha pré-hospitalar** — registro clínico feito em campo: sinais vitais,
  procedimentos e medicações.
- **Pré-admissão** — solicitação antecipada de leito, enviada antes de a viatura
  cruzar os portões do hospital.
- **Sala Vermelha** — área de atendimento a paciente crítico.
- **Observação** — área de monitoramento breve, para casos de menor criticidade.
- **Passagem de plantão digital** — transferência estruturada do caso da equipe
  móvel para a equipe receptora.

## Recursos críticos

- **Leito** — recurso hospitalar com estado explícito (vagos, ocupados, em
  higienização, bloqueados).
- **Reserva de leito** — vínculo temporário entre chamado e leito, com prazo.
- **Reserva dupla** — duas reservas ativas no mesmo leito; condição proibida (RN-05).
- **Bloqueio sanitário** — indisponibilização de leito ou item por risco de contaminação.
- **Maleta de emergência** — conjunto de fármacos e insumos embarcados na viatura.
- **Dispensação** — saída de item do estoque para uso em atendimento.
- **Lote** — identificação de fabricação de um medicamento; base do controle de validade.
- **Item controlado** — fármaco sujeito a controle especial (ex.: opioides, sedativos).
- **SNGPC** — Sistema Nacional de Gerenciamento de Produtos Controlados (ANVISA).
- **Reposição** — recomposição da maleta após consumo, autorizada pelo farmacêutico.
- **Conciliação** — conferência entre consumo registrado e estoque físico.

## Auditoria e conformidade

- **Audit trail** (trilha de auditoria) — registro imutável de ações sensíveis:
  quem, o quê, quando, sobre qual entidade, com qual resultado.
- **Evento sensível** — ação que exige trilha: regulação, despacho, dispensação,
  reserva de leito, acesso a prontuário, reclassificação de risco.
- **Imutabilidade** — propriedade de um registro que não pode ser alterado nem
  apagado, apenas complementado.
- **Assinatura digital** — evidência de autoria em conduta excepcional ou recusa
  de atendimento.
- **LGPD** — Lei Geral de Proteção de Dados; dado de saúde é dado **sensível**.
- **Minimização** — princípio de coletar apenas o dado necessário para a finalidade.
- **Indicador** — medida operacional (tempo de resposta, taxa de ocupação,
  consumo por 1.000 atendimentos).
- **Tempo de resposta** — intervalo entre abertura do chamado e início do
  atendimento efetivo (RN-12 define o recorte aceito).

## Engenharia de software (uso neste projeto)

- **RF** — requisito funcional, comportamento observável do sistema.
- **RNF** — requisito não funcional, atributo de qualidade mensurável.
- **UC** — caso de uso; interação entre ator e sistema orientada a objetivo.
- **ADR** — *Architecture Decision Record*; registro de decisão com contexto e consequências.
- **Matriz de rastreabilidade** — tabela que liga requisito → caso de uso → classe
  → sequência → caso de teste.
- **CT** — caso de teste; procedimento com entrada, passos e resultado esperado.
- **Wireframe** — protótipo de baixa fidelidade que fixa estrutura, não estética.
- **Fronteira de módulo** — limite de responsabilidade entre dois grupos; definido
  por contrato de entrada e saída.
