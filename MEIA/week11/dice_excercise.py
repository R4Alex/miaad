import random

def simular_dados(n=1000000):
    suma_7 = 0
    suma_mayor_10 = 0

    for _ in range(n):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        suma = d1 + d2

        if suma == 7:
            suma_7 += 1
        if suma > 10:
            suma_mayor_10 += 1

    prob_7 = suma_7 / n
    prob_mayor_10 = suma_mayor_10 / n

    return prob_7, prob_mayor_10

# Ejecutar simulación
n_simulaciones = 1000000
sim_7, sim_mayor_10 = simular_dados(n_simulaciones)

# Resultados teóricos
teo_7 = 6 / 36
teo_mayor_10 = 3 / 36

# Mostrar resultados
print(f"Probabilidad teórica (suma = 7):       {teo_7:.4f}")
print(f"Probabilidad simulada (suma = 7):       {sim_7:.4f}")
print(f"Diferencia absoluta:                   {abs(teo_7 - sim_7):.5f}")

print(f"\nProbabilidad teórica (suma > 10):      {teo_mayor_10:.4f}")
print(f"Probabilidad simulada (suma > 10):      {sim_mayor_10:.4f}")
print(f"Diferencia absoluta:                   {abs(teo_mayor_10 - sim_mayor_10):.5f}")