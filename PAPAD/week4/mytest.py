import json
import pyomo.environ as pyo
from warehouse_model import create_wl_model

model = pyo.ConcreteModel()

p = {1:1, 2:4, 3:9}

model = pyo.ConcreteModel()

p = {1:1, 2:4, 3:9}

model.A = pyo.Set(initialize=[1,2,3])

model.p = pyo.Param(model.A, initialize=p, mutable=True)

model.x = pyo.Var(model.A, within=pyo.NonNegativeReals)

model.p[2] = 4.2

