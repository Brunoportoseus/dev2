# Classification and Regression Tree Analysis — Jake Morgan (BU, 2014)

> Nota baseada no relatório técnico "Classification and Regression Tree Analysis"
> (Technical Report No. 1, Boston University School of Public Health, 2014).
> Documento de domínio público/acadêmico. Referência seminal: Breiman, Friedman,
> Olshen & Stone, "Classification and Regression Trees", 1984.

## Ideia central

CART é particionamento recursivo do espaço de dados: divide o dataset em
subconjuntos onde as interações entre variáveis ficam mais claras, construindo
uma árvore interpretável que identifica as variáveis com maior poder explicativo.

## Dois tipos de árvore

- **Árvore de classificação:** variável resposta categórica (binária). Critério
  de divisão = **índice de impureza Gini** (1 − Σp²(c|l)) — cada divisão
  maximiza a diminuição de impureza. Métrica final: taxa de misclassificação.
- **Árvore de regressão:** variável resposta contínua. Critério = **erro
  quadrático médio** (MSE). Cada nó terminal retorna a média da resposta no
  subconjunto (modelo constante por partes).

## Anatomia da árvore

- **Raiz (root):** primeira divisão — variável de maior poder explicativo global.
- **Nó interno (split):** cada divisão subsequente, condicional ao ramo anterior.
- **Folha/nó terminal (leaf):** partição final — sem divisão adicional útil.
- Navegar pelos ramos = modelagem condicional; descer um nível = condicionar
  em uma variável adicional.

## Critério de parada e poda (pruning)

Árvore crescida ao máximo overfita. Técnicas para controlar:
- **Parâmetro de complexidade (cp):** penaliza tamanho; o valor ótimo é
  encontrado por validação cruzada.
- **Poda custo-complexidade:** remove nós que reduzem misclassificação menos
  do que o custo de tê-los.

## Vantagens práticas

- Lida com variáveis contínuas e categóricas sem pré-processamento.
- Detecta interações entre variáveis automaticamente.
- Resultado visual e interpretável por não estatísticos — ponte entre rigor
  estatístico e comunicação com especialistas de domínio.
- Não paramétrico: sem suposição de linearidade ou distribuição.

## Limitações e armadilhas

- **Instabilidade:** pequena mudança nos dados altera muito a estrutura da
  árvore (alta variância). Use ensemble para mitigar.
- **Poder preditivo inferior** a métodos de ensemble em dados tabulares.
- Suscetível a divisões espúrias em amostras pequenas — valide com CV.
- Misclassification rate de 24% em publicações é comum; interpretar com cautela.

## Extensões

- **Bagging (Bootstrap Aggregating):** cria múltiplos datasets por bootstrap,
  roda CART em cada um e agrega — reduz variância. Útil para árvores instáveis.
  Random Forest é a extensão mais conhecida.
- **Boosting:** treina classificadores sequencialmente pesando mais os casos
  misclassificados anteriores — reduz misclassificação em "weak learners"
  (dados com misclassificação próxima de 50%).
- Regra prática: **bagging** quando a árvore é instável; **boosting** quando
  os dados são fracos/ruidosos.

## Implementação em R

```r
# Regressão
mytree <- tree(Y ~ x1 + x2 + ..., data = mydata)

# Classificação
myclass <- tree(factor(Y) ~ x1 + x2 + ..., data = mydata)

# Bagging
mybag <- bagging(Y ~ ., data = mydata, nbagg = 30, coob = TRUE)
```
Alternativa: `rpart` (mais extensível, melhor para surrogate variables).

## Como o squad aplica

- `analista-dados`: use CART como ferramenta de EDA para identificar as
  variáveis mais importantes antes de modelagem formal; a visualização
  facilita comunicar padrões.
- `estatistico-bigdata`: CART como baseline não paramétrico; preferir Random
  Forest/gradient boosting para performance preditiva; validar com CV.
- `analista-critico`: verificar se a árvore foi podada via CV (overfitting
  sem poda = achado falso); checar se variável-raiz é confundida por outra
  não incluída.
- `lider-squad-dados`: CART é útil para apresentar resultados exploratórios
  a partes interessadas sem background estatístico.
