import pyomo.environ as pyo

# Preguntar al usuario el número de períodos
T = int(input("Ingrese el número de períodos a modelar: "))

# Crear el modelo
model = pyo.ConcreteModel()

# Parámetros
model.p1 = pyo.Param(initialize=0.88)
model.p2 = pyo.Param(initialize=0.82)
model.p3 = pyo.Param(initialize=0.92)
model.p4 = pyo.Param(initialize=0.84)
model.p5 = pyo.Param(initialize=0.73)
model.p6 = pyo.Param(initialize=0.87)
model.p7 = pyo.Param(initialize=2700)
model.p8 = pyo.Param(initialize=2300)
model.p9 = pyo.Param(initialize=540)
model.ps = pyo.Param(initialize=700000)

# Definir bloques para cada período
def deer_block_rule(b, t):
    # Variables del período t
    b.fawns = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Machos jóvenes
    b.does = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Hembras
    b.bucks = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Machos adultos
    b.hfawns = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Caza de machos jóvenes
    b.hdoes = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Caza de hembras
    b.hbucks = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Caza de machos adultos
    b.br = pyo.Var(initialize=1.5, within=pyo.PositiveReals)  # Tasa de nacimiento
    b.c = pyo.Var(initialize=500000, within=pyo.PositiveReals)  # Alimento disponible
    
    # Restricciones de balance poblacional
    b.fawns_bal = pyo.Constraint(expr=b.fawns == model.p1 * b.br * ((model.p2 / 10.0) * b.fawns + model.p3 * b.does) - b.hfawns)
    b.does_bal = pyo.Constraint(expr=b.does == model.p4 * b.does + (model.p5 / 2.0) * b.fawns - b.hdoes)
    b.bucks_bal = pyo.Constraint(expr=b.bucks == model.p6 * b.bucks + (model.p5 / 2.0) * b.fawns - b.hbucks)
    
    # Restricciones de consumo de alimentos
    b.food_cons = pyo.Constraint(expr=b.c == model.p7 * b.bucks + model.p8 * b.does + model.p9 * b.fawns)
    b.supply = pyo.Constraint(expr=b.c <= model.ps)
    
    # Restricción de natalidad
    b.birth = pyo.Constraint(expr=b.br == 1.1 + 0.8 * (model.ps - b.c) / model.ps)
    
    # Restricción de proporción de machos adultos
    b.minbuck = pyo.Constraint(expr=b.bucks >= (1.0 / 5.0) * (0.4 * b.fawns + b.does))

# Crear los bloques con índices correctos
model.periods = pyo.Block(range(T), rule=lambda b, t: deer_block_rule(b, t))

# Conectar períodos (bloques)
def connect_fawns_rule(m, t):
    return m.periods[t+1].fawns == model.p4 * (m.periods[t].fawns - m.periods[t].hfawns) + 0.5 * m.periods[t].br * m.periods[t].fawns
model.connect_fawns = pyo.Constraint(range(T-1), rule=connect_fawns_rule)

def connect_does_rule(m, t):
    return m.periods[t+1].does == model.p4 * (m.periods[t].does - m.periods[t].hdoes) + 0.5 * m.periods[t].br * m.periods[t].fawns
model.connect_does = pyo.Constraint(range(T-1), rule=connect_does_rule)

def connect_bucks_rule(m, t):
    return m.periods[t+1].bucks == model.p6 * (m.periods[t].bucks - m.periods[t].hbucks) + model.p5 / 2.0 * m.periods[t].fawns
model.connect_bucks = pyo.Constraint(range(T-1), rule=connect_bucks_rule)

# Función objetivo: Maximizar la cosecha total en los períodos
model.obj = pyo.Objective(expr=sum(model.periods[t].hdoes + model.periods[t].hfawns + 10 * model.periods[t].hbucks for t in range(T)), sense=pyo.maximize)

# Resolver el modelo
solver = pyo.SolverFactory('ipopt')
solver.solve(model)

# Mostrar resultados
for t in range(T):
    print(f'Period {t+1}:')
    print(f'Fawns: {pyo.value(model.periods[t].fawns)}')
    print(f'Does: {pyo.value(model.periods[t].does)}')
    print(f'Bucks: {pyo.value(model.periods[t].bucks)}\n')
    
    print(f'Hunt Fawns: {pyo.value(model.periods[t].hfawns)}')
    print(f'Hunt Does: {pyo.value(model.periods[t].hdoes)}')
    print(f'Hunt Bucks: {pyo.value(model.periods[t].hbucks)}')
    print('---------------------------\n')
