# The Elements of Statistical Learning (ESL) — Hastie, Tibshirani, Friedman

> Nota conceitual (síntese própria, não reproduz o texto original). PDF oficial
> gratuito: hastie.su.domains/ElemStatLearn/. Referência de modelagem preditiva.

## Ideia central

Aprendizado supervisionado é estimar uma função preditiva controlando o
**trade-off viés×variância** para minimizar erro **fora da amostra**, não
dentro dela.

## Conceitos-âncora

- **Viés×variância:** modelo simples = viés alto, variância baixa; modelo
  complexo = viés baixo, variância alta. Erro de teste é U: existe um ponto
  ótimo de complexidade.
- **Overfitting:** erro de treino baixo com erro de teste alto. Erro de treino
  **não** estima desempenho real.
- **Validação cruzada (k-fold):** estimativa honesta de erro fora da amostra e
  base para seleção de modelo/hiperparâmetro. Toda escolha de modelo passa por
  dado não visto.
- **Maldição da dimensionalidade:** em alta dimensão tudo fica esparso e
  distante; mais variáveis sem mais dados pioram a generalização.

## Métodos e quando

- **Linear / OLS:** interpretável, baseline obrigatório.
- **Regularização — Ridge (L2):** encolhe coeficientes, lida com
  multicolinearidade. **Lasso (L1):** encolhe e zera (seleção de variável).
  Elastic net combina. Padrão quando há muitas variáveis correlacionadas.
- **Logística / LDA:** classificação interpretável.
- **Árvores:** capturam interação e não linearidade; sozinhas têm variância
  alta.
- **Ensembles:** *bagging/Random Forest* reduz variância; *boosting / gradient
  boosting* reduz viés sequencialmente — costuma ser o mais preciso em dado
  tabular, ao custo de interpretabilidade.
- **Não supervisionado:** PCA (redução de dimensão), clustering (k-means,
  hierárquico) — exploratório, sem rótulo de verdade.

## Armadilhas que o livro enfatiza

- **Data leakage:** qualquer pré-processamento (seleção de variável, escala,
  imputação) ajustado fora do fold da CV vaza o teste para o treino e infla o
  resultado.
- Selecionar variável olhando todo o dataset e só depois validar = otimismo
  falso.
- Acurácia engana sob classes desbalanceadas — olhar precisão/recall/AUC.

## Como o squad aplica

- `estatistico-bigdata`: CV obrigatória para qualquer escolha de modelo;
  reportar erro fora da amostra; preferir o modelo mais simples competitivo.
- `analista-critico`: caçar leakage e seleção de variável pré-validação como
  falha 🔴; questionar acurácia em base desbalanceada.
- `analista-dados`: padronizar/imputar dentro do pipeline de validação.
