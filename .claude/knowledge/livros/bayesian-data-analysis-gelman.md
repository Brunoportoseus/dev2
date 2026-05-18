# Bayesian Data Analysis — Gelman, Carlin, Stern, Dunson, Vehtari, Rubin

> Nota conceitual (síntese própria, não reproduz o texto original). 3ª ed.
> disponível gratuitamente: stat.columbia.edu/~gelman/book/. Referência máxima
> em inferência bayesiana aplicada.

## Ideia central

Inferência bayesiana = atualização de crença. Todo parâmetro é incerto;
expressamos essa incerteza como distribuição de probabilidade, atualizamos com
dados via teorema de Bayes, e comunicamos o resultado como distribuição posterior
— não como ponto único com p-valor.

## Equação fundamental

```
posterior ∝ likelihood × prior
p(θ | y) ∝ p(y | θ) · p(θ)
```

- **Prior p(θ):** crença antes dos dados. Não é arbitrário: use **prior
  fracamente informativo** (concentra em valores plausíveis, não domina o
  posterior com n razoável). Prior vago demais causa problemas computacionais.
- **Likelihood p(y|θ):** como os dados foram gerados dado o parâmetro.
- **Posterior p(θ|y):** distribuição completa do parâmetro após os dados.
  É a saída; dela extraímos IC (credibility interval), média, mediana etc.

## Por que usar abordagem bayesiana

- O IC bayesiano (intervalo de credibilidade) tem a interpretação que leigos
  esperam do IC frequentista: "há 95% de probabilidade de θ estar neste
  intervalo" — mas frequentista não suporta esta frase.
- Propaga incerteza naturalmente por modelos hierárquicos.
- Incorpora conhecimento prévio de forma explícita e auditável.
- Funciona bem com n pequeno desde que o prior seja justificado.

## Modelos hierárquicos (multilevel)

Estrutura para dados com grupos: parâmetros de grupo estimados conjuntamente
puxados em direção a uma distribuição de nível superior.

- **Pooling completo:** ignora grupos — viés alto.
- **Sem pooling:** estima cada grupo separadamente — variância alta (overfitting
  em grupos pequenos).
- **Pooling parcial (hierárquico):** compromisso ótimo. Grupos com menos dados
  são mais "encolhidos" para a média global (shrinkage). É a solução bayesiana
  padrão para análises segmentadas.

## Verificação do modelo (Bayesian workflow)

1. **Especifique** o modelo (prior + likelihood).
2. **Estime** a distribuição posterior (MCMC, variational inference).
3. **Verifique** com **posterior predictive check**: simule dados do modelo e
   compare com dados reais. Se simulação não parece dados reais, o modelo está
   errado — expanda ou revise.
4. **Expanda** ou simplifique conforme necessário.

## MCMC e diagnósticos

- **R-hat (Rhat):** convergência. Rhat < 1.01 em todas as cadeias = OK.
  Rhat > 1.1 = problema grave, conclusões inválidas.
- **ESS (effective sample size):** amostras independentes efetivas. ESS < 400
  → incerteza nas estimativas de cauda.
- **Trace plot:** inspecionar visualmente mistura e estacionariedade.

## Comparação de modelos

- Preferir **LOO-CV** (leave-one-out cross-validation) ou **WAIC** a Bayes
  factors para comparar modelos — mais estáveis e menos sensíveis ao prior.
- Bayes factors são muito sensíveis ao prior difuso — evitar sem justificativa
  forte.

## Como o squad aplica

- `estatistico-bigdata`: use abordagem bayesiana quando n é pequeno, quando
  há conhecimento prévio legítimo a incorporar, ou quando um modelo hierárquico
  é necessário (grupos com tamanhos diferentes). Sempre reportar R-hat e ESS.
- `analista-critico`: verificar se prior foi justificado; exigir posterior
  predictive check antes de aceitar conclusão; R-hat > 1.1 = invalidar 🔴.
- `analista-ba`: intervalo de credibilidade é mais direto para comunicar
  incerteza em metas/previsões do que IC frequentista.
