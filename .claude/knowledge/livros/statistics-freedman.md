# Statistics — Freedman, Pisani & Purves

> Nota conceitual (síntese própria, não reproduz o texto original). Referência
> de rigor em desenho de estudo e no que um teste de fato significa.

## Ideia central

A qualidade da conclusão é determinada pelo **desenho do estudo**, não pela
sofisticação da conta. Experimento controlado > estudo observacional.

## Desenho de estudo

- **Experimento controlado:** tratamento atribuído pelo pesquisador; com
  **randomização** e **duplo-cego**, controla confundidores conhecidos e
  desconhecidos. Padrão-ouro para causa.
- **Estudo observacional:** o sujeito se autosseleciona ao grupo. Associação
  pode ser real, mas o **confundidor** é a explicação alternativa default.
  Ajuste estatístico ajuda, mas nunca elimina confundidor não medido.
- Pergunta-chave antes de inferir causa: *isto é experimento ou observação?*

## Descritiva e correlação

- Média e DP resumem bem só distribuições aproximadamente simétricas; em
  assimétricas use mediana/percentis.
- **Coeficiente r:** mede só associação **linear**. Cuidado com:
  não linearidade, outliers que inflam/deflacionam r, **correlação ecológica**
  (r de médias de grupos exagera o r individual), restrição de amplitude.
- Correlação não é causa: pode haver causa reversa ou variável de confusão.

## Efeito e falácia de regressão

- **Regression effect:** em duas medidas correlacionadas, casos extremos na
  primeira tendem a ficar menos extremos na segunda (puro acaso, não causa).
- **Regression fallacy:** atribuir esse retorno à média a uma intervenção
  ("piorei, fiz X, melhorei → X funcionou"). Vital em autoexperimentos.

## Inferência

- **Modelo da caixa (box model):** todo cálculo de erro padrão exige um modelo
  explícito do processo de sorteio. Sem modelo de chance, não há erro padrão.
- **Teste de significância:** P-valor = probabilidade dos dados (ou mais
  extremos) **se H0 for verdadeira**. NÃO é a probabilidade de H0, nem o
  tamanho do efeito, nem prova de relevância prática.
- Significância em **estudo observacional** não resolve confundidor: um
  P pequeno num desenho viciado continua viciado.
- Significância estatística ≠ importância prática.

## Como o squad aplica

- `estatistico-bigdata`: declarar sempre experimento vs. observação e o modelo
  de chance; nunca vender P-valor como probabilidade de hipótese.
- `analista-critico`: confundidor é a hipótese nula default em dado
  observacional; checar falácia de regressão em todo "fiz X e melhorou".
- `analista-comportamento-consumidor`: autorrelato é observacional —
  autosseleção e confundidor antes de qualquer "porquê".
