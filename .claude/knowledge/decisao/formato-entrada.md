# Formato do arquivo de entrada — `decisao.py`

> Esquema do modelo lido pela ferramenta. YAML ou JSON. Genérico para
> qualquer decisão. Exemplos: `.claude/tools/decisao/exemplos/`.

## Estrutura geral

```yaml
problema: "texto livre — a decisão"
objetivo: "o que o número representa"
sentido: max | min          # max = ganho/utilidade; min = custo
moeda: "R$"                  # rótulo (opcional)
horizonte_meses: 30          # informativo (opcional)
iteracoes: 50000             # iterações Monte Carlo (default 50000)
seed: 42                     # reprodutibilidade
limiar_bom_negocio: 0        # opcional: limiar p/ P(bom resultado)

parametros: { ... }          # incertezas (distribuições)
alternativas: [ ... ]        # 2+ decisões possíveis
```

`sentido: max` → "bom" = payoff ≥ limiar. `sentido: min` → "bom" = payoff ≤ limiar.

## Distribuições (`parametros`)

Cada parâmetro é um nome → especificação. Um número puro = constante.

| `dist` | Campos | Uso |
|---|---|---|
| `const` | `valor` | valor fixo |
| `uniforme` | `min`, `max` | só faixa conhecida |
| `triangular` | `min`, `moda`, `max` | 3 estimativas |
| `pert` | `min`, `moda`, `max`, `lambda?` | 3 estimativas (suaviza extremos) |
| `normal` | `media`, `desvio` | erro simétrico |
| `lognormal` | `media_log`, `desvio_log` | quantidade positiva multiplicativa |
| `bernoulli` | `p` | evento sim/não (gera 0/1) |
| `discreta` | `valores`, `probs` | poucos cenários |
| `beta` | `alpha`, `beta` | proporção/probabilidade em [0,1] |

```yaml
parametros:
  desval_30m:   { dist: pert, min: 0.30, moda: 0.42, max: 0.55 }
  manut_ano:    { dist: normal, media: 9000, desvio: 3000 }
  prob_falha:   { dist: pert, min: 0.20, moda: 0.30, max: 0.45 }
```

## Alternativas

Cada alternativa tem `nome`, opcional `constantes`, e **`formula`** OU
**`arvore`**.

### Via fórmula

Expressão aritmética sobre constantes + parâmetros amostrados.
Operadores: `+ - * / ** %`. Funções: `min max abs round exp log sqrt floor
ceil`. Condicional: `(a if cond else b)`. Comparações: `< <= > >= == !=`.
Sem acesso a builtins/atributos (avaliação restrita por AST — seguro).

```yaml
- nome: "Comprar novo"
  constantes: { preco: 100000 }
  formula: "preco - venda_usado - preco*(1-desval_30m) + manut_novo"
```

### Via árvore de decisão

Nós: `tipo: chance` (ramos com probabilidade), `tipo: decisao`
(escolhe o melhor ramo), `tipo: folha` (`valor:` ou `formula:`).

Probabilidade de um ramo de chance:
- `p: 0.3` — constante
- `p_var: prob_falha` — vem de um parâmetro (permite probabilidade incerta)
- `p_resto: true` — absorve `1 − soma(demais)`

```yaml
- nome: "Manter usado"
  constantes: { anos: 2.5 }
  arvore:
    tipo: chance
    ramos:
      - p_var: prob_falha
        tipo: folha
        formula: "manut_ano*anos + custo_pane - residual"
      - p_resto: true
        tipo: folha
        formula: "manut_ano*anos - residual"
```

## Saída

- **EMV (rollback)**: valor esperado determinístico (parâmetros no centro).
- **Monte Carlo** por alternativa: média, p5–p95, **P(ser a melhor decisão)**,
  **P(bom resultado)** vs. limiar.
- **Recomendação** + **tornado**: quais incertezas podem virar a decisão.

## Execução

```
python3 .claude/tools/decisao/decisao.py modelo.yaml
python3 .claude/tools/decisao/decisao.py modelo.json --json saida.json
```
