import json
import pyomo.environ as pyo
from warehouse_model import create_wl_model

# cargar los datos desde un archivo JSON
with open("warehouse_data.json", "r") as fd:
    data = json.load(fd)

# llamar a la funcion para crear el modelo
model = create_wl_model(data, P=2)

# Resolver el modelo
solver = pyo.SolverFactory("glpk")
solver.solve(model)

# ver la solucion
model.y.pprint()
