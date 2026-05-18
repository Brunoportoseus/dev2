# Estatística & Decisão

Ferramenta e squad de análise para transformar **qualquer problema ou
decisão** em um cálculo com probabilidades: Pesquisa Operacional + árvore
de decisão + simulação de Monte Carlo.

## Site (GitHub Pages)

A página inicial (`index.html`) é a ferramenta web — abre no navegador,
sem servidor, e roda a simulação localmente.

`https://brunoportoseus.github.io/estatistica/`

## Conteúdo

| Caminho | O que é |
|---|---|
| `index.html` | Interface web da ferramenta (página inicial do site). |
| `.claude/tools/decisao/decisao.py` | Mesmo motor em linha de comando. |
| `.claude/tools/decisao/exemplos/` | `carro.yaml` (resolvido) e `template.yaml` (em branco). |
| `.claude/agents/` | Squad de Decisão (líder, modelador PO, árvore de decisão, probabilidades, crítico) e squad de Análise de Dados. |
| `.claude/knowledge/decisao/` | Base de conhecimento: PO, árvore de decisão, probabilidades/simulação, elicitação e formato de entrada. |

## Uso rápido

**Web:** abra `index.html` (ou o site no Pages) → *Carregar exemplo (carro)*
ou preencha problema, incertezas e alternativas → *Rodar análise*.

**CLI:**

```bash
python3 .claude/tools/decisao/decisao.py .claude/tools/decisao/exemplos/carro.yaml
```

**Conversa:** acione o agente `lider-squad-decisao` — ele faz as perguntas
detalhadas, monta o modelo e devolve a probabilidade de cada decisão ser a
melhor.

A saída sempre traz, por alternativa: probabilidade de ser a melhor decisão,
valor esperado, intervalo p5–p95 e a sensibilidade (o que pode virar a
decisão).
