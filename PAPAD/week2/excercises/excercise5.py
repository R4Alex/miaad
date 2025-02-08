import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
# model.x = pyo.Var(within=pyo.NonNegativeReals)
# model.y = pyo.Var(within=pyo.NonNegativeReals)
# model.z = pyo.Var(within=pyo.NonNegativeReals)
model.x = pyo.Var(within=pyo.NonNegativeIntegers)
model.y = pyo.Var(within=pyo.NonNegativeIntegers)
model.z = pyo.Var(within=pyo.NonNegativeIntegers)

# Objective function
model.obj = pyo.Objective(expr=model.x * 50 + model.y * 20 + model.z * 25, sense=pyo.maximize)

# Constraints
model.fresadora = pyo.Constraint(expr=model.x * 9 + model.y * 3 + model.z * 5 <= 500)
model.torno = pyo.Constraint(expr=model.x * 5 + model.y * 4 <= 350)
model.rectificadora = pyo.Constraint(expr=model.x * 3 + model.z * 2 <= 150)

# No negative constrains
model.con100 = pyo.Constraint(expr=model.x >= 0)
model.con101 = pyo.Constraint(expr=model.y >= 0)
model.con102 = pyo.Constraint(expr=model.z >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Maximum Profit:", model.obj())
print(f"x = {model.x.value}, y = {model.y.value}, z = {model.z.value}")
