# A pyomo model for the Rosenbrock Problem
import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.x = pyo.Var(initialize=1.5)
model.y = pyo.Var(initialize=1.5)

def rosenbrock(model):
    return (1.0 - model.x) ** 2 + 100.0 * (model.y - model.x**2)**2

model.obj = pyo.Objective(rule=rosenbrock, sense=pyo.minimize)
status = pyo.SolverFactory("ipopt").solve(model)
pyo.assert_optimal_termination(status)
model.pprint()
print("Valor minimo:", model.obj())
model.x.pprint()
