import pyomo.environ as pyo
import pandas as pd


lambda_risk = input("Input a lambda risk: ")
lambda_risk = float(lambda_risk)


# Load Data
# Load the covariance matrix
expected_financial_returns = pd.read_csv("expected_returns_portfolio.csv")
expected_financial_returns = expected_financial_returns.get("RendimientoEsperado").values

# Load the covariance matrix
covariance_matrix_data = pd.read_csv("covariance_matrix_portafolio.csv", index_col=0)
covariance_dict = covariance_matrix_data.to_dict()

# Create the model
model = pyo.ConcreteModel()

# Decision variables and parameters
assets = list(covariance_matrix_data.columns)
model.assets = pyo.Set(initialize=assets)
model.x = pyo.Var(model.assets, domain=pyo.NonNegativeReals)

# Parameters (mainly covariance)
def init_covariance(model, i, j):
    return covariance_dict[i][j]

# model.covariances = pyo.Param(model.assets, model.assets, initialize=init_covariance, within=pyo.Any)
model.covariances = pyo.Param(model.assets, model.assets, initialize=init_covariance)

# Constraints
def total_investment_rule(model):
    return sum(model.x[i] for i in model.assets) == 1

model.total_investment_constraint = pyo.Constraint(rule=total_investment_rule)

expected_return_dict = {asset: expected_financial_returns[idx] for idx, asset in enumerate(assets)}
model.returns = pyo.Param(model.assets, initialize=expected_return_dict)

def objective_function(model):
    expected_return = sum(model.returns[i] * model.x[i] for i in model.assets)
    risk = sum(model.covariances[i, j] * model.x[i] * model.x[j] for i in model.assets for j in model.assets)
    
    return expected_return - lambda_risk * risk

model.obj = pyo.Objective(rule=objective_function, sense=pyo.maximize)

# Resolve
solver = pyo.SolverFactory("ipopt")

# Solver and Check if the solver found a solution
# result = solver.solve(model, tee=True)
result = solver.solve(model)
pyo.assert_optimal_termination(result)

# Showing results
print("Maximized Performance:", model.obj())
for i in model.assets:
    print(f"Invest to Asset {i}: {pyo.value(model.x[i])}")
