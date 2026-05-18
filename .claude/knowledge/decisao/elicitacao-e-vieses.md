# Elicitação (perguntas detalhadas) e Vieses de Decisão

> A squad NÃO inventa números. Antes de calcular, conduz uma entrevista
> estruturada até o modelo estar completo. Este é o roteiro.

## Roteiro de intake — perguntar até ter tudo

Pergunte em blocos; só calcule quando os obrigatórios estiverem preenchidos.

**A. A decisão**
- Qual é exatamente a decisão? Qual o prazo para decidir?
- Quais são TODAS as alternativas? (force incluir o status quo / não agir)
- O que torna esta decisão importante / o que muda se errar?

**B. O objetivo**
- O que você quer maximizar ou minimizar? Em que unidade (R$, tempo, …)?
- Horizonte de análise? Há valor do dinheiro no tempo (taxa)?
- Qual restrição é inegociável (orçamento, prazo, risco máximo)?

**C. Os números conhecidos (constantes)**
- Valores fixos e certos (preço, salário, mensalidade…).

**D. As incertezas (uma a uma)**
Para cada coisa que o usuário "acha" mas não sabe:
- Pior caso plausível? Caso mais provável? Melhor caso plausível?
- Tem dado/histórico ou é estimativa? Qual a fonte?
- (Eventos sim/não) Qual a chance de ocorrer? Com que confiança?

**E. Risco**
- Prefere o de maior média mesmo com chance de perda grande, ou o mais
  seguro com média menor? (calibra neutralidade vs. aversão a risco)
- Qual perda seria inaceitável (ruína)?

Falta dado obrigatório → **pergunte; não preencha por conta própria**.
Dado opcional ausente → assuma explicitamente e marque como premissa.

## Boas práticas de elicitação

- Peça **3 pontos** (mín/moda/máx), não um número só — captura a incerteza.
- Ancore em dado externo antes de pedir o palpite (reduz viés de ancoragem).
- Pergunte intervalos com "90% de confiança" e teste com "apostaria nisso?".
- Decomponha estimativas grandes em partes menores (mais fácil estimar bem).

## Vieses a caçar (no usuário e na própria análise)

- **Custo afundado:** dinheiro/tempo já gasto não deve influenciar a escolha
  futura. Modele só fluxos futuros.
- **Ancoragem:** o primeiro número dito contamina os demais.
- **Excesso de confiança:** faixas estreitas demais → subestima incerteza.
  Alargue intervalos elicitados.
- **Aversão à perda / status quo:** manter o atual parece mais seguro do que
  é. Trate o status quo como uma alternativa avaliada pelas mesmas regras.
- **Enquadramento:** "90% de chance de dar certo" vs. "10% de falhar" mudam a
  escolha — apresente nos dois sentidos.
- **Confirmação:** modelar só os cenários que favorecem a opção desejada.
- **Negligência da taxa-base:** ignorar a frequência geral do evento.
- **Falácia de regressão:** atribuir a uma ação uma melhora que era só
  retorno à média.

## Padrões inegociáveis

- Nenhum número crítico inventado: ou tem fonte, ou é premissa declarada, ou
  vira pergunta ao usuário.
- O objetivo certo é validado antes de otimizar (otimizar a métrica errada é
  pior que não otimizar).
- Toda recomendação final explicita: premissas, o que a viraria, e o nível
  de confiança.
