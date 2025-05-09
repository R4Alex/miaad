# wl_concrete_script.py
# Solve an instance of the warehouse location problem

# Import Pyomo environment and model
import pyomo.environ as pyo
from wl_concrete import create_warehouse_model

# Establish the data for this model (this could also be
# imported using other Python packages)
N = ['Harlingen', 'Memphis', 'Ashland']
M = ['NYC', 'LA', 'Chicago', 'Houston']
P=2
d = {('Harlingen', 'NYC'): 1956, \
 ('Harlingen', 'LA'): 1606, \
 ('Harlingen', 'Chicago'): 1410, \
 ('Harlingen', 'Houston'): 330, \
 ('Memphis', 'NYC'): 1096, \
 ('Memphis', 'LA'): 1792, \
 ('Memphis', 'Chicago'): 531, \
 ('Memphis', 'Houston'): 567, \
 ('Ashland', 'NYC'): 485, \
 ('Ashland', 'LA'): 2322, \
 ('Ashland', 'Chicago'): 324, \
 ('Ashland', 'Houston'): 1236 }

# Create the Pyomo model
model = create_warehouse_model(N, M, d, P)

# Create the solver interface and solve the model
solver = pyo.SolverFactory('glpk')
res = solver.solve(model)
model.y.pprint() # Print the optimal warehouse locations
