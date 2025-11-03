import pandas as pd
from pyomo.environ import *

# Names in data:
# "Showroom space (100 m2)": "Showroom",
# "Population cat 1 (1000s)": "Pop_cat1",
# "Population cat 2 (1000s)": "Pop_cat2",
# "Enquiries Alpha model (100s)": "Enq_alpha",
# "Enquiries Beta model (100s)": "Enq_beta",
# "Alpha sales (1000s)": "Sales_alpha",
# "Beta sales (1000s)": "Sales_beta",
# "Profit (millions)": "Profit"

# --------------------
# 1. Leer datos del CSV
# --------------------
df = pd.read_csv("garage_data.csv")
df.index = df.index + 1  # DMU indices from 1 to N

# --------------------
# 2. Construir x_data e y_data
# --------------------
input_vars = ['Staff', 'Showroom', 'Pop_cat1', 'Pop_cat2', 'Enq_alpha', 'Enq_beta']
output_vars = ['Sales_alpha', 'Sales_beta', 'Profit']

x_data = {(col.lower(), dmu): df.loc[dmu, col] for col in input_vars for dmu in df.index}
y_data = {(col.lower(), dmu): df.loc[dmu, col] for col in output_vars for dmu in df.index}

# --------------------
# 3. Definición del modelo DEA para una DMU
# --------------------
def build_dea_model(target_dmu):
    model = ConcreteModel()

    model.I = Set(initialize=[i.lower() for i in input_vars])
    model.R = Set(initialize=[r.lower() for r in output_vars])
    model.J = Set(initialize=df.index.tolist())

    model.u = Var(model.R, domain=NonNegativeReals)
    model.v = Var(model.I, domain=NonNegativeReals)

    epsilon = 1e-4
    model.obj = Objective(
        expr=sum(model.u[r] * y_data[r, target_dmu] for r in model.R),
        sense=maximize
    )

    model.norm_constraint = Constraint(
        expr=sum(model.v[i] * x_data[i, target_dmu] for i in model.I) == 1
    )

    def efficiency_rule(model, j):
        return sum(model.u[r] * y_data[r, j] for r in model.R) <= \
               sum(model.v[i] * x_data[i, j] for i in model.I)
    model.efficiency_constraints = Constraint(model.J, rule=efficiency_rule)

    model.min_weight_u = Constraint(model.R, rule=lambda m, r: m.u[r] >= epsilon)
    model.min_weight_v = Constraint(model.I, rule=lambda m, i: m.v[i] >= epsilon)

    return model

# --------------------
# 4. Evaluar todas las DMUs
# --------------------
results = []
weights = []

solver = SolverFactory("glpk")

for dmu in df.index:
    model = build_dea_model(target_dmu=dmu)
    try:
        solver.solve(model)
    except Exception as e:
        print(f"\n\n\n\nError al resolver el modelo para DMU {dmu}")
        for i in model.I:
            if (i, dmu) not in x_data:
                print(f"Falta x_data para input {i}, DMU {dmu}")
        for r in model.R:
            if (r, dmu) not in y_data:
                print(f"Falta y_data para output {r}, DMU {dmu}\n\n\n")
        raise e

    eff = value(model.obj)
    u_vals = {r: value(model.u[r]) for r in model.R}
    v_vals = {i: value(model.v[i]) for i in model.I}

    results.append({
        "DMU": dmu,
        "Garage": df.loc[dmu, "Garage"] if "Garage" in df.columns else f"Garage_{dmu}",
        "Efficiency": eff,
        "Efficient": "Yes" if abs(eff - 1.0) < 1e-4 else "No"
    })
    weights.append({
        "DMU": dmu,
        "Garage": df.loc[dmu, "Garage"] if "Garage" in df.columns else f"Garage_{dmu}",
        **u_vals, **v_vals
    })

# --------------------
# 5. Resultados
# --------------------
eff_df = pd.DataFrame(results)
weights_df = pd.DataFrame(weights)

# Guardar resultados
eff_df.to_csv("efficiencies.csv", index=False)
weights_df.to_csv("weights.csv", index=False)

# Mostrar resumen ordenado
print("\n--- Ranking de eficiencia ---")
print(eff_df.sort_values("Efficiency", ascending=False).to_string(index=False))
