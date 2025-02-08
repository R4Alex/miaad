import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.x = pyo.Var(within=pyo.NonNegativeReals)
model.y = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
model.obj = pyo.Objective(expr=model.x * 5 + model.y * 2, sense=pyo.maximize)

# Constraints
model.con1 = pyo.Constraint(expr=model.x * 3 + model.y * 2 <= 2400)

# Individual constrains
model.con2 = pyo.Constraint(expr=model.x * 2 <= 1200)
model.con3 = pyo.Constraint(expr=model.y <= 800)

# No negative constrains
model.con100 = pyo.Constraint(expr=model.x >= 0)
model.con101 = pyo.Constraint(expr=model.y >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Maximum Profit:", model.obj())
print(f"x = {model.x.value}, y = {model.y.value}")
print(f"seguros = {model.x.value}, hipotecas = {model.y.value}")
