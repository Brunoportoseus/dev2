# How to Lie with Statistics — Darrell Huff

> Nota conceitual (síntese própria, não reproduz o texto original). Manual de
> defesa contra estatística enganosa. Use como checklist antiembuste.

## Ideia central

Números parecem objetivos, mas a forma de coletar, resumir e plotar embute
escolhas que distorcem. O leitor crítico desconfia do número antes de aceitá-lo.

## Truques de distorção a reconhecer

- **Amostra viciada (biased sample):** quem respondeu não representa a
  população. Pergunte sempre como a amostra foi obtida e quem ficou de fora.
- **A média bem escolhida:** "média" sem dizer se é média aritmética, mediana
  ou moda. Em distribuição assimétrica (renda, gasto), a média esconde a
  cauda. Exija a mediana e a dispersão.
- **n omitido / amostra pequena:** porcentagem sem base. "70% preferiram" com
  n=10 não é nada. Sem n, sem conclusão.
- **Erro provável escondido:** diferença menor que a margem de erro
  apresentada como tendência.
- **Gee-whiz graph:** eixo Y truncado (não começa em zero ou quebra de escala)
  amplifica visualmente uma variação pequena.
- **Pictograma unidimensional:** dobrar a altura de um ícone quadruplica a
  área percebida — exagero visual.
- **Número semiconectado (semiattached figure):** prova-se uma coisa e
  anuncia-se outra ("X vendeu mais" → "X é melhor").
- **Post hoc / correlação vira causa:** A e B andam juntos, logo A causa B —
  ignorando terceira variável e acaso.

## As 5 perguntas para "responder a uma estatística"

1. **Quem diz isso?** Há viés/interesse de quem produziu o número?
2. **Como ele sabe?** Amostra adequada? Como foi medido?
3. **O que está faltando?** Falta o n, a base, o erro, a comparação?
4. **Alguém mudou de assunto?** O dado bruto vira outra coisa na conclusão?
5. **Faz sentido?** A magnitude é plausível no mundo real?

## Como o squad aplica

- `analista-critico`: este é o checklist de objeções padrão.
- `analista-dados`: nunca reportar % sem n; nunca truncar eixo sem rótulo.
- `analista-ba`: desconfiar de métrica de vaidade e de "média" sem dispersão.
- Regra: todo gráfico com eixo não iniciando em zero declara isso
  explicitamente.
