# 🚑 SAPH-Clin — Projeto de Engenharia de Software I (FACAPE, 2026.2)

> Projeto aplicado da disciplina **Engenharia de Software I**
> Curso de Engenharia de Software · Professor: Mateus Silva
> Semestre: **2026.2**

---

## 📋 Contexto

Este repositório centraliza os artefatos de modelagem do **SAPH-Clin** — Sistema
Integrado de Atendimento Pré-Hospitalar e Gestão Hospitalar Crítica — definido em
[`docs/definicao-projeto.md`](docs/definicao-projeto.md).

O problema que o sistema resolve: a informação clínica produzida na rua (viatura)
não chega estruturada ao hospital. O resultado é retrabalho na recepção, atraso na
abertura de leito crítico e baixa rastreabilidade do consumo de fármacos
controlados em trânsito.

O SAPH-Clin cobre três frentes:

- **Regulação e despacho** de ocorrências com classificação de risco (Manchester).
- **Telemedicina e prontuário** pré-hospitalar com pré-admissão no hospital.
- **Recursos críticos** (leitos e estoque de controlados) com **auditoria** transversal.

O sistema **não** substitui o prontuário hospitalar definitivo nem o sistema de
faturamento; ele cobre o **hiato entre o chamado e a entrega do paciente ao leito**.

---

## 🗂️ Estrutura do Repositório

```text
es1_projeto_saph_clin_facape/
│
├── README.md                      ← este arquivo (mantido pelo professor)
├── CONTRIBUTING.md                ← regras de contribuição e fluxo de PR
│
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md   ← checklist obrigatório no PR
│   ├── ISSUE_TEMPLATE/
│   │   └── entrega-grupo.md       ← template de issue de entrega
│   └── workflows/
│       └── validar-entrega.yml    ← CI: escopo, estrutura, nomenclatura
│
├── scripts/
│   ├── check_entrega.py           ← validador local (roda a mesma regra da CI)
│   └── gerar_grupos.py            ← mantenedor: regenera README/matriz dos grupos
│
├── docs/                          ← fonte de verdade do domínio (professor)
│   ├── definicao-projeto.md/.pdf  ← definição oficial do projeto
│   ├── contexto-do-sistema.md     ← problema, escopo, atores, regras de negócio
│   ├── glossario-base.md          ← vocabulário comum do domínio
│   ├── temas-grupos.md            ← os 6 grupos, escopo e fronteiras
│   ├── arquitetura-modular.md     ← contratos de interface entre módulos
│   ├── requisitos-entrega-av2.md  ← entregáveis, marcos, rubrica, penalidades
│   ├── exemplos/                  ← entrega-modelo (nível de detalhe esperado)
│   └── templates/                 ← modelos de artefato (use, não reinvente)
│
└── grupos/
    ├── grupo-01-regulacao-triagem/        ← G1 · Chamado e triagem de risco
    ├── grupo-02-despacho-viaturas/        ← G2 · Despacho e frota (USB/USA)
    ├── grupo-03-telemedicina-prontuario/  ← G3 · Teleorientação e pré-admissão
    ├── grupo-04-leitos-criticos/          ← G4 · Leitos Sala Vermelha/Observação
    ├── grupo-05-estoque-controlados/      ← G5 · Maletas, lotes e controlados
    └── grupo-06-auditoria-compliance/     ← G6 · Trilha de auditoria e indicadores
```

> ⚠️ **Regra de ouro:** cada grupo escreve **exclusivamente** dentro da sua pasta
> `grupos/grupo-XX-*/`. Qualquer alteração fora dela **reprova a CI** e o PR não
> pode ser mesclado.

---

## 👥 Grupos e Responsabilidades

| Grupo | Pasta | Módulo do SAPH-Clin | Responsabilidade central |
| ----- | ----- | ------------------- | ------------------------ |
| G1 | `grupo-01-regulacao-triagem` | M1 · Regulação | Acolhimento, triagem Manchester, ciclo de vida do Chamado |
| G2 | `grupo-02-despacho-viaturas` | M1 · Regulação | Despacho por gravidade/proximidade, estados da Viatura |
| G3 | `grupo-03-telemedicina-prontuario` | M2 · Telemedicina | Teleorientação, ficha pré-hospitalar, pré-admissão |
| G4 | `grupo-04-leitos-criticos` | M3 · Recursos críticos | Reserva de leito, estados do Leito, bloqueios sanitários |
| G5 | `grupo-05-estoque-controlados` | M3 · Recursos críticos | Dispensação, lote/validade, reposição de maleta |
| G6 | `grupo-06-auditoria-compliance` | M4 · Auditoria | Trilha imutável, assinatura digital, indicadores, LGPD |

Detalhes de escopo, entradas e saídas de cada grupo:
[`docs/temas-grupos.md`](docs/temas-grupos.md).

---

## 🔄 Fluxo de Trabalho

```text
1. Fork deste repositório para a conta do grupo
2. Clone o fork e cadastre o upstream do professor
3. Trabalhe APENAS dentro de grupos/grupo-XX-*/
4. Rode o validador local:  python3 scripts/check_entrega.py --grupo grupo-XX
5. Commit no padrão:        [G0X] feat: descricao-curta
6. Push na branch:          grupo-XX/descricao-curta
7. Abra o Pull Request para main deste repositório
8. Preencha o PULL_REQUEST_TEMPLATE por completo
9. CI valida escopo, estrutura e nomenclatura; professor revisa e aprova
```

Regras completas, nomenclatura e definição de pronto:
[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 📦 Entregáveis do Grupo

Cada grupo entrega **o módulo completo**, não um recorte. Os sete artefatos
obrigatórios estão detalhados em
[`docs/requisitos-entrega-av2.md`](docs/requisitos-entrega-av2.md):

1. Visão e escopo do módulo
2. Catálogo de requisitos (RF/RNF) com identificadores
3. Casos de uso (geral + específicos com `<<include>>`/`<<extend>>`) e especificação textual
4. Diagrama de classes de domínio + dicionário de dados
5. Diagramas de sequência e máquina de estados dos ciclos de vida do módulo
6. ADRs, matriz de rastreabilidade e casos de teste
7. Protótipos de baixa fidelidade + relatório técnico

---

## 📅 Marcos de Acompanhamento

| Marco | Aula | O que é verificado |
| ----- | ---- | ------------------ |
| M1 | Aula 18 | Escopo do módulo, RF/RNF, casos de uso v1.0 |
| M2 | Aula 24 | Classes, sequência, estados, ADRs v1.0 |
| M3 | Aula 27 | Rastreabilidade, testes, protótipos, PR final |
| M4 | Aulas 29–30 | Defesa pública do módulo (banca) |

Datas oficiais por turma seguem o cronograma da disciplina publicado pelo
professor. Marco não entregue no PR = módulo tratado como **não entregue**.

---

## ✅ Validação Local (antes de abrir o PR)

```bash
# valida escopo, estrutura mínima e nomenclatura do seu grupo
python3 scripts/check_entrega.py --grupo grupo-02

# opcional: verificar apenas arquivos alterados em relação à main
python3 scripts/check_entrega.py --grupo grupo-02 --base origin/main
```

O script roda sem dependências externas (Python 3.10+). A CI executa a mesma
regra — se passar local, passa no PR.

---

## 📚 Referências do Domínio

- **Portaria MS/GM nº 2.048/2002** — Regulamento Técnico dos Sistemas Estaduais
  de Urgência e Emergência (regulação médica e classificação de risco).
- **Protocolo de Manchester** — triagem por gravidade (Vermelho, Laranja,
  Amarelo, Verde, Azul).
- **Lei nº 13.709/2018 (LGPD)** — dados de saúde são dados sensíveis (art. 5º, II).
- **Lei nº 14.510/2022** e **Resolução CFM nº 2.314/2022** — telessaúde e telemedicina.
- **Portaria SVS/MS nº 344/1998** e **RDC ANVISA nº 22/2014** — substâncias
  sujeitas a controle especial e SNGPC.
- **RDC ANVISA nº 301/2019** — boas práticas de distribuição e transporte de
  medicamentos.

> Confirme sempre a redação vigente da norma antes de citá-la como requisito.
> Citar norma desatualizada sem verificação é erro de engenharia de requisitos.

---

## 🙏 Créditos

Projeto acadêmico da Faculdade de Petrolina (FACAPE). Domínio inspirado em
serviços reais de regulação médica e na literatura de engenharia de software
(Sommerville; Pressman & Maxim; Pfleeger).
