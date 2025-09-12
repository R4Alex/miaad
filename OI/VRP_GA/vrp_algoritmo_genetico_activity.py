import json
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

# ------------------------------------------------------------
# 1) Datos
# ------------------------------------------------------------
# Lee depósito
with open("vrp_agricola_metadata.json", "r") as file:
    meta = json.load(file)
depot_xy = (float(meta["depot"]["x"]), float(meta["depot"]["y"]))

# Lee clientes
df = pd.read_csv("vrp_agricola_24clientes_4vehiculos.csv")
# Asegura orden por cliente_id y tipos numéricos
df = df.sort_values("cliente_id").reset_index(drop=True)
df["cliente_id"] = df["cliente_id"].astype(int)

# Construye listas/arrays alineados por índice:
#   índice 0 = Depot, índices 1..n = clientes en orden de df
names = ["Depot"] + [str(c) for c in df["cliente_id"].tolist()]
coords = np.vstack([
    np.array(depot_xy, dtype=float),
    df[["x", "y"]].to_numpy(dtype=float)
])
demands = np.zeros(len(names), dtype=float)
demands[1:] = df["demanda"].to_numpy(dtype=float)

num_locations = len(names)             # Depot + clientes
num_clients = num_locations - 1        # Solo clientes (sin depot)
CLIENT_INDICES = list(range(1, num_locations))  # 1..n (para cromosoma)

# ------------------------------------------------------------
# 2) Utilidades: distancia y matriz
# ------------------------------------------------------------
def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

distance_matrix = np.zeros((num_locations, num_locations), dtype=float)
for i in range(num_locations):
    for j in range(num_locations):
        distance_matrix[i, j] = euclidean(coords[i], coords[j])

# ------------------------------------------------------------
# 3) Decodificador: permutación -> rutas factibles (capacidad)
# ------------------------------------------------------------
def decode_routes(permutation, capacity, demands_array):
    """
    permutation: lista de índices (1..n) SIN 0 (depot)
    capacity:    capacidad máxima por vehículo (p.ej., 30)
    demands_array: demands[i] = demanda del nodo i (0=depot)
    return: lista de rutas, cada ruta es lista de índices de clientes (sin 0)
    """
    routes = []
    current = []
    load = 0.0

    for client in permutation:
        d = demands_array[client]
        if load + d > capacity:
            if current:
                routes.append(current)
            current = [client]
            load = d
        else:
            current.append(client)
            load += d

    if current:
        routes.append(current)
    return routes

# ------------------------------------------------------------
# 4) Distancia total de un conjunto de rutas (con viajes al depot)
# ------------------------------------------------------------
def routes_total_distance(routes, dist_mtx):
    total = 0.0
    for r in routes:
        # depot -> primer cliente
        total += dist_mtx[0, r[0]]
        # tramos internos
        for i in range(len(r) - 1):
            total += dist_mtx[r[i], r[i+1]]
        # último cliente -> depot
        total += dist_mtx[r[-1], 0]
    return total

# ------------------------------------------------------------
# 5) Fitness = distancia + penalización por exceder #rutas
# ------------------------------------------------------------
def fitness(permutation,
            capacity,
            demands_array,
            dist_mtx,
            max_routes=4,
            alpha=None):
    routes = decode_routes(permutation, capacity, demands_array)
    dist = routes_total_distance(routes, dist_mtx)

    # Penalización si excede número máximo de vehículos
    excess = max(0, len(routes) - max_routes)

    # Si no te dan un alpha, calcula uno razonable (ajústalo si gustas):
    # idea: un múltiplo de la distancia media depot->cliente por #clientes
    if alpha is None:
        mean_dep = float(np.mean(dist_mtx[0, 1:]))
        alpha = 5.0 * mean_dep * num_clients  # bastante grande para "doler"

    return dist + alpha * excess

# ------------------------------------------------------------
# 6) GA: población inicial, selección, cruza, mutación
# ------------------------------------------------------------
def initial_population(size):
    return [random.sample(CLIENT_INDICES, len(CLIENT_INDICES)) for _ in range(size)]

def tournament_selection(population, fitness_values, k=3):
    selected = []
    zipped = list(zip(population, fitness_values))
    for _ in range(len(population)):
        aspirants = random.sample(zipped, k)
        winner = min(aspirants, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected

def roulette_selection(population, fitness_values):
    # Como fitness es distancia (minimizar), invertimos para tener mayores=mejor
    inv_fit = np.max(fitness_values) - np.array(fitness_values) + 1e-6
    probs = inv_fit / np.sum(inv_fit)
    selected = random.choices(population, weights=probs, k=len(population))
    return selected

def crossover(parent1, parent2):
    """
    OX simple (Order Crossover-like)
    """
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[a:b+1] = parent1[a:b+1]
    ptr = 0
    for i in range(size):
        if parent2[i] not in child:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = parent2[i]
    return child

def crossover_population(parents, probability_crossover):
    offspring = []
    for i in range(0, len(parents) - 1, 2):
        p1, p2 = parents[i], parents[i+1]
        if random.random() < probability_crossover:
            # Sí se cruzan
            c1 = crossover(p1, p2)
            c2 = crossover(p2, p1)
        else:
            # No se cruzan, se copian tal cual
            c1, c2 = p1[:], p2[:]
        offspring.extend([c1, c2])
    if len(parents) % 2 == 1:
        offspring.append(parents[-1][:])
    return offspring

def mutate(individual, rate=0.1):
    """
    Swap aleatorio
    """
    if random.random() < rate:
        a, b = random.sample(range(len(individual)), 2)
        individual[a], individual[b] = individual[b], individual[a]
    return individual

def mutate_population(population, rate=0.1):
    return [mutate(ind.copy(), rate) for ind in population]

# ------------------------------------------------------------
# 7) Ejecutar GA
# ------------------------------------------------------------
random.seed(42)
np.random.seed(42)

CAPACITY = 30
MAX_ROUTES = 4
ALPHA = 10000

# population_size = 80
population_size = 30
# generations = 200
generations = 1000
mutation_rate = 0.1
tournament_k = 3
probability_crossover =  0.9

population = initial_population(population_size)
best_history = []
avg_history = []

elitism = 5

for g in range(generations):
    fitness_values = [fitness(ind,
                              capacity=CAPACITY,
                              demands_array=demands,
                              dist_mtx=distance_matrix,
                              max_routes=MAX_ROUTES,
                              alpha=ALPHA)
                      for ind in population]

    best = min(fitness_values)
    avg = float(np.mean(fitness_values))
    best_history.append(best)
    avg_history.append(avg)

    # Selección → Cruza → Mutación
    # selected = tournament_selection(population, fitness_values, k=tournament_k)
    selected = roulette_selection(population, fitness_values)
    offspring = crossover_population(selected, probability_crossover)
    offspring = mutate_population(offspring, rate=mutation_rate)

    # ---- ELITISMO ----
    if elitism > 0:
        # Ordena población actual por fitness
        elite_idx = np.argsort(fitness_values)[:elitism]
        elites = [population[i][:] for i in elite_idx]
        # Reemplaza parte de la descendencia con los elites
        offspring[:elitism] = elites

    # Nueva población
    population = offspring

# ------------------------------------------------------------
# 8) Resultados: mejor solución, rutas y gráficas
# ------------------------------------------------------------
fitness_values = [fitness(ind,
                          capacity=CAPACITY,
                          demands_array=demands,
                          dist_mtx=distance_matrix,
                          max_routes=MAX_ROUTES,
                          alpha=ALPHA)
                  for ind in population]
best_idx = int(np.argmin(fitness_values))
best_perm = population[best_idx]
best_routes = decode_routes(best_perm, capacity=CAPACITY, demands_array=demands)
best_dist = routes_total_distance(best_routes, distance_matrix)

print("Mejor permutación:", best_perm)
print("Rutas decodificadas (índices):", best_routes)
print("Número de rutas:", len(best_routes))
print(f"Distancia total sin penalización: {best_dist:.2f}")

# Convergencia (mejor y promedio)
plt.figure(figsize=(7,4))
plt.plot(best_history, marker='o', linewidth=1, label="Mejor")
plt.plot(avg_history, marker='.', linewidth=1, label="Promedio")
plt.xlabel("Generación")
plt.ylabel("Fitness")
plt.title("Convergencia del GA (VRP con capacidad y tope de vehículos)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("convergencia.png", dpi=150)

# Dibuja rutas
plt.figure(figsize=(6,6))
plt.scatter(coords[0,0], coords[0,1], s=120, marker='s', label='Depot')
plt.scatter(coords[1:,0], coords[1:,1], s=50, marker='o', label='Clientes')

for r_i, r in enumerate(best_routes, start=1):
    # arma la polilínea 0 -> r -> 0
    seq = [0] + r + [0]
    route_xy = coords[seq]
    plt.plot(route_xy[:,0], route_xy[:,1], marker='o', linewidth=1.5, label=f"Ruta {r_i}")

# etiquetas simples
for i, (x, y) in enumerate(coords):
    plt.text(x+0.8, y+0.8, names[i], fontsize=8)

plt.title("Mejor solución (rutas)")
plt.grid(True)
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("solved.png", dpi=150)
