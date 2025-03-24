from pyomo.environ import *

# Crear el modelo de optimización
model = ConcreteModel()

# Parámetros del problema
demand = 1263  # Demanda total del sistema en MW
units = ["G1", "G2", "G3", "G4", "G5", "G6"]

# Datos de la tabla 4 (sin zonas prohibidas)
data = {
    "G1": {"P_min": 100, "P_max": 500, "a": 7.0e-3, "b": 7.0, "c": 240, "UR": 80, "DR": 120},
    "G2": {"P_min": 50, "P_max": 200, "a": 9.5e-3, "b": 10.0, "c": 200, "UR": 50, "DR": 90},
    "G3": {"P_min": 80, "P_max": 300, "a": 9.0e-3, "b": 8.5, "c": 220, "UR": 65, "DR": 100},
    "G4": {"P_min": 50, "P_max": 150, "a": 9.0e-3, "b": 11.0, "c": 200, "UR": 50, "DR": 90},
    "G5": {"P_min": 50, "P_max": 200, "a": 8.0e-3, "b": 10.5, "c": 220, "UR": 50, "DR": 90},
    "G6": {"P_min": 50, "P_max": 120, "a": 7.5e-3, "b": 12.0, "c": 190, "UR": 50, "DR": 90},
}

# Variables de decisión: Potencia generada por cada unidad
model.P = Var(units, domain=NonNegativeReals)

# Función objetivo: minimizar el costo total de generación
def cost_function(model):
    return sum(data[g]["a"] * model.P[g] ** 2 + data[g]["b"] * model.P[g] + data[g]["c"] for g in units)
model.obj = Objective(rule=cost_function, sense=minimize)

# Restricción de balance de potencia
def balance_constraint(model):
    return sum(model.P[g] for g in units) == demand
model.balance = Constraint(rule=balance_constraint)

# Restricciones de límites de generación
model.gen_limits = ConstraintList()
for g in units:
    model.gen_limits.add(data[g]["P_min"] <= model.P[g])
    model.gen_limits.add(model.P[g] <= data[g]["P_max"])

# Restricciones de rampas de subida y bajada
# Suponiendo que la generación previa era el punto medio entre P_min y P_max
model.ramp_limits = ConstraintList()
for g in units:
    P_prev = (data[g]["P_min"] + data[g]["P_max"]) / 2  # Estado inicial aproximado
    model.ramp_limits.add(model.P[g] - P_prev <= data[g]["UR"])  # Límite de subida
    model.ramp_limits.add(P_prev - model.P[g] <= data[g]["DR"])  # Límite de bajada

# Resolver el modelo con IPOPT
solver = SolverFactory("ipopt")
results = solver.solve(model, tee=True)

# Mostrar los resultados
print("\nResultados del despacho económico de carga:")
for g in units:
    print(f"{g}: {model.P[g]():.2f} MW")
print(f"Costo total: {model.obj():.2f} $/h")
