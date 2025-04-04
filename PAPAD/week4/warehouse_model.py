import pyomo.environ as pyo
def create_wl_model(data, P):
    # create the model
    model = pyo.ConcreteModel(name="(WL)")
    model.WH = data["WH"]
    model.CUST = data["CUST"]
    model.dist = data["dist"]
    model.P = P
    model.x = pyo.Var(model.WH, model.CUST, bounds=(0, 1))
    model.y = pyo.Var(model.WH, within=pyo.Binary)

    def obj_rule(m):
        return sum(m.dist[w][c]*m.x[w,c] for w in m.WH for c in m.CUST)
    model.obj = pyo.Objective(rule=obj_rule)

    def one_per_cust_rule(m, c):
        return sum(m.x[w,c] for w in m.WH) == 1
    model.one_per_cust = pyo.Constraint(model.CUST, rule=one_per_cust_rule)

    def warehouse_active_rule(m, w, c):
        return m.x[w,c] <= m.y[w]
    model.warehouse_active = pyo.Constraint(model.WH, model.CUST, rule=warehouse_active_rule)

    def num_warehouse_rule(m):
        return sum(m.y[w] for w in m.WH) <= m.P
    model.num_warehouses = pyo.Constraint(rule=num_warehouse_rule)

    return model
