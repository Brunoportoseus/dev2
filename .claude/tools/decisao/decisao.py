#!/usr/bin/env python3
"""
Motor de Análise de Decisão — genérico para QUALQUER problema/decisão.

Transforma uma decisão descrita num arquivo de modelo (YAML ou JSON) em:
  - Valor esperado de cada alternativa (rollback de árvore de decisão / EMV)
  - Simulação de Monte Carlo sob incerteza (distribuições de probabilidade)
  - Probabilidade de cada alternativa ser a melhor decisão
  - Probabilidade de "bom negócio" por alternativa
  - Métricas de risco (downside, percentis)
  - Sensibilidade (tornado) — quais incertezas mais movem a decisão

Sem dependências obrigatórias além da stdlib. YAML é usado se o pacote
`yaml` estiver disponível; caso contrário use entrada JSON.

Uso:
    python3 decisao.py modelo.yaml
    python3 decisao.py modelo.json --json saida.json
    python3 decisao.py --help

O esquema do arquivo de entrada está documentado em
.claude/knowledge/decisao/formato-entrada.md
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import random
import statistics
import sys
from typing import Any


# --------------------------------------------------------------------------- #
# Avaliador de expressão seguro (sem eval()): só aritmética + nomes + funções  #
# --------------------------------------------------------------------------- #

_ALLOWED_FUNCS = {
    "min": min, "max": max, "abs": abs, "round": round,
    "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
    "floor": math.floor, "ceil": math.ceil,
}


def safe_eval(expr: str, variables: dict[str, float]) -> float:
    """Avalia uma expressão aritmética restrita. Sem builtins, sem atributos."""
    node = ast.parse(str(expr), mode="eval").body

    def ev(n: ast.AST) -> Any:
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError(f"constante não numérica: {n.value!r}")
        if isinstance(n, ast.Name):
            if n.id in variables:
                return variables[n.id]
            raise ValueError(f"variável não definida na fórmula: '{n.id}'")
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            op = n.op
            if isinstance(op, ast.Add):
                return a + b
            if isinstance(op, ast.Sub):
                return a - b
            if isinstance(op, ast.Mult):
                return a * b
            if isinstance(op, ast.Div):
                return a / b
            if isinstance(op, ast.Pow):
                return a ** b
            if isinstance(op, ast.Mod):
                return a % b
            raise ValueError(f"operador não permitido: {op}")
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            if isinstance(n.op, ast.UAdd):
                return +v
            if isinstance(n.op, ast.USub):
                return -v
            raise ValueError("operador unário não permitido")
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.func.id not in _ALLOWED_FUNCS:
                raise ValueError("função não permitida na fórmula")
            return _ALLOWED_FUNCS[n.func.id](*[ev(a) for a in n.args])
        if isinstance(n, ast.IfExp):  # a if cond else b
            return ev(n.body) if ev(n.test) else ev(n.orelse)
        if isinstance(n, ast.Compare):
            left = ev(n.left)
            for op, comp in zip(n.ops, n.comparators):
                right = ev(comp)
                ok = (
                    (isinstance(op, ast.Lt) and left < right)
                    or (isinstance(op, ast.LtE) and left <= right)
                    or (isinstance(op, ast.Gt) and left > right)
                    or (isinstance(op, ast.GtE) and left >= right)
                    or (isinstance(op, ast.Eq) and left == right)
                    or (isinstance(op, ast.NotEq) and left != right)
                )
                if not ok:
                    return False
                left = right
            return True
        raise ValueError(f"expressão não permitida: {type(n).__name__}")

    return float(ev(node))


# --------------------------------------------------------------------------- #
# Amostragem de distribuições de probabilidade                                 #
# --------------------------------------------------------------------------- #

def _pert(rng: random.Random, lo: float, mode: float, hi: float, lamb: float = 4.0) -> float:
    """PERT (beta reescalada) — padrão em análise de decisão para 3 estimativas."""
    if hi <= lo:
        return lo
    alpha = 1 + lamb * (mode - lo) / (hi - lo)
    beta = 1 + lamb * (hi - mode) / (hi - lo)
    return lo + rng.betavariate(alpha, beta) * (hi - lo)


def sample(rng: random.Random, spec: Any) -> float:
    """Amostra um valor de uma especificação de distribuição (ou constante)."""
    if isinstance(spec, (int, float)):
        return float(spec)
    if not isinstance(spec, dict) or "dist" not in spec:
        raise ValueError(f"distribuição inválida: {spec!r}")
    d = str(spec["dist"]).lower()
    if d in ("const", "constante", "constant"):
        return float(spec["valor"])
    if d in ("uniforme", "uniform"):
        return rng.uniform(float(spec["min"]), float(spec["max"]))
    if d in ("triangular", "triang"):
        return rng.triangular(float(spec["min"]), float(spec["max"]), float(spec["moda"]))
    if d == "pert":
        return _pert(rng, float(spec["min"]), float(spec["moda"]), float(spec["max"]),
                     float(spec.get("lambda", 4.0)))
    if d in ("normal", "gauss"):
        return rng.gauss(float(spec["media"]), float(spec["desvio"]))
    if d in ("lognormal", "lognorm"):
        return rng.lognormvariate(float(spec["media_log"]), float(spec["desvio_log"]))
    if d in ("bernoulli", "binaria"):
        return 1.0 if rng.random() < float(spec["p"]) else 0.0
    if d in ("discreta", "discrete"):
        valores = spec["valores"]
        probs = spec["probs"]
        return float(rng.choices(valores, weights=probs, k=1)[0])
    if d in ("beta",):
        return rng.betavariate(float(spec["alpha"]), float(spec["beta"]))
    raise ValueError(f"distribuição desconhecida: '{d}'")


def mean_of(spec: Any) -> float:
    """Valor 'central' determinístico de uma distribuição (para rollback EMV)."""
    if isinstance(spec, (int, float)):
        return float(spec)
    d = str(spec["dist"]).lower()
    if d in ("const", "constante", "constant"):
        return float(spec["valor"])
    if d in ("uniforme", "uniform"):
        return (float(spec["min"]) + float(spec["max"])) / 2
    if d in ("triangular", "triang"):
        return (float(spec["min"]) + float(spec["moda"]) + float(spec["max"])) / 3
    if d == "pert":
        return (float(spec["min"]) + 4 * float(spec["moda"]) + float(spec["max"])) / 6
    if d in ("normal", "gauss"):
        return float(spec["media"])
    if d in ("lognormal", "lognorm"):
        return math.exp(float(spec["media_log"]) + float(spec["desvio_log"]) ** 2 / 2)
    if d in ("bernoulli", "binaria"):
        return float(spec["p"])
    if d in ("discreta", "discrete"):
        return sum(v * p for v, p in zip(spec["valores"], spec["probs"])) / sum(spec["probs"])
    if d in ("beta",):
        a, b = float(spec["alpha"]), float(spec["beta"])
        return a / (a + b)
    raise ValueError(f"distribuição desconhecida: '{d}'")


# --------------------------------------------------------------------------- #
# Avaliação do payoff de uma alternativa: fórmula OU árvore de decisão         #
# --------------------------------------------------------------------------- #

def eval_tree(node: dict, env: dict[str, float]) -> float:
    """Rollback de árvore. Nó 'chance' = média ponderada pelas probabilidades."""
    tipo = node.get("tipo", "folha")
    if tipo in ("folha", "leaf"):
        if "valor" in node:
            return float(node["valor"])
        return safe_eval(node["formula"], env)
    if tipo in ("chance", "acaso"):
        ramos = node["ramos"]
        probs: list[float | None] = []
        for ramo in ramos:
            if ramo.get("p_resto"):
                probs.append(None)  # absorve a probabilidade restante
            elif "p" in ramo:
                probs.append(float(ramo["p"]))
            elif "p_var" in ramo:
                probs.append(float(env[ramo["p_var"]]))
            else:
                raise ValueError("ramo de chance precisa de 'p', 'p_var' ou 'p_resto'")
        fixos = sum(p for p in probs if p is not None)
        n_resto = sum(1 for p in probs if p is None)
        if n_resto:
            resto = max(0.0, 1.0 - fixos)
            probs = [resto / n_resto if p is None else p for p in probs]
        soma_p = sum(probs)
        if abs(soma_p - 1.0) > 1e-6:
            raise ValueError(f"probabilidades de um nó de chance somam {soma_p:.4f}, não 1")
        return sum(p * eval_tree(r, env) for p, r in zip(probs, ramos))
    if tipo in ("decisao", "decision"):
        # subdecisão: escolhe o melhor ramo conforme 'sentido' do env
        vals = [eval_tree(r, env) for r in node["ramos"]]
        return max(vals) if env.get("_sentido_max", 1.0) >= 0.5 else min(vals)
    raise ValueError(f"tipo de nó desconhecido: '{tipo}'")


def payoff(alt: dict, env: dict[str, float], sentido_max: bool) -> float:
    base = dict(env)
    base["_sentido_max"] = 1.0 if sentido_max else 0.0
    for k, v in alt.get("constantes", {}).items():
        base[k] = float(v)
    if "arvore" in alt:
        node = alt["arvore"]
        if isinstance(node, list):
            node = {"tipo": "chance", "ramos": node}
        return eval_tree(node, base)
    if "formula" in alt:
        return safe_eval(alt["formula"], base)
    raise ValueError(f"alternativa '{alt.get('nome')}' precisa de 'formula' ou 'arvore'")


# --------------------------------------------------------------------------- #
# Núcleo: rollback determinístico + Monte Carlo                                #
# --------------------------------------------------------------------------- #

def percentil(dados: list[float], q: float) -> float:
    s = sorted(dados)
    if not s:
        return float("nan")
    idx = q * (len(s) - 1)
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return s[int(idx)]
    return s[lo] + (s[hi] - s[lo]) * (idx - lo)


def analisar(modelo: dict) -> dict:
    sentido = str(modelo.get("sentido", "max")).lower()
    sentido_max = sentido in ("max", "maximizar", "maximize")
    params: dict[str, Any] = modelo.get("parametros", {})
    alternativas: list[dict] = modelo["alternativas"]
    n_iter = int(modelo.get("iteracoes", 50000))
    seed = modelo.get("seed", 42)
    limiar = modelo.get("limiar_bom_negocio", None)

    # 1) Rollback determinístico (parâmetros no valor central) -> EMV
    env_central = {k: mean_of(v) for k, v in params.items()}
    emv = {}
    for alt in alternativas:
        emv[alt["nome"]] = payoff(alt, env_central, sentido_max)

    # 2) Monte Carlo
    rng = random.Random(seed)
    dist: dict[str, list[float]] = {a["nome"]: [] for a in alternativas}
    vence: dict[str, int] = {a["nome"]: 0 for a in alternativas}
    for _ in range(n_iter):
        env = {k: sample(rng, v) for k, v in params.items()}
        vals = {}
        for alt in alternativas:
            try:
                vals[alt["nome"]] = payoff(alt, env, sentido_max)
            except Exception as e:  # noqa: BLE001
                raise SystemExit(f"Erro ao avaliar '{alt['nome']}': {e}")
        for nome, v in vals.items():
            dist[nome].append(v)
        melhor = max(vals, key=vals.get) if sentido_max else min(vals, key=vals.get)
        vence[melhor] += 1

    resultado = {
        "objetivo": modelo.get("objetivo", ""),
        "sentido": "maximizar" if sentido_max else "minimizar",
        "iteracoes": n_iter,
        "moeda": modelo.get("moeda", ""),
        "alternativas": [],
    }
    for alt in alternativas:
        nome = alt["nome"]
        d = dist[nome]
        media = statistics.fmean(d)
        registro = {
            "nome": nome,
            "emv_rollback": emv[nome],
            "media_mc": media,
            "desvio": statistics.pstdev(d) if len(d) > 1 else 0.0,
            "p5": percentil(d, 0.05),
            "p50": percentil(d, 0.50),
            "p95": percentil(d, 0.95),
            "prob_melhor": vence[nome] / n_iter,
        }
        if limiar is not None:
            lim = float(limiar)
            bons = sum(1 for x in d if (x >= lim if sentido_max else x <= lim))
            registro["prob_bom_negocio"] = bons / n_iter
            registro["limiar_bom_negocio"] = lim
        resultado["alternativas"].append(registro)

    melhor_media = (max if sentido_max else min)(
        resultado["alternativas"], key=lambda r: r["media_mc"]
    )
    resultado["recomendacao"] = melhor_media["nome"]

    # 3) Sensibilidade (tornado) sobre o que VIRA a decisão:
    #    diferença entre a alternativa recomendada e a melhor concorrente.
    ordenadas = sorted(
        alternativas,
        key=lambda a: emv[a["nome"]],
        reverse=sentido_max,
    )
    alt_rec = ordenadas[0]
    alt_concorrente = ordenadas[1] if len(ordenadas) > 1 else ordenadas[0]

    def vantagem(env: dict[str, float]) -> float:
        # >0 = recomendada continua vencendo; <0 = decisão vira.
        p_rec = payoff(alt_rec, env, sentido_max)
        p_con = payoff(alt_concorrente, env, sentido_max)
        return (p_rec - p_con) if sentido_max else (p_con - p_rec)

    tornado = []
    rng2 = random.Random(seed + 1)
    base_adv = vantagem(env_central)
    for pname, pspec in params.items():
        amostras = sorted(sample(rng2, pspec) for _ in range(2000))
        baixo = amostras[int(0.10 * len(amostras))]
        alto = amostras[int(0.90 * len(amostras))]
        e_lo = dict(env_central); e_lo[pname] = baixo
        e_hi = dict(env_central); e_hi[pname] = alto
        a_lo = vantagem(e_lo)
        a_hi = vantagem(e_hi)
        tornado.append({
            "parametro": pname,
            "swing": abs(a_hi - a_lo),
            "valor_p10": baixo, "valor_p90": alto,
            "vantagem_p10": a_lo, "vantagem_p90": a_hi,
            "pode_virar": (a_lo < 0) or (a_hi < 0),
        })
    tornado.sort(key=lambda t: t["swing"], reverse=True)
    resultado["sensibilidade"] = tornado
    resultado["comparacao"] = {
        "recomendada": alt_rec["nome"],
        "concorrente": alt_concorrente["nome"],
        "vantagem_central": base_adv,
    }
    return resultado


# --------------------------------------------------------------------------- #
# Relatório legível                                                            #
# --------------------------------------------------------------------------- #

def fmt(v: float, moeda: str) -> str:
    return f"{moeda} {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def relatorio(modelo: dict, r: dict) -> str:
    moeda = r.get("moeda", "")
    L = []
    L.append("=" * 70)
    L.append("ANÁLISE DE DECISÃO")
    L.append("=" * 70)
    if modelo.get("problema"):
        L.append(f"Problema : {modelo['problema']}")
    L.append(f"Objetivo : {r['objetivo']} ({r['sentido']})")
    L.append(f"Monte Carlo: {r['iteracoes']:,} iterações".replace(",", "."))
    L.append("")
    L.append("-" * 70)
    L.append("ALTERNATIVAS")
    L.append("-" * 70)
    for a in r["alternativas"]:
        L.append(f"\n• {a['nome']}")
        L.append(f"    Valor esperado (rollback EMV) : {fmt(a['emv_rollback'], moeda)}")
        L.append(f"    Média Monte Carlo             : {fmt(a['media_mc'], moeda)}")
        L.append(f"    Intervalo p5–p95              : {fmt(a['p5'], moeda)}  …  {fmt(a['p95'], moeda)}")
        L.append(f"    P(ser a MELHOR decisão)       : {a['prob_melhor']*100:5.1f}%")
        if "prob_bom_negocio" in a:
            L.append(f"    P(bom negócio | limiar {fmt(a['limiar_bom_negocio'], moeda)}) : {a['prob_bom_negocio']*100:5.1f}%")
    L.append("")
    L.append("-" * 70)
    L.append(f"RECOMENDAÇÃO: {r['recomendacao']}")
    L.append("-" * 70)
    melhor = max(r["alternativas"], key=lambda x: x["prob_melhor"])
    L.append(f"Maior probabilidade de ser a melhor decisão: "
             f"{melhor['nome']} ({melhor['prob_melhor']*100:.1f}%).")
    L.append("")
    L.append("-" * 70)
    L.append("SENSIBILIDADE — o que mais move a decisão (tornado)")
    L.append("-" * 70)
    cmp = r.get("comparacao", {})
    if cmp:
        L.append(f"Vantagem de '{cmp['recomendada']}' sobre '{cmp['concorrente']}': "
                 f"{fmt(cmp['vantagem_central'], moeda)} (no cenário central).")
        L.append("Um parâmetro 'pode virar' a decisão se, no p10 ou p90, a "
                 "vantagem fica negativa.")
        L.append("")
    for t in r["sensibilidade"][:8]:
        flag = "  <-- PODE VIRAR A DECISÃO" if t.get("pode_virar") else ""
        L.append(f"  {t['parametro']:<26} swing {fmt(t['swing'], moeda)}{flag}")
    L.append("=" * 70)
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def carregar(caminho: str) -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read()
    if caminho.endswith((".yaml", ".yml")):
        try:
            import yaml  # type: ignore
        except ImportError:
            raise SystemExit("pyyaml ausente: converta o modelo para .json")
        return yaml.safe_load(texto)
    return json.loads(texto)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Motor genérico de análise de decisão (árvore + Monte Carlo)."
    )
    ap.add_argument("modelo", help="arquivo do modelo (.yaml ou .json)")
    ap.add_argument("--json", dest="json_out", metavar="ARQ",
                    help="grava o resultado completo em JSON")
    args = ap.parse_args(argv)

    modelo = carregar(args.modelo)
    if not modelo or "alternativas" not in modelo:
        raise SystemExit("modelo inválido: faltam 'alternativas'")
    r = analisar(modelo)
    print(relatorio(modelo, r))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)
        print(f"\n[JSON salvo em {args.json_out}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
