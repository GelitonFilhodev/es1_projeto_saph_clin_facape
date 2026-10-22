#!/usr/bin/env python3
"""Validador local de entrega dos grupos do projeto SAPH-Clin.

Roda sem dependencias externas (Python 3.10+) e aplica a MESMA regra da CI
(`.github/workflows/validar-entrega.yml`).

Uso:
    python3 scripts/check_entrega.py --grupo grupo-02
    python3 scripts/check_entrega.py --grupo grupo-02 --base origin/main
    python3 scripts/check_entrega.py --grupo grupo-02 --strict   # warnings falham

Saida: ERRO (bloqueia o PR), AVISO (registrado, nao bloqueia), OK.
Codigo de saida: 0 = aprovado, 1 = reprovado, 2 = erro de uso.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

GRUPOS_DIR = "grupos"
ARQUIVOS_OBRIGATORIOS = ("README.md", "matriz-rastreabilidade.md")
PASTAS_OBRIGATORIAS = ("casos-de-uso", "diagramas", "prototipos", "adr", "testes")
FONTES_DIAGRAMA = (".puml", ".drawio", ".bpmn", ".excalidraw")
EXPORTS_DIAGRAMA = (".png", ".svg", ".pdf")
PROIBIDOS = ("__pycache__", ".DS_Store", "node_modules", ".pyc", "~$")
PREFIXO_ARTEFATO = {
    "casos-de-uso": ("uc-",),
    "adr": ("adr-",),
    "testes": ("ct-",),
}
# Nomes convencionais que fogem ao kebab-case e sao aceitos.
NOMES_CONSAGRADOS = {"README.md", "LICENSE", "CHANGELOG.md"}
# Minimo de arquivos reais (fora .gitkeep) esperados em cada pasta, por marco.
MINIMOS_MARCO = {
    "M1": {"casos-de-uso": 1, "diagramas": 0, "prototipos": 0, "adr": 0, "testes": 0},
    "M2": {"casos-de-uso": 1, "diagramas": 2, "prototipos": 0, "adr": 2, "testes": 1},
    "M3": {"casos-de-uso": 2, "diagramas": 3, "prototipos": 2, "adr": 2, "testes": 4},
}

PLACEHOLDERS = ("preencher", "tbd", "todo", "lorem")

RE_GRUPO = re.compile(r"^grupo-\d{2}-[a-z0-9-]+$")
RE_NOME_OK = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
RE_ID = re.compile(r"^(RF|RNF|UC|CT|ADR|DS)-G\d{2}-\d{2}$")


class Relatorio:
    def __init__(self) -> None:
        self.erros: list[str] = []
        self.avisos: list[str] = []

    def erro(self, msg: str) -> None:
        self.erros.append(msg)

    def aviso(self, msg: str) -> None:
        self.avisos.append(msg)

    def imprimir(self, grupo: str, pasta: Path, marco: str | None = None) -> int:
        print(f"grupo: {grupo}")
        print(f"pasta: {pasta}")
        print(f"marco: {marco or 'nao informado'}")
        if self.avisos:
            print(f"\nAVISO ({len(self.avisos)}):")
            for a in self.avisos:
                print(f"  - {a}")
        if self.erros:
            print(f"\nERRO ({len(self.erros)}):")
            for e in self.erros:
                print(f"  - {e}")
            print("\nRESULTADO: REPROVADO")
            return 1
        print("\nRESULTADO: APROVADO")
        return 0


def normalizar_grupo(valor: str) -> str:
    valor = valor.strip().lower()
    m = re.fullmatch(r"g?0?(\d{1,2})", valor)
    if m:
        return f"grupo-{int(m.group(1)):02d}"
    return valor.rstrip("-")


def localizar_pasta(raiz: Path, grupo: str) -> Path | None:
    base = raiz / GRUPOS_DIR
    if not base.is_dir():
        return None
    if grupo.startswith("grupo-") and (base / grupo).is_dir():
        return base / grupo
    candidatos = sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith(grupo + "-"))
    if len(candidatos) == 1:
        return candidatos[0]
    if len(candidatos) > 1:
        nomes = ", ".join(c.name for c in candidatos)
        raise ValueError(f"grupo ambiguo '{grupo}': {nomes}")
    return None


def arquivos_do_grupo(pasta: Path) -> list[Path]:
    return sorted(p for p in pasta.rglob("*") if p.is_file())


def tem_acento_ou_maiuscula(nome: str) -> bool:
    if nome != unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode():
        return True
    return nome != nome.lower()


def checar_nomes(pasta: Path, rel: Relatorio) -> None:
    for arq in arquivos_do_grupo(pasta):
        nome = arq.name
        if nome == ".gitkeep" or nome in NOMES_CONSAGRADOS:
            continue
        relativo = arq.relative_to(pasta.parent)
        if tem_acento_ou_maiuscula(nome):
            rel.erro(f"nome fora do padrao kebab-case (minusculo, sem acento): {relativo}")
        elif not RE_NOME_OK.match(nome):
            rel.erro(f"nome com caractere invalido (use [a-z0-9._-]): {relativo}")
        if " " in nome:
            rel.erro(f"nome com espaco: {relativo}")
        for proibido in PROIBIDOS:
            if proibido in str(relativo):
                rel.erro(f"arquivo que nao deve ser versionado: {relativo}")


def checar_estrutura(pasta: Path, rel: Relatorio, marco: str | None) -> None:
    for nome in ARQUIVOS_OBRIGATORIOS:
        if not (pasta / nome).is_file():
            rel.erro(
                f"arquivo obrigatorio ausente: {nome} "
                f"(veja docs/templates/)"
            )
    minimos = MINIMOS_MARCO.get(marco or "", {})
    for nome in PASTAS_OBRIGATORIAS:
        alvo = pasta / nome
        if not alvo.is_dir():
            rel.erro(f"pasta obrigatoria ausente: {nome}/")
            continue
        reais = [p for p in alvo.iterdir() if p.name != ".gitkeep"]
        minimo = minimos.get(nome, 0)
        if not reais:
            if minimo:
                rel.erro(f"pasta vazia para o marco {marco}: {nome}/ (minimo {minimo} arquivo(s))")
            else:
                rel.aviso(f"pasta vazia (sem artefatos): {nome}/")
        elif minimo and len(reais) < minimo:
            rel.erro(
                f"pasta {nome}/ tem {len(reais)} arquivo(s); "
                f"o marco {marco} exige no minimo {minimo}"
            )



def checar_diagramas(pasta: Path, rel: Relatorio) -> None:
    for arq in pasta.rglob("*"):
        if not arq.is_file() or arq.suffix.lower() not in FONTES_DIAGRAMA:
            continue
        tem_export = any(
            (arq.with_suffix(ext)).is_file() for ext in EXPORTS_DIAGRAMA
        )
        if not tem_export:
            rel.erro(
                f"diagrama sem exportacao: {arq.relative_to(pasta.parent)} "
                f"(entregue .png, .svg ou .pdf ao lado da fonte)"
            )


def checar_artefatos(pasta: Path, rel: Relatorio) -> None:
    for sub, prefixos in PREFIXO_ARTEFATO.items():
        alvo = pasta / sub
        if not alvo.is_dir():
            continue
        for arq in sorted(alvo.glob("*.md")):
            nome = arq.name.lower()
            if not nome.startswith(prefixos):
                rel.erro(
                    f"artefato sem prefixo de ID em {sub}/: {arq.name} "
                    f"(esperado ex.: {prefixos[0]}XX-NN-nome.md)"
                )
            ids = set(RE_ID.findall(arq.read_text(encoding="utf-8").upper()))
            if not ids:
                rel.aviso(f"nenhum identificador (RF/UC/CT/ADR-GXX-NN) em {arq.relative_to(pasta)}")


def checar_matriz(pasta: Path, rel: Relatorio, marco: str | None) -> None:
    matriz = pasta / "matriz-rastreabilidade.md"
    if not matriz.is_file():
        return
    texto = matriz.read_text(encoding="utf-8")
    linhas = [ln for ln in texto.splitlines() if ln.strip().startswith("|")]
    corpo = [ln for ln in linhas if not re.match(r"^\|\s*-{2,}", ln) and "---" not in ln]
    if len(corpo) < 3:
        rel.erro("matriz de rastreabilidade sem linhas de requisito")
        return
    if not re.search(r"\|\s*RF-G\d{2}-\d{2}", texto):
        rel.erro("matriz sem nenhum identificador RF-GXX-NN")
    pendentes = len(re.findall(r"pendente", texto, flags=re.I))
    total = len(re.findall(r"RF-G\d{2}-\d{2}", texto))
    if pendentes:
        if marco == "M3":
            rel.erro(f"matriz com {pendentes} marcacao(oes) 'pendente' no marco M3")
        elif total and pendentes >= total:
            rel.aviso("matriz ainda com todos os requisitos marcados como pendentes")


def checar_placeholders(pasta: Path, rel: Relatorio, marco: str | None) -> None:
    for arq in arquivos_do_grupo(pasta):
        if arq.suffix.lower() not in (".md",):
            continue
        texto = arq.read_text(encoding="utf-8").lower()
        achados = [p for p in PLACEHOLDERS if p in texto]
        if not achados:
            continue
        msg = f"placeholder em {arq.relative_to(pasta.parent)}: {', '.join(achados)}"
        if marco == "M3":
            rel.erro(msg + " (proibido no marco M3)")
        else:
            rel.aviso(msg)



def checar_escopo(pasta: Path, raiz: Path, base: str, rel: Relatorio) -> None:
    cmd = ["git", "-C", str(raiz), "diff", "--name-only", f"{base}...HEAD"]
    try:
        saida = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        rel.aviso(f"nao foi possivel comparar com {base}: {exc}")
        return
    if saida.returncode != 0:
        rel.aviso(
            f"git diff contra '{base}' falhou ({saida.stderr.strip()[:120]}); "
            f"rode 'git fetch' e confira a branch base"
        )
        return
    permitido = str(pasta.relative_to(raiz)) + "/"
    for linha in saida.stdout.splitlines():
        caminho = linha.strip()
        if not caminho:
            continue
        if not (caminho + "/").startswith(permitido) and not caminho.startswith(permitido):
            rel.erro(
                f"arquivo alterado FORA da pasta do grupo ({permitido}): {caminho}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida a entrega de um grupo do projeto SAPH-Clin."
    )
    parser.add_argument("--grupo", required=True, help="ex.: grupo-02, g2 ou 02")
    parser.add_argument("--raiz", default=".", help="raiz do repositorio (default: .)")
    parser.add_argument(
        "--base",
        help="branch/base para checar escopo (ex.: origin/main). Sem isso o escopo nao e verificado.",
    )
    parser.add_argument(
        "--marco",
        choices=("M1", "M2", "M3"),
        help="marco da entrega: define o minimo de artefatos por pasta e a tolerancia a pendencias",
    )
    parser.add_argument("--strict", action="store_true", help="trata AVISO como ERRO")
    args = parser.parse_args()

    raiz = Path(args.raiz).resolve()
    if not (raiz / GRUPOS_DIR).is_dir():
        print(f"ERRO: nao encontrei '{GRUPOS_DIR}/' em {raiz}", file=sys.stderr)
        return 2

    chave = normalizar_grupo(args.grupo)
    try:
        pasta = localizar_pasta(raiz, chave)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2
    if pasta is None:
        existentes = sorted(p.name for p in (raiz / GRUPOS_DIR).iterdir() if p.is_dir())
        print(f"ERRO: grupo '{args.grupo}' nao encontrado.", file=sys.stderr)
        print("Disponiveis: " + ", ".join(existentes), file=sys.stderr)
        return 2

    if not RE_GRUPO.match(pasta.name):
        print(
            f"ERRO: pasta '{pasta.name}' fora do padrao grupo-NN-nome-em-kebab-case",
            file=sys.stderr,
        )
        return 2

    rel = Relatorio()
    checar_estrutura(pasta, rel, args.marco)
    checar_nomes(pasta, rel)
    checar_diagramas(pasta, rel)
    checar_artefatos(pasta, rel)
    checar_matriz(pasta, rel, args.marco)
    checar_placeholders(pasta, rel, args.marco)
    if args.base:
        checar_escopo(pasta, raiz, args.base, rel)

    codigo = rel.imprimir(pasta.name, pasta, args.marco)
    if codigo == 0 and args.strict and rel.avisos:
        print("RESULTADO (--strict): REPROVADO por AVISOs")
        return 1
    return codigo


if __name__ == "__main__":
    sys.exit(main())
