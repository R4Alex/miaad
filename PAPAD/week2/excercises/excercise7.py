import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.x = pyo.Var(within=pyo.NonNegativeReals)
model.y = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
model.obj = pyo.Objective(expr=model.x * 4 + model.y * 2, sense=pyo.minimize)

# Constraints
model.con0 = pyo.Constraint(expr=model.x * 5 + model.y * 15 >= 50)
model.con1 = pyo.Constraint(expr=model.x * 20 + model.y * 5 >= 40)
model.con2 = pyo.Constraint(expr=model.x * 15 + model.y * 2 >= 60)

# No negative constrains
model.con100 = pyo.Constraint(expr=model.x >= 0)
model.con101 = pyo.Constraint(expr=model.y >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Daily Mimimal cost:", model.obj())
print(f"x = {model.x.value}, y = {model.y.value}")
