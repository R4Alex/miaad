import json
import pyomo.environ as pyo
from warehouse_model import create_wl_model
import matplotlib.pyplot as plt

# load the data from a json file
with open("warehouse_data.json", "r") as fd:
    data = json.load(fd)

# call function to create a model
model = create_wl_model(data, P=2)
model.integer_cuts = pyo.ConstraintList()
objective_values = list()
done = False

while not done:
    # solver the model
    solver = pyo.SolverFactory("glpk")
    results = solver.solve(model)
    term_cond = results.solver.termination_condition
    print('')
    print("--- Solver status: {0} ---".format(term_cond))
    if pyo.check_optimal_termination(results):
        #look at the solution
        print("Optimal Obj. Value = {0}".format(pyo.value(model.obj)))
        objective_values.append(pyo.value(model.obj))
        model.y.pprint()
        # create new integer cut to exclude this solution
        WH_True = [i for i in model.WH if pyo.value(model.y[i]) > 0.5]
        WH_False = [i for i in model.WH if pyo.value(model.y[i]) < 0.5]
        expr1 = sum(model.y[i] for i in WH_True)
        expr2 = sum(model.y[i] for i in WH_False)
        model.integer_cuts.add(sum(model.y[i] for i in WH_True) - sum(model.y[i] for i in WH_False) <= len(WH_True)-1)
    else:
        done = True

x = range(1, len(objective_values)+1)
plt.bar(x, objective_values, align="center")
plt.gca().set_xticks(x)
plt.xlabel("Solution Number")
plt.ylabel("Optimal Obj. Value")
plt.savefig("WarehouseCuts.pdf")
