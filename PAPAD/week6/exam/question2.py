import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.A = pyo.Var(within=pyo.NonNegativeIntegers)
model.B = pyo.Var(within=pyo.NonNegativeIntegers)

# Objective function
model.obj = pyo.Objective(expr=model.A * 40 + model.B * 80, sense=pyo.maximize)

# Constraints
# Limit Hours
model.limit_hours = pyo.Constraint(expr=model.A * 2 + model.B * 3 <= 105)
model.max_production_A = pyo.Constraint(expr=model.A <= 30)
model.max_production_B = pyo.Constraint(expr=model.B <= 20)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Maximum Profit:", model.obj())
print(f"A = {model.A.value}, B = {model.B.value}")

