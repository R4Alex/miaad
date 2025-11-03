from scipy.stats import binom

# n = 20, p = 0.25
1 - binom.cdf(9, 20, 0.25)


sum([binom.pmf(k, 20, 0.25) for k in range(5, 9)])


sum([binom.pmf(k, 20, 0.25) for k in range(3)])


#################################

import numpy as np
import matplotlib.pyplot as plt

def rand0(seed, n):
    a = 1664525
    c = 1013904223
    m = 2**32
    x = seed
    values = []
    for _ in range(n):
        x = (a * x + c) % m
        values.append(x / m)
    return values

def rand1(seed, n):
    a = 1103515245
    c = 12345
    m = 2**31
    x = seed
    values = []
    for _ in range(n):
        x = (a * x + c) % m
        values.append(x / m)
    return values

def rand2(seed, n):
    np.random.seed(seed)
    values = []
    table = np.random.rand(32)
    x = seed
    for _ in range(n):
        j = int(32 * (x % 1))
        x = 1664525 * x + 1013904223
        x = x % 2**32
        new = table[j]
        table[j] = x / 2**32
        values.append(new)
    return values

def rand3(seed, n):
    np.random.seed(seed)
    return np.random.uniform(0, 1, n).tolist()

def plot_histogram(values, title):
    plt.hist(values, bins=50, density=True, edgecolor='black')
    plt.title(title)
    plt.xlabel('Valor generado')
    plt.ylabel('Frecuencia relativa')
    plt.grid(True)
    # plt.show()
    plt.savefig("comparations_%s_plot.png" % title)

seed = 123456789
n = 10000

generators = [
    ('rand0', rand0(seed, n)),
    ('rand1', rand1(seed, n)),
    ('rand2', rand2(seed, n)),
    ('rand3', rand3(seed, n)),
]

for name, data in generators:
    plot_histogram(data, f"Histograma de {name}")


np.random.randint(0, 6)
