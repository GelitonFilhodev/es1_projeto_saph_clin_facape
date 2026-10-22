#!/usr/bin/env python3
"""Gera README.md e matriz-rastreabilidade.md iniciais dos 6 grupos do SAPH-Clin."""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
GRUPOS = BASE / "grupos"

DADOS = {
    "grupo-01-regulacao-triagem": {
        "codigo": "G01",
        "nome": "Regulação e Triagem",
        "modulo": "M1 — Regulação e Despacho de Urgência",
        "subprocesso": "Acolhimento, classificação de risco e ciclo de vida do Chamado",
        "atores": "TASI, MedicoRegulador",
        "entidades": "`Chamado`, `Triagem`, `Solicitante`, `ClassificacaoRisco`",
        "fronteira_in": "Ligação do solicitante (fora do sistema)",
        "fronteira_out": "Contrato C1 `chamado_classificado` para G2",
        "fora": [
            "escolher viatura ou equipe (G2)",
            "registrar dados clínicos de campo (G3)",
            "reservar leito (G4)",
        ],
        "ucs": [
            "UC-G01-01 Registrar Chamado",
            "UC-G01-02 Classificar Risco (Manchester)",
            "UC-G01-03 Reclassificar Chamado (`<<extend>>` de Classificar Risco)",
            "UC-G01-04 Cancelar Chamado",
        ],
        "rfs": [
            ("RF-G01-01", "Registrar chamado com solicitante, localização e queixa principal", "UC-G01-01"),
            ("RF-G01-02", "Classificar risco nas cinco cores do Protocolo de Manchester", "UC-G01-02"),
            ("RF-G01-03", "Registrar autor e justificativa em toda reclassificação", "UC-G01-03"),
            ("RF-G01-04", "Detectar chamado duplicado da mesma ocorrência", "UC-G01-01"),
            ("RF-G01-05", "Cancelar chamado com motivo obrigatório", "UC-G01-04"),
            ("RF-G01-06", "Manter histórico completo de classificações do chamado", "UC-G01-02"),
            ("RF-G01-07", "Alertar regulador quando triagem exceder 4 minutos (RN-01)", "UC-G01-02"),
            ("RF-G01-08", "Publicar evento `CHAMADO_CLASSIFICADO` para G6", "UC-G01-02"),
        ],
        "rnfs": [
            ("RNF-G01-01", "Acolhimento concluído em ≤ 90 s no fluxo principal", "desempenho"),
            ("RNF-G01-02", "Triagem disponível mesmo com falha de rede local (registro offline)", "disponibilidade"),
            ("RNF-G01-03", "Dado do solicitante protegido por perfil de acesso (LGPD)", "segurança"),
            ("RNF-G01-04", "Reclassificação visível no histórico em ≤ 3 s", "desempenho"),
            ("RNF-G01-05", "Vocabulário de queixa alinhado ao glossário do domínio", "usabilidade"),
        ],
        "riscos": [
            "modelar triagem como atributo de cor (perde histórico de reclassificação)",
            "aceitar classificação sem registro do médico regulador",
            "esquecer que o TASI não decide conduta clínica",
        ],
        "eventos": ["`CHAMADO_CLASSIFICADO`", "`PRIORIDADE_RECLASSIFICADA`", "`CHAMADO_CANCELADO`"],
    },
    "grupo-02-despacho-viaturas": {
        "codigo": "G02",
        "nome": "Despacho e Frota de Viaturas",
        "modulo": "M1 — Regulação e Despacho de Urgência",
        "subprocesso": "Despacho por gravidade/proximidade e ciclo de vida da Viatura",
        "atores": "MedicoRegulador, EquipeIntervencao",
        "entidades": "`Viatura` (abstrata), `ViaturaUSB`, `ViaturaUSA`, `Equipe`, `Despacho`, `Base`",
        "fronteira_in": "Contrato C1 `chamado_classificado` (G1)",
        "fronteira_out": "Contrato C2 `despacho_ativo` para G3",
        "fora": [
            "classificar risco do chamado (G1)",
            "preencher ficha clínica (G3)",
            "controlar estoque da maleta (G5)",
        ],
        "ucs": [
            "UC-G02-01 Despachar Viatura (`<<include>>` Verificar Disponibilidade de Equipe)",
            "UC-G02-02 Acionar Suporte Avançado (`<<extend>>` de Despachar Viatura)",
            "UC-G02-03 Encerrar Atendimento",
            "UC-G02-04 Sinalizar Indisponibilidade da Viatura",
        ],
        "rfs": [
            ("RF-G02-01", "Selecionar viatura compatível com a prioridade clínica", "UC-G02-01"),
            ("RF-G02-02", "Impedir dupla alocação da mesma viatura (RN-04)", "UC-G02-01"),
            ("RF-G02-03", "Exigir equipe de suporte avançado completo para despachar USA (RN-03)", "UC-G02-01"),
            ("RF-G02-04", "Registrar justificativa do despacho escolhido", "UC-G02-01"),
            ("RF-G02-05", "Acionar suporte avançado durante atendimento em curso", "UC-G02-02"),
            ("RF-G02-06", "Rastrear estados da viatura em tempo real", "UC-G02-04"),
            ("RF-G02-07", "Devolver chamado à fila quando não houver viatura compatível", "UC-G02-01"),
            ("RF-G02-08", "Publicar evento `VIATURA_DESPACHADA` para G6", "UC-G02-01"),
        ],
        "rnfs": [
            ("RNF-G02-01", "Despacho concluído em ≤ 120 s após classificação", "desempenho"),
            ("RNF-G02-02", "Estimativa de chegada atualizada a cada 2 min", "desempenho"),
            ("RNF-G02-03", "Estado da viatura consistente entre despachos concorrentes", "consistência"),
            ("RNF-G02-04", "Painel legível em tablet de campo sob luz solar", "usabilidade"),
            ("RNF-G02-05", "Histórico de despacho retido por 5 anos para auditoria", "conformidade"),
        ],
        "riscos": [
            "modelar viatura sem herança e duplicar atributos de USA",
            "ignorar indisponibilidade (viatura em higienização ainda aparece como livre)",
            "não modelar o que acontece quando não há viatura",
        ],
        "eventos": ["`VIATURA_DESPACHADA`", "`SUPORTE_AVANCADO_ACIONADO`", "`ATENDIMENTO_ENCERRADO`"],
    },
    "grupo-03-telemedicina-prontuario": {
        "codigo": "G03",
        "nome": "Telemedicina e Prontuário Pré-Hospitalar",
        "modulo": "M2 — Telemedicina Regulada e Prontuário Integrado",
        "subprocesso": "Teleorientação, ficha pré-hospitalar digital e pré-admissão",
        "atores": "MedicoRegulador, EquipeIntervencao, EquipeReceptora",
        "entidades": "`Teleorientacao`, `Prontuario`, `RegistroSinaisVitais`, `Procedimento`, `ConsumoFarmaco`, `PreAdmissao`",
        "fronteira_in": "Contrato C2 `despacho_ativo` (G2)",
        "fronteira_out": "Contrato C3 `pedido_pre_admissao` (G4) e C4 `consumo_farmaco` (G5)",
        "fora": [
            "decidir despacho (G2)",
            "aceitar ou negar reserva de leito (G4)",
            "dar baixa em estoque (G5)",
        ],
        "ucs": [
            "UC-G03-01 Registrar Teleorientação",
            "UC-G03-02 Preencher Ficha Pré-Hospitalar",
            "UC-G03-03 Solicitar Pré-Admissão (`<<include>>` Validar Prioridade)",
            "UC-G03-04 Registrar Recusa de Atendimento (`<<extend>>`, exige assinatura)",
        ],
        "rfs": [
            ("RF-G03-01", "Registrar teleorientação com autor, horário e destinatário", "UC-G03-01"),
            ("RF-G03-02", "Registrar sinais vitais em campo com horário de coleta", "UC-G03-02"),
            ("RF-G03-03", "Registrar procedimentos e fármacos administrados", "UC-G03-02"),
            ("RF-G03-04", "Emitir pedido de pré-admissão com prioridade herdada da triagem", "UC-G03-03"),
            ("RF-G03-05", "Registrar recusa de atendimento com assinatura e testemunha (RN-10)", "UC-G03-04"),
            ("RF-G03-06", "Manter ficha disponível sem conexão e sincronizar depois", "UC-G03-02"),
            ("RF-G03-07", "Restringir acesso à ficha por perfil e registrar cada acesso", "UC-G03-02"),
            ("RF-G03-08", "Publicar eventos `TELEORIENTACAO_REGISTRADA` e `PRONTUARIO_ACESSADO`", "UC-G03-01"),
        ],
        "rnfs": [
            ("RNF-G03-01", "Ficha sincronizada em ≤ 5 s após reconexão", "desempenho"),
            ("RNF-G03-02", "Nenhum dado clínico perdido em queda de conexão durante o registro", "confiabilidade"),
            ("RNF-G03-03", "Dado clínico criptografado em repouso (LGPD)", "segurança"),
            ("RNF-G03-04", "Ficha utilizável em tablet com uma mão, alvos de toque ≥ 44 px", "usabilidade"),
            ("RNF-G03-05", "Telessaúde aderente à Res. CFM 2.314/2022", "conformidade"),
        ],
        "riscos": [
            "transformar a ficha em prontuário hospitalar completo (fora de escopo)",
            "recusa sem evidência de assinatura",
            "pré-admissão recalculando prioridade em vez de herdar",
        ],
        "eventos": ["`TELEORIENTACAO_REGISTRADA`", "`PRONTUARIO_ACESSADO`", "`RECUSA_ASSINADA`"],
    },
    "grupo-04-leitos-criticos": {
        "codigo": "G04",
        "nome": "Leitos Críticos e Reserva",
        "modulo": "M3 — Gestão de Recursos Críticos e Estoque Finitivo",
        "subprocesso": "Oferta, reserva, bloqueio e liberação de leitos críticos",
        "atores": "MedicoRegulador, EquipeReceptora",
        "entidades": "`Leito`, `Setor` (Sala Vermelha, Observação), `ReservaLeito`, `Higienizacao`, `AlertaTransferencia`",
        "fronteira_in": "Contrato C3 `pedido_pre_admissao` (G3)",
        "fronteira_out": "Reserva ativa + alerta à equipe receptora",
        "fora": [
            "decidir prioridade clínica (G1)",
            "preencher ficha pré-hospitalar (G3)",
            "controlar insumos da maleta (G5)",
        ],
        "ucs": [
            "UC-G04-01 Consultar Disponibilidade de Leitos",
            "UC-G04-02 Reservar Leito (`<<include>>` Verificar Conflito de Reserva)",
            "UC-G04-03 Bloquear Leito por Motivo Sanitário",
            "UC-G04-04 Liberar Leito após Alta/Higienização",
            "UC-G04-05 Cancelar Reserva Expirada",
        ],
        "rfs": [
            ("RF-G04-01", "Manter estado explícito de cada leito (vago, reservado, ocupado, em higienização, bloqueado)", "UC-G04-01"),
            ("RF-G04-02", "Reservar leito vinculado ao chamado e ao prontuário", "UC-G04-02"),
            ("RF-G04-03", "Impedir duas reservas ativas no mesmo leito (RN-05)", "UC-G04-02"),
            ("RF-G04-04", "Expirar reserva não confirmada após o prazo do ETA", "UC-G04-05"),
            ("RF-G04-05", "Bloquear leito com motivo obrigatório e autor", "UC-G04-03"),
            ("RF-G04-06", "Não ofertar leito em higienização ou bloqueado (RN-06)", "UC-G04-01"),
            ("RF-G04-07", "Alertar equipe receptora no aceite da reserva", "UC-G04-02"),
            ("RF-G04-08", "Publicar eventos `LEITO_RESERVADO` e `LEITO_NEGADO`", "UC-G04-02"),
        ],
        "rnfs": [
            ("RNF-G04-01", "Reserva confirmada em ≤ 2 s no pico de 20 req/min", "desempenho"),
            ("RNF-G04-02", "Zero reserva dupla em qualquer cenário de concorrência", "consistência"),
            ("RNF-G04-03", "Painel de leitos com defasagem máxima de 30 s", "desempenho"),
            ("RNF-G04-04", "Bloqueio sanitário visível em todos os pontos de consulta", "usabilidade"),
            ("RNF-G04-05", "Histórico de ocupação disponível para indicadores (G6)", "conformidade"),
        ],
        "riscos": [
            "tratar leito como quantidade (\"4 vagos\") em vez de entidade com estado",
            "ignorar expiração de reserva (leito fica preso)",
            "permitir bloqueio sem autor e motivo",
        ],
        "eventos": ["`LEITO_RESERVADO`", "`LEITO_NEGADO`", "`LEITO_BLOQUEADO`"],
    },
    "grupo-05-estoque-controlados": {
        "codigo": "G05",
        "nome": "Estoque de Fármacos Controlados",
        "modulo": "M3 — Gestão de Recursos Críticos e Estoque Finitivo",
        "subprocesso": "Maletas de emergência, dispensação por lote, validade e reposição",
        "atores": "EquipeIntervencao, FarmaceuticoHospitalar",
        "entidades": "`ItemEstoque`, `Lote`, `Maleta`, `MovimentacaoEstoque`, `AutorizacaoDispensacao`",
        "fronteira_in": "Contrato C4 `consumo_farmaco` (G3)",
        "fronteira_out": "Baixa por lote, solicitação de reposição e trava de item",
        "fora": [
            "prescrever ou indicar conduta clínica (G3)",
            "controlar leitos (G4)",
            "compilar indicadores gerais (G6)",
        ],
        "ucs": [
            "UC-G05-01 Registrar Consumo em Campo",
            "UC-G05-02 Dispensar Controlado (`<<include>>` Validar Lote e Validade)",
            "UC-G05-03 Solicitar Reposição de Maleta",
            "UC-G05-04 Travar Item Suspeito ou Vencido",
            "UC-G05-05 Conciliar Estoque da Maleta",
        ],
        "rfs": [
            ("RF-G05-01", "Controlar estoque por item, lote e validade", "UC-G05-01"),
            ("RF-G05-02", "Registrar dispensação com autor e vínculo ao prontuário", "UC-G05-02"),
            ("RF-G05-03", "Bloquear dispensação de lote vencido ou travado (RN-08)", "UC-G05-02"),
            ("RF-G05-04", "Exigir autorização farmacêutica para controlado (RN-07)", "UC-G05-02"),
            ("RF-G05-05", "Gerar solicitação de reposição após consumo", "UC-G05-03"),
            ("RF-G05-06", "Apontar divergência entre consumo registrado e estoque", "UC-G05-05"),
            ("RF-G05-07", "Travessar item sob suspeita sanitária com motivo", "UC-G05-04"),
            ("RF-G05-08", "Publicar eventos `CONTROLADO_DISPENSADO` e `ITEM_TRAVADO`", "UC-G05-02"),
        ],
        "rnfs": [
            ("RNF-G05-01", "Baixa de controlado registrada em ≤ 3 s em campo", "desempenho"),
            ("RNF-G05-02", "Rastreabilidade lote → paciente → profissional preservada", "conformidade"),
            ("RNF-G05-03", "Nenhuma dispensação sem autorização registrada", "segurança"),
            ("RNF-G05-04", "Alerta de vencimento com 30 dias de antecedência", "usabilidade"),
            ("RNF-G05-05", "Dados aderentes à Portaria SVS/MS 344/1998 e RDC 22/2014", "conformidade"),
        ],
        "riscos": [
            "modelar estoque apenas como quantidade (perde lote e validade)",
            "dispensação sem autorização registrada",
            "não modelar o que acontece com sobra de controlado",
        ],
        "eventos": ["`CONTROLADO_DISPENSADO`", "`ITEM_TRAVADO`", "`ESTOQUE_CONCILIADO`"],
    },
    "grupo-06-auditoria-compliance": {
        "codigo": "G06",
        "nome": "Auditoria, Compliance e Indicadores",
        "modulo": "M4 — Auditoria, Rastreabilidade e Conformidade",
        "subprocesso": "Modelo de evento imutável, assinatura, indicadores e acesso a dado sensível",
        "atores": "Auditor, Administrador, MedicoRegulador",
        "entidades": "`EventoAuditoria`, `AssinaturaDigital`, `Indicador`, `PerfilAcesso`, `AlertaCompliance`",
        "fronteira_in": "Contrato C5 `evento_sensivel` (G1 a G5)",
        "fronteira_out": "Trilha imutável, relatórios e alertas de conformidade",
        "fora": [
            "executar a regulação, o despacho ou a reserva (módulos de origem)",
            "armazenar conteúdo clínico completo (só referência por identificador)",
            "definir stack tecnológica de armazenamento",
        ],
        "ucs": [
            "UC-G06-01 Registrar Evento Sensível",
            "UC-G06-02 Consultar Trilha de Auditoria",
            "UC-G06-03 Assinar Conduta Excepcional",
            "UC-G06-04 Calcular Indicadores Operacionais",
            "UC-G06-05 Auditar Acesso a Prontuário",
        ],
        "rfs": [
            ("RF-G06-01", "Registrar evento imutável com ator, entidade, horário e resultado", "UC-G06-01"),
            ("RF-G06-02", "Rejeitar qualquer alteração ou exclusão de evento registrado", "UC-G06-01"),
            ("RF-G06-03", "Consultar trilha por chamado, ator e período", "UC-G06-02"),
            ("RF-G06-04", "Assinar digitalmente condutas excepcionais e recusas", "UC-G06-03"),
            ("RF-G06-05", "Calcular tempo de resposta e tempo porta-leito (RN-12)", "UC-G06-04"),
            ("RF-G06-06", "Registrar todo acesso a prontuário como evento sensível (LGPD)", "UC-G06-05"),
            ("RF-G06-07", "Emitir alerta de divergência de estoque e de reserva negada", "UC-G06-04"),
            ("RF-G06-08", "Garantir idempotência por `evento_id` no reenvio", "UC-G06-01"),
        ],
        "rnfs": [
            ("RNF-G06-01", "Consulta de trilha de 30 dias em ≤ 5 s", "desempenho"),
            ("RNF-G06-02", "Evento gravado não pode ser alterado por nenhum perfil", "integridade"),
            ("RNF-G06-03", "Retenção mínima de 5 anos para eventos sensíveis", "conformidade"),
            ("RNF-G06-04", "Indicadores atualizados em janela de 15 min", "desempenho"),
            ("RNF-G06-05", "Acesso a dado sensível auditável e minimizado (LGPD art. 6º)", "conformidade"),
        ],
        "riscos": [
            "modelar auditoria como log de texto sem estrutura",
            "deixar de definir o que não pode ser registrado (minimização)",
            "compilar indicador que não fecha com os eventos de origem",
        ],
        "eventos": ["`TRILHA_CONSULTADA`", "`ASSINATURA_REGISTRADA`", "`ALERTA_COMPLIANCE`"],
    },
}


def readme(slug, d):
    linhas = [
        f"# {d['codigo']} — {d['nome']}",
        "",
        f"> Grupo responsável pelo subprocesso **{d['subprocesso']}** do SAPH-Clin.",
        f"> Módulo: {d['modulo']}",
        "",
        "## Integrantes",
        "",
        "| Nome | Matrícula | Papel no grupo |",
        "| --- | --- | --- |",
        "| *preencher* | | requisitos |",
        "| *preencher* | | modelagem estrutural |",
        "| *preencher* | | modelagem comportamental |",
        "| *preencher* | | testes e rastreabilidade |",
        "",
        "## Escopo do módulo (E1)",
        "",
        f"- **Subprocesso:** {d['subprocesso']}.",
        f"- **Atores envolvidos:** {d['atores']}.",
        f"- **Entidades de domínio (donas do módulo):** {d['entidades']}.",
        f"- **Entrada:** {d['fronteira_in']}.",
        f"- **Saída:** {d['fronteira_out']}.",
        "",
        "### Fora do escopo do grupo",
        "",
    ]
    linhas += [f"- {x}." for x in d["fora"]]
    linhas += [
        "",
        "> Se algo do escopo acima for necessário, consuma o **contrato** descrito em",
        "> `docs/arquitetura-modular.md` — não modele a entidade do vizinho.",
        "",
        "## Casos de uso esperados (E3)",
        "",
    ]
    linhas += [f"- {uc}" for uc in d["ucs"]]
    linhas += [
        "",
        "Use `docs/templates/caso-de-uso.md`. Mínimo: 4 casos de uso, sendo 2",
        "especificados textualmente e pelo menos um `<<include>>` e um `<<extend>>`",
        "justificados.",
        "",
        "## Requisitos âncora (ponto de partida, não de chegada)",
        "",
        "| ID | Requisito funcional | Caso de uso |",
        "| --- | --- | --- |",
    ]
    linhas += [f"| {rid} | {desc} | {uc} |" for rid, desc, uc in d["rfs"]]
    linhas += [
        "",
        "| ID | Requisito não funcional (com métrica) | Categoria |",
        "| --- | --- | --- |",
    ]
    linhas += [f"| {rid} | {desc} | {cat} |" for rid, desc, cat in d["rnfs"]]
    linhas += [
        "",
        "> Estes requisitos são **sementes** extraídas do contexto. O grupo deve",
        "> refiná-los, dividir os compostos e acrescentar o que a análise revelar.",
        "> Requisito copiado sem análise perde nota em profundidade.",
        "",
        "## Eventos que o módulo publica para G06",
        "",
    ]
    linhas += [f"- {ev}" for ev in d["eventos"]]
    linhas += [
        "",
        "## Riscos de modelagem conhecidos",
        "",
    ]
    linhas += [f"- {r}." for r in d["riscos"]]
    linhas += [
        "",
        "## Estado da entrega",
        "",
        "| Artefato | M1 (Aula 18) | M2 (Aula 24) | M3 (Aula 27) |",
        "| --- | --- | --- | --- |",
        "| E1 Visão e escopo | pendente | — | — |",
        "| E2 Catálogo RF/RNF | pendente | — | — |",
        "| E3 Casos de uso | pendente | — | — |",
        "| E4 Classes + dicionário | — | pendente | — |",
        "| E5 Sequência + estados | — | pendente | — |",
        "| E6 ADRs, matriz e testes | — | parcial | pendente |",
        "| E7 Protótipos + relatório | — | — | pendente |",
        "",
        "Atualize esta tabela a cada PR: é o primeiro lugar onde o professor olha.",
        "",
        "## Como rodar a validação local",
        "",
        "```bash",
        f"python3 scripts/check_entrega.py --grupo {slug}",
        "```",
        "",
        "## Estrutura da pasta",
        "",
        "```text",
        f"{slug}/",
        "├── README.md                  ← este arquivo (escopo, requisitos, estado)",
        "├── matriz-rastreabilidade.md  ← RF → UC → Classe → Sequência → CT",
        "├── casos-de-uso/              ← UC-G0X-NN-*.md",
        "├── diagramas/                 ← fonte (.puml/.drawio/.bpmn) + export (.png/.svg)",
        "├── prototipos/                ← wireframes (fonte + imagem)",
        "├── adr/                       ← ADR-G0X-NN-*.md",
        "└── testes/                    ← CT-G0X-NN-*.md",
        "```",
    ]
    return "\n".join(linhas) + "\n"


def matriz(d):
    linhas = [
        f"# Matriz de Rastreabilidade — {d['codigo']}",
        "",
        "> Preencha conforme o modelo em `docs/templates/matriz-rastreabilidade.md`.",
        "> Célula vazia é pendência: use `pendente` explicitamente.",
        "",
        "## Requisitos funcionais",
        "",
        "| RF | Descrição curta | Caso de uso | Classe(s) | Sequência | Caso de teste | Status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for rid, desc, uc in d["rfs"]:
        linhas.append(f"| {rid} | {desc} | {uc} | | | | pendente |")
    linhas += [
        "",
        "## Requisitos não funcionais",
        "",
        "| RNF | Métrica e alvo | Como é verificado | Status |",
        "| --- | --- | --- | --- |",
    ]
    for rid, desc, _cat in d["rnfs"]:
        linhas.append(f"| {rid} | {desc} | | pendente |")
    linhas += [
        "",
        "## Contratos consumidos",
        "",
        "| Contrato | Origem | Campo crítico |",
        "| --- | --- | --- |",
        f"| — | {d['fronteira_in']} | — |",
        "",
        "## Contratos fornecidos",
        "",
        "| Contrato | Destino | Campo crítico |",
        "| --- | --- | --- |",
        f"| — | {d['fronteira_out']} | — |",
        "",
        "## Pendências",
        "",
        "| Item | Impacto | Prazo interno |",
        "| --- | --- | --- |",
        "| | | |",
    ]
    return "\n".join(linhas) + "\n"


def main():
    for slug, d in DADOS.items():
        pasta = GRUPOS / slug
        (pasta / "README.md").write_text(readme(slug, d), encoding="utf-8")
        (pasta / "matriz-rastreabilidade.md").write_text(matriz(d), encoding="utf-8")
        for sub in ("casos-de-uso", "diagramas", "prototipos", "adr", "testes"):
            (pasta / sub).mkdir(exist_ok=True)
            (pasta / sub / ".gitkeep").write_text("", encoding="utf-8")
        print("ok", slug)


if __name__ == "__main__":
    main()
