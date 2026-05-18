# Probabilidades e Simulação

> De onde vêm os números de probabilidade e como a simulação produz
> "P(esta decisão é a melhor) = X%".

## De onde vem cada probabilidade (em ordem de preferência)

1. **Dado próprio** (histórico do usuário): frequência observada. Reporte n.
2. **Base rate / dado de mercado**: estatística de referência do domínio
   (ex.: curva de desvalorização do modelo, taxa de falha do componente).
3. **Atualização bayesiana**: combine base rate (prior) com evidência
   específica. posterior ∝ verossimilhança × prior. Não ignore a base rate.
4. **Elicitação de especialista / do próprio usuário**: peça 3 pontos —
   mínimo plausível, mais provável, máximo plausível → vira distribuição
   (triangular ou PERT). Calibre: "você apostaria nisso?".

Nunca apresente uma probabilidade sem dizer de onde veio e quão incerta é.

## Escolha da distribuição

| Situação | Distribuição |
|---|---|
| 3 estimativas (mín/moda/máx), assimétrica | PERT (ou triangular) |
| Só faixa, sem moda | uniforme |
| Erro simétrico em torno de média | normal |
| Quantidade positiva multiplicativa (preço, custo) | lognormal |
| Evento sim/não | bernoulli |
| Poucos cenários discretos | discreta (valores+probs) |
| Probabilidade incerta (ex.: p de falha) | pert/beta sobre [0,1] |

A própria probabilidade pode ser incerta — modele-a como distribuição e
deixe a árvore usá-la (incerteza de segunda ordem).

## Monte Carlo: como nasce "P(ser a melhor decisão)"

1. Sorteia-se um valor de cada incerteza conforme sua distribuição.
2. Calcula-se o payoff de **todas** as alternativas nesse mesmo cenário.
3. Marca-se qual alternativa venceu (melhor objetivo) naquele cenário.
4. Repete-se N vezes (ex.: 50.000).
5. **P(alternativa A é a melhor)** = fração de cenários em que A venceu.

Saídas a sempre reportar por alternativa: média, p5–p50–p95, P(ser a melhor),
P(bom resultado vs. limiar), e risco de downside.

## Interpretação honesta

- "P(comprar é a melhor) = 64%" significa: em 64% dos cenários plausíveis
  modelados, comprar saiu melhor — **dado o modelo e as distribuições**. Não
  é certeza nem profecia; muda se as premissas mudarem.
- Probabilidade próxima de 50/50 = decisão **insensível**: o modelo não
  distingue as opções; busque mais informação ou decida por critério
  secundário (risco, reversibilidade).
- Use a **mesma amostra** (mesmo seed/cenário) para comparar alternativas —
  comparação pareada reduz ruído.
- Distinga incerteza **aleatória** (irredutível) de **epistêmica** (some com
  mais dado): só a segunda justifica pagar por informação (ver EVPI).
