import pyomo.environ as pyo

# Crear el modelo
model = pyo.ConcreteModel()

# Variables de decisión
model.x1 = pyo.Var(within=pyo.NonNegativeReals)
model.x2 = pyo.Var(within=pyo.NonNegativeReals)

# Función objetivo
model.obj = pyo.Objective(expr=30 * model.x1 + 40 * model.x2, sense=pyo.maximize)

# Restricciones
model.con1 = pyo.Constraint(expr=2 * model.x1 + model.x2 <= 100)
model.con2 = pyo.Constraint(expr=model.x1 + 3 * model.x2 <= 90)
model.con3 = pyo.Constraint(expr=model.x1 + model.x2 >= 0)

# Resolver
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Mostrar resultados
print("Ganancia máxima:", model.obj())
print(f"x1 = {model.x1.value}, x2 = {model.x2.value}")

