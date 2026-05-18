# Pesquisa Operacional — formalizar qualquer problema

> Como transformar uma decisão descrita em palavras ("vou comprar um carro",
> "troco de emprego?", "faço o curso?") em um modelo matemático resolvível.

## O que TODO problema de decisão tem

1. **Decisor e objetivo único.** O que se quer maximizar ou minimizar,
   numa só métrica (R$, tempo, utilidade). Múltiplos objetivos → combine em
   uma função (peso) ou trate como restrição.
2. **Alternativas** mutuamente exclusivas e coletivamente exaustivas. Inclua
   sempre a opção "não fazer nada / manter o status quo".
3. **Estados da natureza** (incertezas): o que não está sob controle do
   decisor (mercado, falha, demanda) — cada um vira uma distribuição.
4. **Payoff**: a conta que liga (alternativa × estado) → valor do objetivo.
5. **Restrições**: orçamento, prazo, limites legais/físicos — o que torna uma
   alternativa inviável (descarte-a, não a penalize artificialmente).
6. **Horizonte e taxa de desconto**: fluxos em datas diferentes não se somam
   direto; traga a valor presente quando o horizonte for longo.

## Roteiro de formalização

1. **Escreva a pergunta de decisão em uma frase.** "Devo X ou Y, para
   maximizar/minimizar Z, no horizonte H?"
2. **Liste alternativas** (mínimo 2; sempre inclua o status quo).
3. **Liste as incertezas** que mudam o resultado. Para cada uma: faixa
   plausível (mín, mais provável, máx) → vira distribuição.
4. **Escreva o payoff de cada alternativa** como fórmula sobre constantes
   conhecidas + incertezas. Decomponha (custo de aquisição − valor residual +
   operação + risco).
5. **Identifique restrições** e elimine alternativas inviáveis.
6. **Reduza ao essencial.** Modelo bom é o mais simples que ainda muda a
   decisão. Não modele o que não altera a escolha.

## Padrões de modelagem comuns (uso pessoal)

- **Custo total de propriedade (TCO):** aquisição + operação + manutenção +
  oportunidade − valor residual. Útil para comprar/trocar bens.
- **VPL / payback:** investimentos e projetos com fluxo no tempo.
- **Fila / espera:** quando o problema é tempo de espera vs. custo de
  capacidade (conceitual: λ, μ, utilização).
- **Estoque/lote:** quando comprar/quanto comprar (trade-off pedido × posse).
- **Atribuição/seleção sob restrição:** escolher o subconjunto de maior valor
  dado um limite (orçamento, tempo).

## Padrões inegociáveis

- Objetivo e horizonte definidos por escrito antes de qualquer conta.
- Sempre incluir o status quo como alternativa.
- Toda incerteza relevante é uma distribuição, nunca um número "chutado" fixo.
- Restrição elimina alternativa; não vira penalidade arbitrária no payoff.
- O modelo é só tão bom quanto sua estrutura — simplicidade que preserva a
  decisão vence sofisticação que não muda a escolha.
