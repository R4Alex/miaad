# DeerProblem.py

import pyomo.environ as pyo

model = pyo.AbstractModel()
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

def deer_block_rule(b, t):
    # variables
    b.f = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.d = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.b = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.hf = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.hd = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.hb = pyo.Var(initialize=20, within=pyo.PositiveReals)
    b.br = pyo.Var(initialize=1.5, within=pyo.PositiveReals)
    b.c = pyo.Var(initialize=500000, within=pyo.PositiveReals)

    #constraints
    m = b.model()
    b.f_bal = pyo.Constraint(expr=b.f == m.p1 * b.br * (m.p2 / 10.0 * b.f + m.p3 * b.d) - b.hf)
    b.d_bal = pyo.Constraint(expr=b.d == m.p4 * b.d + m.p5 / 2.0 * b.f - b.hd)
    b.b_bal = pyo.Constraint(expr=b.b == m.p6 * b.b + m.p5 / 2.0 * b.f - b.hb)
    b.food_cons = pyo.Constraint(expr=b.c == m.p7 * b.b + m.p8 * b.d + m.p9 * b.f)
    b.supply = pyo.Constraint(expr=b.c <= m.ps)
    b.birth = pyo.Constraint(expr=b.br == 1.1 + 0.8 * (m.ps - b.c) / m.ps)
    b.minbuck = pyo.Constraint(expr=b.b >= 1.0/5.0 * (0.4 * b.f + b.d))

model.db = pyo.Block(rule=deer_block_rule)

def obj_rule(m):
    return 10 * m.db.hb + m.db.hd + m.db.hf

model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

# create the ConcreteModel
instance = model.create_instance('DeerProblem.dat')
status = pyo.SolverFactory('ipopt').solve(instance)
pyo.assert_optimal_termination(status)
instance.pprint()
