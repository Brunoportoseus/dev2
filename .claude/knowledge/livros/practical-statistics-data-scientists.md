# Practical Statistics for Data Scientists — Bruce, Bruce & Gedeck

> Nota conceitual (síntese própria, não reproduz o texto original). Ponte
> prática entre estatística clássica e ciência de dados; abordagem resampling-first.

## Ideia central

Para decidir na prática, estatística robusta + reamostragem (bootstrap,
permutação) costuma ser mais segura e intuitiva que fórmulas paramétricas
sensíveis a suposições.

## EDA e estimativas robustas

- Localização: **mediana** e média aparada resistem a outlier; média não.
- Dispersão: **MAD** e IQR resistem; desvio-padrão é sensível a cauda.
- Sempre olhar a distribuição (histograma, boxplot) antes de resumir num número.

## Distribuições amostrais e bootstrap

- Distinguir distribuição **dos dados** da distribuição **de uma estatística**
  (amostral). O erro padrão descreve a segunda.
- **Bootstrap:** reamostrar com reposição para obter erro padrão e intervalo
  de confiança sem supor normalidade. Default quando a fórmula é duvidosa.
- **IC** corretamente lido: faixa de incerteza do procedimento, não
  probabilidade sobre o parâmetro.

## Experimentos e significância

- **A/B test:** definir métrica, hipótese e tamanho de efeito mínimo **antes**.
- **Teste de permutação:** embaralhar rótulos para gerar a distribuição sob
  H0 — robusto e didático.
- **P-valor:** evidência contra H0, não probabilidade de H0; sempre
  acompanhar de tamanho de efeito.
- **Múltiplos testes:** quanto mais comparações, mais falsos positivos;
  corrigir (FDR/Bonferroni) ou pré-registrar a hipótese.
- **Poder:** sem n suficiente, "não significativo" não é "sem efeito".

## Regressão e classificação

- Regressão para **explicar** ≠ para **prever**: cuidado com multicolinearidade
  e confundidor ao interpretar coeficientes.
- Classificação: sob desbalanceamento, acurácia engana. Usar matriz de
  confusão, **precisão, recall, F1, AUC**; considerar reamostragem/peso de
  classe.

## Como o squad aplica

- `estatistico-bigdata`: bootstrap/permutação como default para IC e teste
  quando suposição paramétrica é frágil; declarar MDE e poder.
- `analista-dados`: estatística robusta (mediana/MAD/IQR) em dado pessoal com
  outlier; sempre ver a distribuição antes de resumir.
- `analista-critico`: cobrar correção de múltiplas comparações e métrica
  adequada sob classe desbalanceada.
