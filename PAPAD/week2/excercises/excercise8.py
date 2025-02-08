import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.x = pyo.Var(within=pyo.NonNegativeReals)
model.y = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
model.obj = pyo.Objective(expr=model.x * 0.4 + model.y * 0.8, sense=pyo.minimize)

# Constraints
model.con0 = pyo.Constraint(expr=model.x * 800 + model.y * 1000 >= 8000)
model.con1 = pyo.Constraint(expr=model.x * 140 + model.y * 70 >= 700)

# No negative constrains
model.con100 = pyo.Constraint(expr=model.x >= 0)
model.con101 = pyo.Constraint(expr=model.y >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Daily Mimimal cost:", model.obj())
print(f"Alimento X = {model.x.value}, Alimento Y(x2) = {model.y.value}")
