import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

N = ['Harlingen', 'Memphis', 'Ashland']
M = ['NYC', 'LA', 'Chicago', 'Houston']
P = 2

# X indica la demanda de cada cliente por que almcacen es suplida
model.x = pyo.Var(N, M, bounds=(0, 1))
# y indica si un almacen se debe construir
model.y = pyo.Var(N, within=pyo.Binary)
# Diccionario de costos
d = {
    ('Harlingen', 'NYC'): 1956,
    ('Harlingen', 'LA'): 1606,
    ('Harlingen', 'Chicago'): 1410,
    ('Harlingen', 'Houston'): 330,

    ('Memphis', 'NYC'): 1096,
    ('Memphis', 'LA'): 1792,
    ('Memphis', 'Chicago'): 531,
    ('Memphis', 'Houston'): 567,

    ('Ashland', 'NYC'): 485,
    ('Ashland', 'LA'): 2322,
    ('Ashland', 'Chicago'): 324,
    ('Ashland', 'Houston'): 1236,
}

# Funcion objetivo
def obj_rule(mdl):
    return sum(d[n, m] * mdl.x[n, m] for n in N for m in M)

model.obj = pyo.Objective(rule=obj_rule)

# Restriccion de demanda por almacen, un demanda no puede ser suplica por un almacen que no esta construido
def warehouse_active_rule(mdl, n, m):
    return mdl.x[n, m] <= mdl.y[n]
model.warehouse_active = pyo.Constraint(N, M, rule=warehouse_active_rule)

# Restriccion del numero maximo de almacenes a construir
def num_warehouses_rule(mdl):
    return sum(mdl.y[n] for n in N) <= P
model.num_wharehouses = pyo.Constraint(rule=num_warehouses_rule)

# Resolver el modelo
solver = pyo.SolverFactory('glpk')
res = solver.solve(model)
pyo.assert_optimal_termination(res)
model.y.pprint()
model.x.pprint()
print("Costo minimo:", model.obj())
