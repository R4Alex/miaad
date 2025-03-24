# DeerProblem using blocks
import pyomo.environ as pyo


model = pyo.AbstractModel()

# Params section
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


def block_define(mb):
    # mb: main_block
    # Decision variables
    mb.f = pyo.Var(initialize = 20, within=pyo.PositiveReals)
    mb.d = pyo.Var(initialize = 20, within=pyo.PositiveReals)
    mb.b = pyo.Var(initialize = 20, within=pyo.PositiveReals)
    mb.hf = pyo.Var(initialize = 20, within=pyo.PositiveReals)
    mb.hd = pyo.Var(initialize = 20, within=pyo.PositiveReals)
    mb.hb = pyo.Var(initialize = 20, within=pyo.PositiveReals)
    mb.br = pyo.Var(initialize=1.5, within=pyo.PositiveReals)
    mb.c = pyo.Var(initialize=500000, within=pyo.PositiveReals)

    # Constrains
    # Get parent model
    m = mb.model()
    mb.f_bal_rule = pyo.Constraint(expr=mb.f == m.p1 * mb.br * (m.p2/10.0 * mb.f + m.p3 * mb.d) - mb.hf)
    mb.d_bal_rule = pyo.Constraint(expr=mb.d == m.p4 * mb.d + m.p5/2.0 * mb.f - mb.hd)
    mb.b_bal_rule = pyo.Constraint(expr=mb.b == m.p6 * mb.b + m.p5/2.0 * mb.f - mb.hb)
    mb.food_cons_rule = pyo.Constraint(expr=mb.c == m.p7 * mb.b + m.p8 * mb.d + m.p9 * mb.f)
    mb.supply_rule = pyo.Constraint(expr=mb.c <= m.ps)
    mb.birth_rule = pyo.Constraint(expr=mb.br == 1.1 + 0.8 * (m.ps - mb.c) / m.ps)
    mb.minbuck_rule = pyo.Constraint(expr=mb.b >= 1.0 / 5.0 * (0.4 * mb.f + mb.d))

##################################################

# create Mainblock in the model
model.main_block = pyo.Block(rule=block_define)

# objetive rule
def obj_rule(m):
    return 10 * m.main_block.hb + m.main_block.hd + m.main_block.hf
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

# create the ConcreteModel
instance = model.create_instance("DeerProblem.dat")
status = pyo.SolverFactory("ipopt").solve(instance)
pyo.assert_optimal_termination(status)
instance.pprint()
