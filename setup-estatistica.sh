#!/usr/bin/env bash
#
# Transfere a "ferramenta completa" de decisão do repositório planoa
# para o repositório separado Brunoportoseus/estat-stica.
#
# Rode no SEU computador (precisa ter acesso/login git aos dois repositórios):
#
#     bash setup-estatistica.sh
#
# O script: clona o estat-stica, copia os arquivos da ferramenta a partir
# da branch da squad no planoa, organiza o layout para GitHub Pages e faz
# commit + push. Não apaga nada do planoa (isso é um passo separado).

set -euo pipefail

PLANOA_REPO="https://github.com/Brunoportoseus/planoa.git"
PLANOA_BRANCH="claude/create-data-analysis-squad-dnba3"
ESTAT_REPO="https://github.com/Brunoportoseus/estat-stica.git"
ESTAT_BRANCH="main"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo ">> Clonando planoa (branch da ferramenta)..."
git clone --depth 1 -b "$PLANOA_BRANCH" "$PLANOA_REPO" "$TMP/planoa"

echo ">> Clonando estat-stica..."
git clone "$ESTAT_REPO" "$TMP/estat"

SRC="$TMP/planoa/.claude/tools/decisao"
DST="$TMP/estat"

echo ">> Copiando a ferramenta completa..."
cp "$SRC/decisao.html" "$DST/index.html"      # vira a home do Pages
cp "$SRC/decisao.py"   "$DST/decisao.py"
mkdir -p "$DST/exemplos"
cp "$SRC/exemplos/"*.yaml "$DST/exemplos/"

# README mínimo do novo repositório
cat > "$DST/README.md" <<'EOF'
# Estatística & Decisão

Ferramenta de análise de decisão (árvore de decisão + simulação de Monte
Carlo) que transforma qualquer problema/decisão em probabilidades.

- `index.html` — interface web (abre no navegador, sem servidor)
- `decisao.py` — versão linha de comando: `python3 decisao.py exemplos/carro.yaml`
- `exemplos/` — `carro.yaml` (resolvido) e `template.yaml` (em branco)

Publicado via GitHub Pages: Settings > Pages > Deploy from a branch >
`main` / `root`.
EOF

cd "$DST"
git add index.html decisao.py exemplos README.md
if git diff --cached --quiet; then
  echo ">> Nada novo para commitar (já estava igual)."
else
  git commit -m "Adiciona ferramenta de Estatística & Decisão (web + CLI + exemplos)"
  git push origin "$ESTAT_BRANCH"
  echo ">> Enviado para $ESTAT_REPO ($ESTAT_BRANCH)."
fi

cat <<'EOF'

==================================================================
PRONTO. Agora, no GitHub do repositório estat-stica:
  Settings > Pages > Source: "Deploy from a branch"
  Branch: main  /  pasta: / (root)  > Save

URL final (alguns minutos para propagar):
  https://brunoportoseus.github.io/estat-stica/
==================================================================
EOF
