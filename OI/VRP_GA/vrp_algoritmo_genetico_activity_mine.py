import json
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd


# Coordenadas de los puntos (depósito + clientes)
# READ info from Files
locations = {}
with open("vrp_agricola_metadata.json", "r") as file:
    data = json.load(file)
    locations["Depot"] = (data["depot"]["x"], data["depot"]["y"])

data = pd.read_csv("vrp_agricola_24clientes_4vehiculos.csv")
data = data.set_index("cliente_id")[["x", "y"]].apply(tuple, axis=1).to_dict()
locations.update(data)

import pdb; pdb.set_trace()


names = list(locations.keys())
coords = np.array([locations[name] for name in names])
num_locations = len(coords)


def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Matriz de distancias
distance_matrix = np.zeros((num_locations, num_locations))
for i in range(num_locations):
    for j in range(num_locations):
        distance_matrix[i, j] = euclidean(coords[i], coords[j])

def total_distance(route):
    dist = 0
    dist += distance_matrix[0, route[0]]  # del depósito al primer cliente
    for i in range(len(route) - 1):
        dist += distance_matrix[route[i], route[i+1]]
    dist += distance_matrix[route[-1], 0]  # regreso al depósito
    return dist

def initial_population(size):
    customers = list(range(1, num_locations))
    return [random.sample(customers, len(customers)) for _ in range(size)]

population_size = 6
population = initial_population(population_size)
population


fitness_values = [total_distance(ind) for ind in population]
for ind, dist in zip(population, fitness_values):
    route_names = [names[i] for i in ind]
    print(f"Ruta: {route_names} -> Distancia: {dist:.2f}")


def tournament_selection(population, fitness_values, k=3):
    selected = []
    for _ in range(len(population)):
        aspirants = random.sample(list(zip(population, fitness_values)), k)
        winner = min(aspirants, key=lambda x: x[1])
        selected.append(winner[0])
    return selected

selected = tournament_selection(population, fitness_values)
selected

def crossover(parent1, parent2):
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

def crossover_population(parents):
    offspring = []
    for i in range(0, len(parents), 2):
        p1, p2 = parents[i], parents[i+1]
        c1 = crossover(p1, p2)
        c2 = crossover(p2, p1)
        offspring.extend([c1, c2])
    return offspring

offspring = crossover_population(selected)
offspring


def mutate(individual, rate=0.1):
    if random.random() < rate:
        a, b = random.sample(range(len(individual)), 2)
        individual[a], individual[b] = individual[b], individual[a]
    return individual

def mutate_population(population, rate=0.1):
    return [mutate(ind.copy(), rate) for ind in population]

mutated = mutate_population(offspring)
mutated


generations = 20
best_history = []

population = initial_population(population_size)

for g in range(generations):
    fitness_values = [total_distance(ind) for ind in population]
    best_dist = min(fitness_values)
    best_history.append(best_dist)
    print(f"Generación {g}: mejor distancia = {best_dist:.2f}")

    selected = tournament_selection(population, fitness_values)
    offspring = crossover_population(selected)
    population = mutate_population(offspring)

# Gráfica de convergencia
plt.plot(best_history, marker='o')
plt.xlabel("Generación")
plt.ylabel("Mejor distancia")
plt.title("Convergencia del Algoritmo Genético (VRP simple)")
plt.grid(True)
# plt.show()
plt.savefig('convergencia.png')

# Mejor ruta encontrada
fitness_values = [total_distance(ind) for ind in population]
best = population[np.argmin(fitness_values)]

route_coords = [coords[0]] + [coords[i] for i in best] + [coords[0]]
route_names = [names[0]] + [names[i] for i in best] + [names[0]]
print(" -> ".join(route_names))

x, y = zip(*route_coords)
plt.figure(figsize=(6, 6))
plt.plot(x, y, marker='o')
for i, name in enumerate(route_names):
    plt.text(x[i]+1, y[i]+1, name)
plt.title("Mejor Ruta Encontrada")
plt.grid(True)
# plt.show()
plt.savefig('solved.png')
