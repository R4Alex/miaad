import pyomo.environ as pyo

# Crear el modelo
model = pyo.ConcreteModel()

# Variables de decisión
model.x11 = pyo.Var(within=pyo.NonNegativeReals)
model.x12 = pyo.Var(within=pyo.NonNegativeReals)
model.x21 = pyo.Var(within=pyo.NonNegativeReals)
model.x22 = pyo.Var(within=pyo.NonNegativeReals)

# Función objetivo
model.obj = pyo.Objective(
    expr=4 * model.x11 + 6 * model.x12 + 5 * model.x21 + 4 * model.x22, sense=pyo.minimize
)

# Restricciones
model.con1 = pyo.Constraint(expr=model.x11 + model.x12 <= 50)
model.con2 = pyo.Constraint(expr=model.x21 + model.x22 <= 60)
model.con3 = pyo.Constraint(expr=model.x11 + model.x21 >= 40)
model.con4 = pyo.Constraint(expr=model.x12 + model.x22 >= 70)

# Resolver
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Mostrar resultados
print("Costo mínimo:", model.obj())
print(f"x11 = {model.x11.value}, x12 = {model.x12.value}")
print(f"x21 = {model.x21.value}, x22 = {model.x22.value}")
