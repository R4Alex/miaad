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
    mb.f_bal_rule = pyo.Constraint(expr=mb.f == mb.p1 * mb.br * (mb.p2/10.0*mb.f + mb.p3*mb.d) - mb.hf)
    mb.d_bal_rule = pyo.Constraint(expr=mb.d == mb.p4*mb.d + mb.p5/2.0*mb.f - mb.hd)
    mb.b_bal_rule = pyo.Constraint(expr=mb.b == mb.p6*mb.b + mb.p5/2.0*mb.f - mb.hb)
    mb.food_cons_rule = pyo.Constraint(expr=mb.c == mb.p7*mb.b + mb.p8*mb.d + mb.p9*mb.f)
    mb.supply_rule = pyo.Constraint(expr=mb.c <= mb.ps)
    mb.birth_rule = pyo.Constraint(expr=mb.br == 1.1 + 0.8*(mb.ps - mb.c)/mb.ps)
    mb.minbuck_rule = pyo.Constraint(expr=mb.b >= 1.0/5.0*(0.4*mb.f + mb.d))

##################################################
model.main_block = pyo.Block(rule=block_define)

def obj_rule(m):
    return 10 * m.main_block.hb + m.main_block.hd + m.main_block.hf
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)



# create the ConcreteModel
instance = model.create_instance("DeerProblem.dat")
status = pyo.SolverFactory("ipopt").solve(instance)
pyo.assert_optimal_termination(status)
instance.pprint()
