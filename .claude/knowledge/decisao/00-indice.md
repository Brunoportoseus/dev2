# Base de Conhecimento — Squad de Decisão / Pesquisa Operacional

> Todos os agentes da squad de decisão leem esta pasta antes de analisar.
> A squad transforma **qualquer problema ou decisão** (não só o exemplo do
> carro) em um modelo matemático com probabilidades.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `pesquisa-operacional.md` | Transformar um problema vago em modelo formal: alternativas, objetivo, restrições, estados da natureza, payoff. |
| `arvore-de-decisao.md` | Nós de decisão/chance, valor esperado (EMV), rollback, valor da informação (EVPI/EVSI), utilidade e risco. |
| `probabilidades-e-simulacao.md` | De onde vêm as probabilidades, atualização bayesiana, distribuições, Monte Carlo, como ler "P(ser a melhor decisão)". |
| `elicitacao-e-vieses.md` | Roteiro de perguntas detalhadas (intake) e vieses de decisão a evitar. |
| `formato-entrada.md` | Esquema do arquivo que alimenta a ferramenta `decisao.py`. |

## Ferramenta

`/.claude/tools/decisao/decisao.py` — motor genérico (árvore de decisão +
Monte Carlo). Exemplos em `.claude/tools/decisao/exemplos/`
(`carro.yaml` resolvido, `template.yaml` em branco).

```
python3 .claude/tools/decisao/decisao.py <modelo>.yaml
```

## Princípio-mestre

Nenhuma decisão é analisada antes de estar **formalizada e quantificada**:
alternativas mutuamente exclusivas, objetivo único, incertezas como
distribuições, e a saída sempre como **probabilidade de cada decisão ser a
melhor** — não como opinião.
