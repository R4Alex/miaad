import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.x = pyo.Var(within=pyo.NonNegativeReals)
model.y = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
model.obj = pyo.Objective(expr=model.x * 120 + model.y * 80, sense=pyo.maximize)

# Sonstraints
model.con1 = pyo.Constraint(expr=model.x * 20 + model.y * 10 <= 500)

model.con2 = pyo.Constraint(expr=model.x <= 40)
model.con3 = pyo.Constraint(expr=model.y <= 10)

model.con4 = pyo.Constraint(expr=model.x >= 0)
model.con5 = pyo.Constraint(expr=model.y >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Maximum Profit:", model.obj())
print(f"x = {model.x.value}, y = {model.y.value}")
print(f"Televisores 27' = {model.x.value}, Televisores 20' = {model.y.value}")

