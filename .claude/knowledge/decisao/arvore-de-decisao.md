# Árvore de Decisão — valor esperado e rollback

> Estrutura para decisões com eventos incertos encadeados. Base do que a
> ferramenta calcula.

## Elementos

- **Nó de decisão (□):** o decisor escolhe um ramo. Escolhe-se o de melhor
  valor esperado.
- **Nó de chance (○):** a natureza decide; cada ramo tem uma probabilidade.
  As probabilidades de um nó somam 1.
- **Folha:** o payoff final daquele caminho (valor ou fórmula).

## Rollback (avaliação)

Calcule da direita (folhas) para a esquerda:

- Em um **nó de chance**: valor = Σ (probabilidade do ramo × valor do ramo).
  Isso é o **EMV** (valor monetário esperado) daquele nó.
- Em um **nó de decisão**: valor = melhor (máx se maximiza; mín se minimiza)
  entre os ramos. O ramo escolhido é a decisão recomendada.

A alternativa com melhor EMV é a recomendação **sob neutralidade ao risco**.

## Além do EMV

- **EMV ignora risco.** Duas alternativas com mesmo EMV mas dispersões
  diferentes não são equivalentes para uma pessoa avessa a risco. Use a
  simulação (distribuição completa, p5–p95, P(prejuízo)) e, se necessário,
  **utilidade** (ex.: log da riqueza) em vez do valor bruto.
- **Valor da informação:**
  - **EVPI** (informação perfeita) = EMV com informação perfeita − EMV sem
    informação. É o teto do que vale pagar para reduzir a incerteza.
  - **EVSI** (informação amostral/imperfeita) = ganho esperado de um teste/
    pesquisa antes de decidir. Compare com o custo do teste.
- **Opção de adiar:** "decidir depois" é uma alternativa legítima — modele-a
  como um ramo (esperar e então escolher com mais informação).

## Boas práticas

- Toda probabilidade tem fonte declarada (dado, base rate, especialista).
- Probabilidades de um nó de chance somam exatamente 1 (use o "ramo resto"
  para o complemento).
- Não confunda nó de decisão (controlável) com nó de chance (incerto).
- Sempre reporte, além do EMV, a **distribuição** e a **probabilidade de cada
  alternativa ser a melhor** — é isso que o decisor pede.
- Faça **rollback determinístico** (valores centrais) E **Monte Carlo**
  (incerteza nos parâmetros): o primeiro explica, o segundo dá a probabilidade.
