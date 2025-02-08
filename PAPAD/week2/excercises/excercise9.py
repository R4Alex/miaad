import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.x11 = pyo.Var(within=pyo.NonNegativeReals)
model.x12 = pyo.Var(within=pyo.NonNegativeReals)
model.x13 = pyo.Var(within=pyo.NonNegativeReals)
model.x21 = pyo.Var(within=pyo.NonNegativeReals)
model.x22 = pyo.Var(within=pyo.NonNegativeReals)
model.x23 = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
def objective_function(model):
    return \
        model.x11 * 600 + \
        model.x12 * 800 + \
        model.x13 * 700 + \
        model.x21 * 400 + \
        model.x22 * 900 + \
        model.x23 * 600
model.obj = pyo.Objective(rule=objective_function, sense=pyo.minimize)

# Customer Constraints
model.customer1_order = pyo.Constraint(expr=model.x11 + model.x21 == 300)
model.customer2_order = pyo.Constraint(expr=model.x12 + model.x22 == 200)
model.customer3_order = pyo.Constraint(expr=model.x13 + model.x23 == 400)

# Production Constraints
model.factory1_production = pyo.Constraint(expr=model.x11 + model.x12 + model.x13 <= 400)
model.factory2_production = pyo.Constraint(expr=model.x21 + model.x22 + model.x23 <= 500)

# No negative constrains
model.con_x11_no_negative = pyo.Constraint(expr=model.x11 >= 0)
model.con_x12_no_negative = pyo.Constraint(expr=model.x12 >= 0)
model.con_x13_no_negative = pyo.Constraint(expr=model.x13 >= 0)
model.con_x21_no_negative = pyo.Constraint(expr=model.x21 >= 0)
model.con_x22_no_negative = pyo.Constraint(expr=model.x22 >= 0)
model.con_x23_no_negative = pyo.Constraint(expr=model.x23 >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Total Mimimal Delivery cost: $", model.obj())
print(f"Units from Factory 1 to Client 1: {model.x11.value}")
print(f"Units from Factory 1 to Client 2: {model.x12.value}")
print(f"Units from Factory 1 to Client 3: {model.x13.value}")
print(f"Units from Factory 2 to Client 1: {model.x21.value}")
print(f"Units from Factory 2 to Client 2: {model.x22.value}")
print(f"Units from Factory 2 to Client 3: {model.x23.value}")
