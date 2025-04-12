import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
# The bounds are set according to the problem statement.
model.xa = pyo.Var(domain=pyo.NonNegativeIntegers, bounds=(10, 38.7))
model.yb = pyo.Var(domain=pyo.NonNegativeIntegers, bounds=(20, 42.72))

###### Decision Variables but no actually variables
def get_ηa(model):
    return 0.9 - 0.0005 * model.xa ** 2

def get_ηb(model):
    return 0.88 - 0.0004 * model.yb ** 2

model.ηa = pyo.Expression(rule=get_ηa)
model.ηb = pyo.Expression(rule=get_ηb)

# Parameters
model.h = pyo.Param(initialize=4200)
model.pci = pyo.Param(initialize=45000)

# Building Objective function
# The objective function is to minimize the fuel usage
def objective_function(model):
    return (
        ((model.xa * model.h) / (model.ηa * model.pci)) + ((model.yb * model.h) / (model.ηb * model.pci))
    )

model.obj = pyo.Objective(rule=objective_function, sense=pyo.minimize)

# Constraints
model.ηa_limit_constraint = pyo.Constraint(expr=model.ηa >= 0.15)
model.ηb_limit_constraint = pyo.Constraint(expr=model.ηb >= 0.15)

model.demand_constraint = pyo.Constraint(expr=model.xa + model.yb == 60)

# Resolve
solver = pyo.SolverFactory('ipopt')

# Solver and Check if the solver found a solution
# result = solver.solve(model, tee=True)
result = solver.solve(model)
pyo.assert_optimal_termination(result)

# Showing results
print("Final Minimal Fuel Consumed:", model.obj())
print(f"Steam produced by A = {model.xa.value}")
print(f"Steam produced by B = {model.yb.value}")
print(f"Final value of ηa = {pyo.value(model.ηa)}")
print(f"Final value of ηb = {pyo.value(model.ηb)}")
