import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.A_C1 = pyo.Var(within=pyo.NonNegativeIntegers)
model.A_C2 = pyo.Var(within=pyo.NonNegativeIntegers)
model.A_C3 = pyo.Var(within=pyo.NonNegativeIntegers)
model.A_C4 = pyo.Var(within=pyo.NonNegativeIntegers)
model.A_C5 = pyo.Var(within=pyo.NonNegativeIntegers)
model.B_C1 = pyo.Var(within=pyo.NonNegativeIntegers)
model.B_C2 = pyo.Var(within=pyo.NonNegativeIntegers)
model.B_C3 = pyo.Var(within=pyo.NonNegativeIntegers)
model.B_C4 = pyo.Var(within=pyo.NonNegativeIntegers)
model.B_C5 = pyo.Var(within=pyo.NonNegativeIntegers)

# Objective function
def objective_function(model):
    return \
        model.A_C1 * 2 + \
        model.A_C2 * 4 + \
        model.A_C3 * 5 + \
        model.A_C4 * 2 + \
        model.A_C5 * 1 + \
        model.B_C1 * 3 + \
        model.B_C2 * 1 + \
        model.B_C3 * 3 + \
        model.B_C4 * 2 + \
        model.B_C5 * 3
model.obj = pyo.Objective(rule=objective_function, sense=pyo.minimize)

# Boxes production in each plant
model.production_in_plant_A = pyo.Constraint(expr=model.A_C1 + model.A_C2 + model.A_C3 + model.A_C4 + model.A_C5 <= 1000)
model.production_in_plant_B = pyo.Constraint(expr=model.B_C1 + model.B_C2 + model.B_C3 + model.B_C4 + model.B_C5 <= 4000)

# Each "BAR (C)" should receved its demand
model.C1_demand = pyo.Constraint(expr=model.A_C1 + model.B_C1 == 500)
model.C2_demand = pyo.Constraint(expr=model.A_C2 + model.B_C2 == 900)
model.C3_demand = pyo.Constraint(expr=model.A_C3 + model.B_C3 == 1800)
model.C4_demand = pyo.Constraint(expr=model.A_C4 + model.B_C4 == 200)
model.C5_demand = pyo.Constraint(expr=model.A_C5 + model.B_C5 == 700)

# Resolve
solver = pyo.SolverFactory('glpk')
result = solver.solve(model)

# Showing results
print(f"Cervecería A al Bar 1 = {model.A_C1.value}")
print(f"Cervecería A al Bar 2 = {model.A_C2.value}")
print(f"Cervecería A al Bar 3 = {model.A_C3.value}")
print(f"Cervecería A al Bar 4 = {model.A_C4.value}")
print(f"Cervecería A al Bar 5 = {model.A_C5.value}")

print(f"Cervecería B al Bar 1 = {model.B_C1.value}")
print(f"Cervecería B al Bar 2 = {model.B_C2.value}")
print(f"Cervecería B al Bar 3 = {model.B_C3.value}")
print(f"Cervecería B al Bar 4 = {model.B_C4.value}")
print(f"Cervecería B al Bar 5 = {model.B_C5.value}")

print(f"Esta ruta genera un costo total de transporte de ${model.obj():.2f}")
