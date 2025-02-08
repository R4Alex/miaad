import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.x = pyo.Var(within=pyo.NonNegativeReals)
model.y = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
model.obj = pyo.Objective(expr=model.x * 4500 + model.y * 4500, sense=pyo.maximize)

# Constraints
model.money = pyo.Constraint(expr=model.x * 5000 + model.y * 4000 <= 6000)
model.time = pyo.Constraint(expr=model.x * 400 + model.y * 500 <= 600)

# No negative constrains
model.con100 = pyo.Constraint(expr=model.x >= 0)
model.con101 = pyo.Constraint(expr=model.y >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Maximum Profit:", model.obj())
print(f"x = {model.x.value}, y = {model.y.value}")
