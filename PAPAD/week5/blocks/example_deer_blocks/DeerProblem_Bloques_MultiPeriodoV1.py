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
def deer_block_rule(b):
    # Variables del período
    b.f = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Hembras
    b.d = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Machos jóvenes
    b.b = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Machos adultos
    b.hf = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Caza de hembras
    b.hd = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Caza de machos jóvenes
    b.hb = pyo.Var(initialize=20, within=pyo.PositiveReals)  # Caza de machos adultos
    b.br = pyo.Var(initialize=1.5, within=pyo.PositiveReals)  # Tasa de nacimiento
    b.c = pyo.Var(initialize=500000, within=pyo.PositiveReals)  # Alimento disponible
    
    # Restricciones de balance poblacional
    b.f_bal = pyo.Constraint(expr=b.f == model.p1 * b.br * ((model.p2 / 10.0) * b.f + model.p3 * b.d) - b.hf)
    b.d_bal = pyo.Constraint(expr=b.d == model.p4 * b.d + (model.p5 / 2.0) * b.f - b.hd)
    b.b_bal = pyo.Constraint(expr=b.b == model.p6 * b.b + (model.p5 / 2.0) * b.f - b.hb)
    
    # Restricciones de consumo de alimentos
    b.food_cons = pyo.Constraint(expr=b.c == model.p7 * b.b + model.p8 * b.d + model.p9 * b.f)
    b.supply = pyo.Constraint(expr=b.c <= model.ps)
    
    # Restricción de natalidad
    b.birth = pyo.Constraint(expr=b.br == 1.1 + 0.8 * (model.ps - b.c) / model.ps)
    
    # Restricción de proporción de machos
    b.minbuck = pyo.Constraint(expr=b.b >= (1.0 / 5.0) * (0.4 * b.f + b.d))

# Crear los bloques
model.periods = pyo.Block(range(T), rule=deer_block_rule)

# Conectar períodos (bloques)
def connect_f_rule(m, t):
    return m.periods[t+1].f == model.p4 * (m.periods[t].f - m.periods[t].hf) + 0.5 * m.periods[t].br * m.periods[t].f
model.connect_f = pyo.Constraint(range(T-1), rule=connect_f_rule)

def connect_d_rule(m, t):
    return m.periods[t+1].d == model.p4 * (m.periods[t].d - m.periods[t].hd) + 0.5 * m.periods[t].br * m.periods[t].f
model.connect_d = pyo.Constraint(range(T-1), rule=connect_d_rule)

def connect_b_rule(m, t):
    return m.periods[t+1].b == model.p6 * (m.periods[t].b - m.periods[t].hb) + model.p5 / 2.0 * m.periods[t].f
model.connect_b = pyo.Constraint(range(T-1), rule=connect_b_rule)

# Función objetivo: Maximizar la cosecha total en los períodos
model.obj = pyo.Objective(expr=sum(model.periods[t].hf + model.periods[t].hd + 10 * model.periods[t].hb for t in range(T)), sense=pyo.maximize)

# Resolver el modelo
solver = pyo.SolverFactory('ipopt')
solver.solve(model)

# Mostrar resultados
for t in range(T):
    print(f'Período {t+1}:')
    print(f'  Población de hembras: {pyo.value(model.periods[t].f)}')
    print(f'  Población de machos jóvenes: {pyo.value(model.periods[t].d)}')
    print(f'  Población de machos adultos: {pyo.value(model.periods[t].b)}')
    print(f'  Cosecha de hembras: {pyo.value(model.periods[t].hf)}')
    print(f'  Cosecha de machos jóvenes: {pyo.value(model.periods[t].hd)}')
    print(f'  Cosecha de machos adultos: {pyo.value(model.periods[t].hb)}')
    print('---------------------------')
