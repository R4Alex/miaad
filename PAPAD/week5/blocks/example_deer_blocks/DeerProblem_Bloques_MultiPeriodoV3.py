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

# Definir bloques para cada período (ahora desde T hasta 1 para corregir la inversión)
model.periods = pyo.Block(range(T, 0, -1))  # Se crea en orden inverso

def deer_block_rule(b, t):
    # Variables del período t
    b.fawns = pyo.Var(initialize=20, within=pyo.PositiveReals)  
    b.does = pyo.Var(initialize=20, within=pyo.PositiveReals)  
    b.bucks = pyo.Var(initialize=20, within=pyo.PositiveReals)  
    b.hfawns = pyo.Var(initialize=20, within=pyo.PositiveReals)  
    b.hdoes = pyo.Var(initialize=20, within=pyo.PositiveReals)  
    b.hbucks = pyo.Var(initialize=20, within=pyo.PositiveReals)  
    b.br = pyo.Var(initialize=1.5, within=pyo.PositiveReals)  
    b.c = pyo.Var(initialize=500000, within=pyo.PositiveReals)  
    
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

# Aplicar la regla de bloques a cada período
for t in range(T, 0, -1):
    deer_block_rule(model.periods[t], t)

# Conectar períodos asegurando la dirección correcta
def connect_fawns_rule(m, t):
    if t > 1:  # Ahora conectamos correctamente hacia adelante
        return m.periods[t-1].fawns == model.p4 * (m.periods[t].fawns - m.periods[t].hfawns) + 0.5 * m.periods[t].br * m.periods[t].fawns
    return pyo.Constraint.Skip
model.connect_fawns = pyo.Constraint(range(T, 1, -1), rule=connect_fawns_rule)

def connect_does_rule(m, t):
    if t > 1:
        return m.periods[t-1].does == model.p4 * (m.periods[t].does - m.periods[t].hdoes) + 0.5 * m.periods[t].br * m.periods[t].fawns
    return pyo.Constraint.Skip
model.connect_does = pyo.Constraint(range(T, 1, -1), rule=connect_does_rule)

def connect_bucks_rule(m, t):
    if t > 1:
        return m.periods[t-1].bucks == model.p6 * (m.periods[t].bucks - m.periods[t].hbucks) + model.p5 / 2.0 * m.periods[t].fawns
    return pyo.Constraint.Skip
model.connect_bucks = pyo.Constraint(range(T, 1, -1), rule=connect_bucks_rule)

# Función objetivo: Maximizar la cosecha total en los períodos
model.obj = pyo.Objective(expr=sum(model.periods[t].hdoes + model.periods[t].hfawns + 10 * model.periods[t].hbucks for t in range(T, 0, -1)), sense=pyo.maximize)

# Resolver el modelo
solver = pyo.SolverFactory('ipopt')
solver.solve(model)

# Mostrar resultados en el orden correcto
for t in range(1, T+1):  # Ahora recorremos de 1 a T como se espera
    print(f'Period {t}:')
    print(f'Fawns: {pyo.value(model.periods[t].fawns)}')
    print(f'Does: {pyo.value(model.periods[t].does)}')
    print(f'Bucks: {pyo.value(model.periods[t].bucks)}\n')
    
    print(f'Hunt Fawns: {pyo.value(model.periods[t].hfawns)}')
    print(f'Hunt Does: {pyo.value(model.periods[t].hdoes)}')
    print(f'Hunt Bucks: {pyo.value(model.periods[t].hbucks)}')
    print('---------------------------\n')
