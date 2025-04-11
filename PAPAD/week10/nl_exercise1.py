import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
# The decision variables are the amounts of fuel A and B to be used
# in the mixture. The bounds are set according to the problem statement.
model.xa = pyo.Var(domain=pyo.NonNegativeIntegers, bounds=(0, 70))
model.xb = pyo.Var(domain=pyo.NonNegativeIntegers, bounds=(0, 80))

# Objective function
# The objective function is to minimize the cost of the mixture, the cost of the fuel A: 50 and B: 35
model.obj = pyo.Objective(expr=model.xa * 50 + model.xb * 35, sense=pyo.minimize)

# Constraints
model.demand_constraint = pyo.Constraint(expr=model.xa + model.xb == 95)
model.co2_limit_constraint = pyo.Constraint(expr=model.xa * 3 + model.xb * 2.1 <= 275)
model.octane_constraint = pyo.Constraint(expr=(model.xa * 92 + model.xb * 70) / (model.xa + model.xb) >= 80)

# Resolve
solver = pyo.SolverFactory('ipopt')

# Solver and Check if the solver found a solution
# result = solver.solve(model, tee=True)
result = solver.solve(model)
pyo.assert_optimal_termination(result)

# Showing results
print("Final Minimal Cost:", model.obj())
print(f"Fuel A = {model.xa.value}, Fuel B = {model.xb.value}")
