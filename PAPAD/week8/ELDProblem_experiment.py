import pyomo.environ as pyo
import pandas as pd

# Create the model
model = pyo.ConcreteModel()

# Decision variables
model.g1_production = pyo.Var(within=pyo.NonNegativeReals)
model.g2_production = pyo.Var(within=pyo.NonNegativeReals)
model.g3_production = pyo.Var(within=pyo.NonNegativeReals)
model.g4_production = pyo.Var(within=pyo.NonNegativeReals)
model.g5_production = pyo.Var(within=pyo.NonNegativeReals)
model.g6_production = pyo.Var(within=pyo.NonNegativeReals)

# Parameters
demand = 1263

def create_block(model, g_row):
    block = pyo.Block(model)
    model.block.P_max = g_row["P_max"]
    model.block.ai = g_row["ai"]
    model.block.bi = g_row["bi"]
    model.block.ci = g_row["ci"]
    model.block.ur = g_row["dr"]
    model.block.pi = g_row["pi"]
    model.block.p_zone = g_row["p_zone"]

# Load information
table_data = pd.read_csv("ELDProblem_data.csv")




for _, g_row in table_data.iterrows():
    pass



