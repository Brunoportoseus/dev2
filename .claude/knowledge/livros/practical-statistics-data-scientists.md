# Practical Statistics for Data Scientists — Bruce, Bruce & Gedeck

> Nota conceitual (síntese própria, não reproduz o texto original). Foco em
> aplicação prática com perspectiva de quem trabalha com dados reais.

## Ideia central

Estatística para cientistas de dados é ferramenta, não ritual. Priorize métodos
de **reamostragem** (bootstrap, permutação) sobre tabelas de distribuição
teórica — mais intuitivos e funcionam com n pequeno.

## Estimativas de localização e variabilidade

- Use **mediana e MAD** (desvio absoluto mediano) como estimativas robustas —
  resistem a outliers onde média e DP quebram.
- **Média truncada (trimmed mean):** compromisso útil entre média e mediana.
- Distribuição de dados ≠ distribuição amostral ≠ distribuição do estimador:
  confundir as três é erro clássico.

## Bootstrap e inferência por reamostragem

- **Bootstrap:** amostre com reposição do próprio dado para obter a distribuição
  do estimador sem suposição distribucional. Funciona para IC de qualquer
  estatística.
- **Teste de permutação:** embaralhe rótulos do tratamento e calcule a
  distribuição nula empiricamente. Equivalente ao teste t, mas sem suposição
  de normalidade; ideal para experimentos pessoais com n pequeno.
- Preferir bootstrap/permutação a p-valor teórico quando distribuição é
  desconhecida ou n < 30.

## Experimentos e testes A/B

- Defina **poder e tamanho mínimo de efeito** antes de coletar — não ajuste o
  n depois de ver o resultado (p-hacking disfarçado).
- **Múltiplos testes:** correção de Bonferroni ou Benjamini-Hochberg; testar
  muitas variações sem ajuste infla a taxa de falso positivo.
- Diferença estatisticamente significante ≠ diferença que muda a decisão.

## Regressão e previsão

- OLS: **interprete** coeficiente como variação marginal de Y controlando as
  demais — não como causa.
- **Multicolinearidade:** VIF > 5–10 → coeficientes individuais não confiáveis;
  use ridge ou lasso.
- Confundidor não medido não é resolvido por mais variáveis; é resolvido por
  desenho de experimento.
- Avaliar modelo por **RMSE/MAE no dado de teste**, não no treino.

## Classificação: avaliação honesta

- **Matriz de confusão** antes de qualquer métrica agregada.
- **Acurácia é enganosa** com classes desbalanceadas → use precisão, recall,
  F1, AUC-ROC.
- **AUC-ROC** mede discriminação; **curva precisão-recall** é mais informativa
  quando a classe positiva é rara.
- Estratégias para desbalanceamento: undersampling, oversampling (SMOTE),
  ajuste de peso de classe.

## Como o squad aplica

- `estatistico-bigdata`: bootstrap como primeira escolha para IC em dados
  pessoais (n pequeno, distribuição desconhecida); teste de permutação para
  comparações.
- `analista-dados`: nunca reportar só acurácia em classificação; matriz de
  confusão obrigatória.
- `analista-critico`: checar se n foi fixado antes do teste; desbalanceamento
  e AUC vs. acurácia como objeções frequentes.
