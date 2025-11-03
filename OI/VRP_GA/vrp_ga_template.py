
"""
VRP con Algoritmo Genético (GA): plantilla lista para adaptar
-------------------------------------------------------------
- Cromosoma: permutación de clientes (1..N)
- Decodificador: construye rutas secuenciales respetando capacidad Q y máx. K vehículos.
- Objetivo: distancia total (euclidiana) incluyendo ida/vuelta al depósito.
- Penalización: si #rutas > K, añade una penalización grande.
- Selección: torneo o ruleta (a elección).
- Cruza: OX (Order Crossover) por defecto.
- Mutación: swap de dos posiciones.
- Métrica de diversidad: entropía media por posición.

Cómo usar:
1) Ajusta rutas de archivo en `load_problem(...)` si necesitas.
2) Ajusta parámetros en `GAConfig` o pásalos a `run_ga(...)`.
3) Ejecuta `python vrp_ga_template.py` para correr una configuración.
4) Para comparar grids de parámetros, usa `grid_search(...)`.

Autor: Plantilla generada para el caso de 24 clientes, 4 vehículos, Q=30.
"""
from __future__ import annotations
import json, math, random, argparse
from dataclasses import dataclass
from typing import List, Tuple, Dict
import pandas as pd

# ---------------------------- Utilidades problema ----------------------------

@dataclass
class VRPInstance:
    depot: Tuple[float, float]
    coords: Dict[int, Tuple[float, float]]
    demand: Dict[int, int]
    K: int      # número de vehículos
    Q: int      # capacidad por vehículo

def euclidean(a: Tuple[float,float], b: Tuple[float,float]) -> float:
    dx, dy = a[0]-b[0], a[1]-b[1]
    return (dx*dx + dy*dy) ** 0.5

def load_problem(csv_path: str, meta_json_path: str) -> VRPInstance:
    df = pd.read_csv(csv_path)
    with open(meta_json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    coords = {int(row["cliente_id"]): (float(row["x"]), float(row["y"])) for _, row in df.iterrows()}
    demand = {int(row["cliente_id"]): int(row["demanda"]) for _, row in df.iterrows()}
    depot = (float(meta["depot"]["x"]), float(meta["depot"]["y"]))
    return VRPInstance(depot=depot, coords=coords, demand=demand, K=int(meta["K"]), Q=int(meta["Q"]))

# ---------------------------- Decodificador & costo --------------------------

@dataclass
class DecodeResult:
    routes: List[List[int]]
    cost: float
    extra_routes: int

def decode_and_cost(instance: VRPInstance, perm: List[int]) -> DecodeResult:
    """Construye rutas por capacidad y calcula distancia total (ida/vuelta)."""
    routes, current, load = [], [], 0
    for cid in perm:
        d = instance.demand[cid]
        if load + d <= instance.Q:
            current.append(cid)
            load += d
        else:
            if current:
                routes.append(current)
            current = [cid]
            load = d
    if current:
        routes.append(current)

    # Coste total con depósito al inicio y fin de cada ruta
    total = 0.0
    for r in routes:
        prev = instance.depot
        for cid in r:
            total += euclidean(prev, instance.coords[cid])
            prev = instance.coords[cid]
        total += euclidean(prev, instance.depot)

    extra = max(0, len(routes) - instance.K)
    return DecodeResult(routes=routes, cost=total, extra_routes=extra)

# ------------------------------ GA: operadores --------------------------------

def order_crossover(p1: List[int], p2: List[int], rng: random.Random) -> List[int]:
    """OX: copia segmento de p1 y rellena con el orden relativo de p2."""
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    child = [None] * n
    child[a:b+1] = p1[a:b+1]
    fill = [g for g in p2 if g not in child]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[j]
            j += 1
    return child

def mutate_swap(perm: List[int], rng: random.Random) -> None:
    i, j = rng.sample(range(len(perm)), 2)
    perm[i], perm[j] = perm[j], perm[i]

def roulette_selection(pop_costs: List[float], rng: random.Random) -> int:
    """Minimización -> fitness = 1/(1+cost)."""
    fitness = [1.0/(1.0+c) for c in pop_costs]
    s = sum(fitness)
    r = rng.uniform(0, s)
    acc = 0.0
    for idx, f in enumerate(fitness):
        acc += f
        if acc >= r:
            return idx
    return len(pop_costs)-1

def tournament_selection(pop_costs: List[float], rng: random.Random, t: int=3) -> int:
    cand = rng.sample(range(len(pop_costs)), t)
    cand.sort(key=lambda i: pop_costs[i])
    return cand[0]

# -------------------------- GA: configuración & bucle -------------------------

@dataclass
class GAConfig:
    pop_size: int = 80
    pc: float = 0.9
    pm: float = 0.1
    elitism: int = 2
    selection: str = "tournament"  # "tournament" o "roulette"
    penalty: float = 10000.0       # penalización por ruta extra
    generations: int = 400
    seed: int = 42

@dataclass
class GAStats:
    best_per_gen: List[float]
    avg_per_gen: List[float]
    diversity_per_gen: List[float]

def diversity_entropy(pop: List[List[int]]) -> float:
    """Entropía media por posición (aprox de diversidad)."""
    import math
    n = len(pop[0])
    m = len(pop)
    h_pos = []
    for pos in range(n):
        counts = {}
        for chrom in pop:
            g = chrom[pos]
            counts[g] = counts.get(g, 0) + 1
        H = 0.0
        for cnt in counts.values():
            p = cnt / m
            H -= p * math.log(p + 1e-12)
        # normaliza por log(n) aprox
        H_norm = H / math.log(n + 1e-12)
        h_pos.append(H_norm)
    return float(sum(h_pos)/len(h_pos))

def run_ga(instance: VRPInstance, cfg: GAConfig) -> Tuple[List[int], DecodeResult, GAStats]:
    rng = random.Random(cfg.seed)
    customers = list(instance.coords.keys())
    n = len(customers)

    # Población inicial: permutaciones aleatorias
    population = []
    for _ in range(cfg.pop_size):
        perm = customers[:]
        rng.shuffle(perm)
        population.append(perm)

    best_per_gen, avg_per_gen, div_per_gen = [], [], []

    def cost_of(perm: List[int]) -> float:
        res = decode_and_cost(instance, perm)
        return res.cost + cfg.penalty * res.extra_routes

    # Evaluación inicial
    costs = [cost_of(ind) for ind in population]

    for _gen in range(cfg.generations):
        # Estadísticas
        best_per_gen.append(min(costs))
        avg_per_gen.append(sum(costs)/len(costs))
        div_per_gen.append(diversity_entropy(population))

        # Elitismo
        elite_idx = sorted(range(len(population)), key=lambda i: costs[i])[:cfg.elitism]
        elites = [population[i][:] for i in elite_idx]

        # Nueva población
        new_pop = elites[:]
        while len(new_pop) < cfg.pop_size:
            # Selección de padres
            if cfg.selection == "roulette":
                i1 = roulette_selection(costs, rng)
                i2 = roulette_selection(costs, rng)
            else:
                i1 = tournament_selection(costs, rng)
                i2 = tournament_selection(costs, rng)

            p1, p2 = population[i1], population[i2]

            # Cruza
            if rng.random() < cfg.pc:
                c = order_crossover(p1, p2, rng)
            else:
                c = p1[:]

            # Mutación
            if rng.random() < cfg.pm:
                mutate_swap(c, rng)

            new_pop.append(c)

        population = new_pop[:cfg.pop_size]
        costs = [cost_of(ind) for ind in population]

    # Final
    best_idx = min(range(len(population)), key=lambda i: costs[i])
    best_perm = population[best_idx][:]
    best_dec = decode_and_cost(instance, best_perm)
    stats = GAStats(best_per_gen, avg_per_gen, div_per_gen)
    return best_perm, best_dec, stats

# ------------------------------ Grid de parámetros ----------------------------

def grid_search(instance: VRPInstance):
    N_opts = [30, 80, 150]
    pc_opts = [0.6, 0.9]
    pm_opts = [0.02, 0.1, 0.2]
    e_opts  = [0, 2, 5]
    sel_opts = ["tournament", "roulette"]

    results = []
    gid = 0
    for N in N_opts:
        for pc in pc_opts:
            for pm in pm_opts:
                for e in e_opts:
                    for sel in sel_opts:
                        gid += 1
                        cfg = GAConfig(pop_size=N, pc=pc, pm=pm, elitism=e, selection=sel, generations=300, seed=42)
                        best_perm, best_dec, stats = run_ga(instance, cfg)
                        results.append({
                            "grid_id": gid,
                            "pop_size": N, "pc": pc, "pm": pm, "elitism": e, "selection": sel,
                            "best_cost": best_dec.cost, "extra_routes": best_dec.extra_routes,
                            "penalized": best_dec.cost + cfg.penalty*best_dec.extra_routes,
                            "routes": len(best_dec.routes)
                        })
                        print(f"[{gid}] N={N} pc={pc} pm={pm} e={e} sel={sel} -> cost={best_dec.cost:.2f}, routes={len(best_dec.routes)}, extra={best_dec.extra_routes}")
    return pd.DataFrame(results)

# ------------------------------ CLI sencillo ----------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="/mnt/data/vrp_agricola_24clientes_4vehiculos.csv")
    parser.add_argument("--meta", default="/mnt/data/vrp_agricola_metadata.json")
    parser.add_argument("--grid", action="store_true", help="Ejecutar búsqueda de hiperparámetros.")
    parser.add_argument("--gens", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    inst = load_problem(args.csv, args.meta)
    cfg = GAConfig(generations=args.gens, seed=args.seed)
    if args.grid:
        df = grid_search(inst)
        out = "/mnt/data/vrp_ga_grid_results.csv"
        df.to_csv(out, index=False)
        print(f"Grid guardado en: {out}")
    else:
        best_perm, best_dec, stats = run_ga(inst, cfg)
        print("Mejor penalizado:", best_dec.cost + cfg.penalty*best_dec.extra_routes)
        print("Rutas:", best_dec.routes)
        print("Distancia sin penalización:", best_dec.cost)
        print("Extra rutas:", best_dec.extra_routes)

if __name__ == "__main__":
    main()
