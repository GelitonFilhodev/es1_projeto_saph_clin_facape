# 🤝 Guia de Contribuição — Projeto SAPH-Clin

Este guia define **como** o trabalho entra no repositório. O que entregar está em
[`docs/requisitos-entrega-av2.md`](docs/requisitos-entrega-av2.md); como entregar
está aqui.

---

## 1. Regras Fundamentais

### ❶ Cada grupo toca APENAS a sua pasta

```text
grupos/grupo-XX-nome-do-grupo/
```

Alterações fora dessa pasta reprovam a CI (`validar-entrega`). Não há exceção:
nem para "corrigir um errinho" no README do professor, nem para corrigir o
arquivo de outro grupo. Precisa mudar `docs/`? Abra uma **issue**; o professor
altera.

### ❷ Padrão de commits

Use o prefixo do grupo em **todas** as mensagens:

```text
[G02] feat: adiciona diagrama de classes do despacho
[G02] fix: corrige multiplicidade Viatura-Chamado
[G02] docs: especifica fluxo alternativo de indisponibilidade
[G02] test: adiciona CT-03 limite de reserva dupla de leito
[G02] chore: renomeia arquivos para kebab-case
```

Tipos permitidos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

Commits genéricos (`update`, `ajustes`, `final`) são recusados na revisão: eles
apagam a rastreabilidade entre decisão e artefato.

### ❸ Nomenclatura de arquivos

- **kebab-case**, minúsculas, sem acentos e sem espaços:
  `diagrama-classes-despacho.puml` — **não** `Diagrama Classes Despacho.PNG`.
- Sempre entregue **fonte + exportação**:
  `.puml`/`.drawio`/`.bpmn` **e** `.png` ou `.svg`.
- Identificadores de artefato seguem o padrão do módulo:
  `RF-G02-01`, `RNF-G02-03`, `UC-G02-02`, `CT-G02-04`, `ADR-G02-01`.

### ❹ Idioma e acentuação

Documentação em **português do Brasil**, com acentuação correta. Nomes de
arquivo, branches e mensagens de commit em ASCII (sem acento) — evita falha em
CI e em ferramentas de versionamento.

---

## 2. Fluxo Passo a Passo

### 1. Fork e clone

```bash
# no GitHub: Fork no repositório do professor
git clone https://github.com/SEU_USUARIO/es1_projeto_saph_clin_facape.git
cd es1_projeto_saph_clin_facape
git remote add upstream https://github.com/mateusamorim96/es1_projeto_saph_clin_facape.git
git fetch upstream
```

### 2. Crie a branch de trabalho

```bash
git checkout -b grupo-02/diagrama-classes
```

Padrão: `grupo-XX/descricao-curta`.

### 3. Trabalhe na sua pasta e valide localmente

```bash
python3 scripts/check_entrega.py --grupo grupo-02
```

O validador confere: escopo (nada fora da pasta), estrutura mínima, nomenclatura
e pares fonte/exportação de diagramas.

### 4. Commit e push

```bash
git add grupos/grupo-02-despacho-viaturas
git commit -m "[G02] feat: adiciona diagrama de classes do despacho"
git push origin grupo-02/diagrama-classes
```

### 5. Abra o Pull Request

- **Base:** repositório do professor, branch `main`
- **Head:** seu fork, branch `grupo-XX/descricao-curta`
- **Título:** `[G02] Entrega M1 — Despacho e Frota`
- Preencha o `PULL_REQUEST_TEMPLATE` **completo** (inclusive decisões e limitações)

### 6. Aguarde a CI e a revisão

A CI roda automaticamente. Erros comuns e correção:

| Erro da CI | Causa | Correção |
| ---------- | ----- | -------- |
| `arquivo fora do escopo` | arquivo editado em `docs/` ou em outro grupo | remova do PR (`git checkout upstream/main -- <arquivo>`) |
| `estrutura minima ausente` | falta `README.md` ou `matriz-rastreabilidade.md` | crie a partir de `docs/templates/` |
| `nome nao conforme` | maiúsculas, espaço ou acento no arquivo | renomeie para kebab-case |
| `diagrama sem exportacao` | `.puml` sem `.png`/`.svg` | exporte e versione a imagem |

---

## 3. Resolução de Conflitos

Como cada grupo trabalha em pasta isolada, conflitos só aparecem se o professor
alterar `docs/` (o que não deve acontecer no meio de um marco). Se ocorrer:

```bash
git fetch upstream
git rebase upstream/main
# resolva os conflitos, mantendo a versao do upstream em docs/
git add .
git rebase --continue
git push --force-with-lease origin grupo-02/diagrama-classes
```

`--force-with-lease` é obrigatório: `--force` puro pode apagar commits de colegas.

---

## 4. Definição de Pronto (DoD)

Um artefato só conta como entregue quando **todos** os itens são verdadeiros:

- [ ] Está na pasta do grupo, com nome kebab-case.
- [ ] Segue o template correspondente em `docs/templates/`.
- [ ] Tem identificador (`RF-G0X-NN`, `UC-G0X-NN`, `CT-G0X-NN`…).
- [ ] Cita a fonte do requisito (definição do projeto, contexto, norma ou decisão do grupo).
- [ ] Diagramas têm fonte editável **e** exportação.
- [ ] Aparece na matriz de rastreabilidade (requisito → caso de uso → classe → sequência → teste).
- [ ] O PR passa na CI.

---

## 5. Checklist antes do PR

- [ ] `python3 scripts/check_entrega.py --grupo grupo-XX` retorna sucesso
- [ ] Nenhum arquivo modificado fora de `grupos/grupo-XX-*/`
- [ ] README do grupo atualizado com estado atual dos artefatos
- [ ] Fontes editáveis e exportações presentes
- [ ] Commits no padrão `[G0X] tipo: descrição`
- [ ] Template de PR preenchido (decisões ≥ 150 palavras, limitações explícitas)
- [ ] Todos os integrantes têm commits no PR

---

## 6. Uso de Ferramentas de IA

Permitido e esperado no mercado — com duas condições:

1. **Declare** no PR quais artefatos usaram apoio de IA e para quê (ex.: "rascunho
   de casos de uso revisado pelo grupo").
2. **O grupo responde pelo conteúdo.** Modelo que inventa requisito, regra de
   negócio ou artigo de lei é erro do grupo, não da ferramenta. Toda afirmação
   normativa precisa de fonte verificável.

---

## 7. Conduta

- Revise o PR do colega antes do professor, quando solicitado.
- Não reescreva o trabalho de outro grupo para "melhorar": abra issue.
- Discordância técnica se resolve com ADR, não com commit revertido.
