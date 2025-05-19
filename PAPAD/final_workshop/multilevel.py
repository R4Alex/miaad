import pyomo.environ as pyo

# Modelo
model = pyo.ConcreteModel()

# Conjuntos
model.P = pyo.Set()
model.C = pyo.Set()
model.J = pyo.Set()
model.K = pyo.Set()

# Parámetros
model.d = pyo.Param(model.J, model.K, within=pyo.NonNegativeReals)
model.cap_prod = pyo.Param(model.P, model.K, within=pyo.NonNegativeReals)
model.cap_alm = pyo.Param(model.C, model.K, within=pyo.NonNegativeReals)
model.cost_prod = pyo.Param(model.P, model.K, within=pyo.NonNegativeReals)
model.cost_pc = pyo.Param(model.P, model.C, model.K, within=pyo.NonNegativeReals)
model.cost_cj = pyo.Param(model.C, model.J, model.K, within=pyo.NonNegativeReals)

# Variables
model.x = pyo.Var(model.P, model.C, model.K, within=pyo.NonNegativeReals)
model.y = pyo.Var(model.C, model.J, model.K, within=pyo.NonNegativeReals)

#----------------------------------FALTA----------------------------------#
#  Función objetivo


# Restricción 1
def demand_rule(model, j, k):
    return sum(model.y[c,j,k] for c in model.C) == model.d[j,k]
model.Demanda = pyo.Constraint(model.J, model.K, rule=demand_rule)

# Restricción 2
def balance_centro_rule(model, c, k):
    return sum(model.x[p,c,k] for p in model.P) == sum(model.y[c,j,k] for j in model.J)
model.Balance = pyo.Constraint(model.C, model.K, rule=balance_centro_rule)

# Restricción 3
def capacidad_prod_rule(model, p, k):
    return sum(model.x[p,c,k] for c in model.C) <= model.cap_prod[p,k]
model.CapProd = pyo.Constraint(model.P, model.K, rule=capacidad_prod_rule)

# Restricción 4
def capacidad_alm_rule(model, c, k):
    return sum(model.y[c,j,k] for j in model.J) <= model.cap_alm[c,k]
model.CapAlm = pyo.Constraint(model.C, model.K, rule=capacidad_alm_rule)

# === SOLVER ===
solver = pyo.SolverFactory('glpk')

results = solver.solve(model, tee=True)


# Valor óptimo
print("Costo total mínimo:", pyo.value(model.obj))

