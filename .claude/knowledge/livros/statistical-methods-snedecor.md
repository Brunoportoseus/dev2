# Statistical Methods — Snedecor & Cochran

> Nota conceitual (síntese própria, não reproduz o texto original). 8ª ed.
> (1989). O manual clássico de métodos estatísticos aplicados — referência
> canônica para ANOVA, experimentos planejados e análise de dados biológicos.

## Ideia central

Estatística aplicada exige **planejamento antes da coleta**. O método de análise
é determinado pelo desenho do experimento; analisar dado coletado sem
planejamento com métodos de experimento planejado gera conclusões inválidas.

## Estatística descritiva e distribuições

- Média, variância, desvio padrão — definições de população vs. amostra.
- Distribuição normal: base para a maioria dos testes paramétricos.
- **Transformações:** quando dados são assimétricos ou heterocedásticos, aplicar
  log, raiz quadrada ou arco-seno antes da análise paramétrica é preferível a
  abandonar o método.

## Testes de hipótese clássicos

- **Teste t:** uma amostra, duas amostras independentes, amostras pareadas.
  Pressuposto: normalidade (robusto para n > 30 pelo TLC) e, no caso de duas
  amostras, variâncias iguais (teste F de Levene/Bartlett para verificar).
- **Teste F:** razão de variâncias; base do ANOVA.
- **Qui-quadrado:** dados categóricos, tabelas de contingência, goodness-of-fit.

## ANOVA — o coração do livro

- **One-way ANOVA:** compara médias de ≥ 3 grupos; decompõe variância total em
  "entre grupos" e "dentro de grupos". F = variância entre / variância dentro.
- **Two-way ANOVA:** dois fatores; permite estimar interação fator×fator — se
  interação significativa, efeitos principais não podem ser interpretados
  isoladamente.
- **ANOVA de medidas repetidas:** o mesmo sujeito em múltiplas condições;
  controla variabilidade entre sujeitos.
- **Pressupostos:** normalidade dos resíduos, homocedasticidade, independência.
  Violações moderadas: ANOVA é robusto; graves: use Kruskal-Wallis ou transforme.

## Comparações múltiplas pós-ANOVA

F significativo → ANOVA diz que "algo difere", não "o quê". Testes post hoc:
- **Tukey HSD:** controla taxa de erro por família; conservador; padrão.
- **Bonferroni:** mais conservador ainda; use quando há poucas comparações
  pré-planejadas.
- **LSD de Fisher:** liberal; evitar sem F global significativo.
- Nunca fazer t-tests múltiplos sem correção — infla erro tipo I.

## Desenho de experimentos

- **Blocos aleatorizados completos (RCBD):** grupos homogêneos (blocos) com
  tratamentos aleatorizados dentro; reduz variância residual.
- **Quadrado latino:** controla duas fontes de variação (linha + coluna);
  requer que tratamentos = linhas = colunas.
- **Fatoriais:** testam múltiplos fatores e interações simultaneamente;
  mais eficiente do que um experimento por vez.
- **Tamanho de amostra:** calcule o n necessário para detectar o efeito mínimo
  relevante com poder ≥ 80% — antes de coletar.

## Regressão e correlação

- Regressão linear: interpretar coeficiente como variação média de Y por
  unidade de X, mantidas as demais variáveis constantes.
- Verificar resíduos (normalidade, homocedasticidade, ausência de padrão).
- **ANCOVA:** combina ANOVA com regressão — ajusta comparação de grupos por
  covariável contínua (ex.: comparar grupos controlando por valor basal).
- Correlação de Pearson r: mede associação linear; testar H0: r=0 não é o
  mesmo que confirmar utilidade preditiva.

## Métodos não paramétricos

Para dados ordinais ou quando pressupostos paramétricos são gravemente violados:
- **Mann-Whitney U / Wilcoxon:** alternativa ao t de duas amostras.
- **Kruskal-Wallis:** alternativa ao one-way ANOVA.
- **Spearman ρ:** correlação de postos.
- Custo: menor poder estatístico; use paramétrico com transformação se possível.

## Como o squad aplica

- `estatistico-bigdata`: Snedecor é o protocolo padrão para comparar grupos em
  experimentos pessoais; sempre declarar o desenho (one-way, two-way, pareado)
  antes de rodar; verificar pressupostos nos resíduos.
- `analista-critico`: comparações múltiplas sem correção = falha 🔴; falta de
  teste de homocedasticidade = 🟡; ANOVA sem inspeção de resíduos = 🟡.
- `analista-dados`: transformação de dados é solução legítima — não é
  "manipulação"; documente a transformação e justifique.
