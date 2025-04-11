import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Parameters
model.ca0 = pyo.Param(initialize=1)
model.fa0 = pyo.Param(initialize=10)
model.k0 = pyo.Param(initialize=1.0e6)
model.E = pyo.Param(initialize=8000)
model.R = pyo.Param(initialize=1.987)

# Decision variables
model.T = pyo.Var(domain=pyo.NonNegativeReals, bounds=(300, 500))
model.V = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 10))

# Getting K
def get_k(model):
    return model.k0 * pyo.exp(-(model.E / (model.R * model.T)))

model.k = pyo.Expression(rule=get_k)

# Objective function
def objective_function(model):
    return 1 - pyo.exp(-(model.k * model.V) / model.fa0)

model.obj = pyo.Objective(rule=objective_function, sense=pyo.maximize)

# Resolve
solver = pyo.SolverFactory("ipopt")

# Solver and Check if the solver found a solution
result = solver.solve(model)
pyo.assert_optimal_termination(result)

# Showing results
print(f"Temperature = {model.T.value}, Volume = {model.V.value}")
