import pyomo.environ as pyo

model = pyo.ConcreteModel()

# Parámetros generales
model.T = pyo.RangeSet(2)  # Dos periodos
model.p1 = pyo.Param()
model.p2 = pyo.Param()
model.p3 = pyo.Param()
model.p4 = pyo.Param()
model.p5 = pyo.Param()
model.p6 = pyo.Param()
model.p7 = pyo.Param()
model.p8 = pyo.Param()
model.p9 = pyo.Param()
model.ps = pyo.Param()

# Crear un bloque 
def deer_block_rule(b, t):
    # Variables
    b.f = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.d = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.b = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.hf = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.hd = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.hb = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.br = pyo.Var(initialize=1.5, within=pyo.PositiveReals)
    b.c = pyo.Var(initialize=500000, within=pyo.PositiveReals)
    
    # Restricciones
    b.f_bal = pyo.Constraint(expr=b.f == model.p1 * b.br * (model.p2 / 10.0 * b.f + model.p3 * b.d) - b.hf)
    b.d_bal = pyo.Constraint(expr=b.d == model.p4 * b.d + model.p5 / 2.0 * b.f - b.hd)
    b.b_bal = pyo.Constraint(expr=b.b == model.p6 * b.b + model.p5 / 2.0 * b.f - b.hb)
    b.food_cons = pyo.Constraint(expr=b.c == model.p7 * b.b + model.p8 * b.d + model.p9 * b.f)
    b.supply = pyo.Constraint(expr=b.c <= model.ps)
    b.birth = pyo.Constraint(expr=b.br == 1.1 + 0.8 * (model.ps - b.c) / model.ps)
    b.minbuck = pyo.Constraint(expr=b.b >= 1.0 / 5.0 * (0.4 * b.f + b.d))

# Asignar el bloque al modelo para cada periodo
model.deer_block = pyo.Block(model.T, rule=deer_block_rule)

# Vincular los bloques entre periodos

def transition_rule(m, t):
    if t == m.T.first():
        return pyo.Constraint.Skip
    return [
        m.deer_block[t].f == 0.5 * m.deer_block[t-1].br,  # Crías hembras sobreviven y maduran
        m.deer_block[t].b == 0.5 * m.deer_block[t-1].br,  # Crías machos sobreviven y maduran
        m.deer_block[t].d >= m.deer_block[t-1].d * model.p4 - m.deer_block[t-1].hd,  # Supervivencia hembras
        m.deer_block[t].b >= m.deer_block[t-1].b * model.p6 - m.deer_block[t-1].hb   # Supervivencia machos
    ]

model.transition = pyo.Constraint(model.T, rule=transition_rule)

# Definir la función objetivo
model.obj = pyo.Objective(expr=sum(10 * model.deer_block[t].hb + model.deer_block[t].hd + model.deer_block[t].hf for t in model.T), sense=pyo.maximize)

# Resolver el modelo
instance = model.create_instance('DeerProblem.dat')
solver = pyo.SolverFactory('ipopt')
status = solver.solve(instance)
pyo.assert_optimal_termination(status)

# Imprimir resultados
instance.pprint()
