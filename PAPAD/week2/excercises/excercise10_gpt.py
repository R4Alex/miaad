from pyomo.environ import *

# Crear el modelo
model = ConcreteModel()

# Variables de decisión (toneladas enviadas entre nodos)
model.x_M1S1 = Var(domain=NonNegativeReals)  # Mina 1 → Almacén 1
model.x_M1S2 = Var(domain=NonNegativeReals)  # Mina 1 → Almacén 2
model.x_M2S1 = Var(domain=NonNegativeReals)  # Mina 2 → Almacén 1
model.x_M2S2 = Var(domain=NonNegativeReals)  # Mina 2 → Almacén 2
model.x_S1P = Var(domain=NonNegativeReals)   # Almacén 1 → Planta
model.x_S2P = Var(domain=NonNegativeReals)   # Almacén 2 → Planta

# Función Objetivo: Minimizar el costo total de transporte
model.obj = Objective(expr=
    2000 * model.x_M1S1 + 1700 * model.x_M1S2 + 
    2000 * model.x_M2S1 + 1100 * model.x_M2S2 + 
    400 * model.x_S1P + 800 * model.x_S2P, 
    sense=minimize)

# Restricciones de producción en las minas
model.prod_M1 = Constraint(expr=model.x_M1S1 + model.x_M1S2 <= 40)  # Mina 1 produce 40 toneladas
model.prod_M2 = Constraint(expr=model.x_M2S1 + model.x_M2S2 <= 60)  # Mina 2 produce 60 toneladas

# Restricciones de capacidad de transporte
model.cap_M1S1 = Constraint(expr=model.x_M1S1 <= 30)  # M1 → S1 máx 30
model.cap_M1S2 = Constraint(expr=model.x_M1S2 <= 30)  # M1 → S2 máx 30
model.cap_M2S1 = Constraint(expr=model.x_M2S1 <= 70)  # M2 → S1 máx 70
model.cap_M2S2 = Constraint(expr=model.x_M2S2 <= 50)  # M2 → S2 máx 50
model.cap_S1P = Constraint(expr=model.x_S1P <= 70)    # S1 → P máx 70
model.cap_S2P = Constraint(expr=model.x_S2P <= 70)    # S2 → P máx 70

# Restricción de demanda en la planta (se requieren exactamente 100 toneladas)
model.demand_P = Constraint(expr=model.x_S1P + model.x_S2P == 100)

# Balance de flujo en los almacenes (todo lo que entra debe salir)
model.flow_S1 = Constraint(expr=model.x_M1S1 + model.x_M2S1 == model.x_S1P)  # S1
model.flow_S2 = Constraint(expr=model.x_M1S2 + model.x_M2S2 == model.x_S2P)  # S2

# Resolver el modelo usando el solver GLPK
solver = SolverFactory('glpk')
solver.solve(model)

# Mostrar resultados
print("Plan Óptimo de Transporte:")
print(f"Mina 1 → Almacén 1: {model.x_M1S1.value} toneladas")
print(f"Mina 1 → Almacén 2: {model.x_M1S2.value} toneladas")
print(f"Mina 2 → Almacén 1: {model.x_M2S1.value} toneladas")
print(f"Mina 2 → Almacén 2: {model.x_M2S2.value} toneladas")
print(f"Almacén 1 → Planta: {model.x_S1P.value} toneladas")
print(f"Almacén 2 → Planta: {model.x_S2P.value} toneladas")
print(f"Costo mínimo total de transporte: ${model.obj.expr()}")
