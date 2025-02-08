import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.m1s1 = pyo.Var(within=pyo.NonNegativeReals)
model.m1s2 = pyo.Var(within=pyo.NonNegativeReals)
model.m2s1 = pyo.Var(within=pyo.NonNegativeReals)
model.m2s2 = pyo.Var(within=pyo.NonNegativeReals)
model.s1p = pyo.Var(within=pyo.NonNegativeReals)
model.s2p = pyo.Var(within=pyo.NonNegativeReals)

# Objective function
def objective_function(model):
    return \
        model.m1s1 * 2000 + \
        model.m1s2 * 1700 + \
        model.m2s1 * 2000 + \
        model.m2s2 * 1100 + \
        model.s1p * 400 + \
        model.s2p * 800
model.obj = pyo.Objective(rule=objective_function, sense=pyo.minimize)

# Shipping Constraints
model.shipping_m1s1 = pyo.Constraint(expr=model.m1s1 <= 30)
model.shipping_m1s2 = pyo.Constraint(expr=model.m1s2 <= 30)
model.shipping_m2s1 = pyo.Constraint(expr=model.m2s1 <= 70)
model.shipping_m2s2 = pyo.Constraint(expr=model.m2s2 <= 50)
model.shipping_s1p = pyo.Constraint(expr=model.s1p <= 70)
model.shipping_s2p = pyo.Constraint(expr=model.s2p <= 70)

# Necessary Material in the plant Constraints
model.necessary_material_plant = pyo.Constraint(expr=model.s1p + model.s2p == 100)

# Production and shipping to warehouses limits
model.production_m1s1_m1s2 = pyo.Constraint(expr=model.m1s1 + model.m1s2 <= 40)
model.production_m2s1_m2s2 = pyo.Constraint(expr=model.m2s1 + model.m2s2 <= 60)

# Warehouse balance Constraints3
model.balance1 = pyo.Constraint(expr=model.m1s1 + model.m2s1 == model.s1p)
model.balance2 = pyo.Constraint(expr=model.m1s2 + model.m2s2 == model.s2p)

# No negative constrains
model.con_m1s1_no_negative = pyo.Constraint(expr=model.m1s1 >= 0)
model.con_m1s2_no_negative = pyo.Constraint(expr=model.m1s2 >= 0)
model.con_m2s1_no_negative = pyo.Constraint(expr=model.m2s1 >= 0)
model.con_m2s2_no_negative = pyo.Constraint(expr=model.m2s2 >= 0)
model.con_s1p_no_negative = pyo.Constraint(expr=model.s1p >= 0)
model.con_s2p_no_negative = pyo.Constraint(expr=model.s2p >= 0)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print("Total Mimimal Delivery cost: $", model.obj())
print(f"Mine 1 → warehouse 1: {model.m1s1.value} tons")
print(f"Mine 1 → warehouse 2: {model.m1s2.value} tons")
print(f"Mine 2 → warehouse 1: {model.m2s1.value} tons")
print(f"Mine 2 → warehouse 2: {model.m2s2.value} tons")
print(f"warehouse 1 → Plant: {model.s1p.value} tons")
print(f"warehouse 2 → Plant: {model.s2p.value} tons")
