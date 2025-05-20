import pandas as pd
from pyomo.environ import *

def optimize_model(rutas):
    capacidad_centro = pd.read_csv(rutas["Centros CSV"])
    Demanda = pd.read_csv(rutas["Clientes CSV"])
    costos = pd.read_csv(rutas["Costos CSV"])
    planta_capacidad = pd.read_csv(rutas["Plantas CSV"])
    productos = pd.read_csv(rutas["Productos CSV"])

    #Extraemos datos
    plantas = planta_capacidad["Planta"].unique().tolist()
    print("Loading Plantas:", plantas)

    centros = capacidad_centro["Centro"].unique().tolist()
    print("Loading Centros:", centros)

    clientes = Demanda["Cliente"].unique().tolist()
    print("Loading Clientes:", clientes)

    productos = productos["Producto"].unique().tolist()
    print("Loading Productos:", productos)

    model = ConcreteModel()

    model.P = Set(initialize=plantas)
    model.C = Set(initialize=centros)
    model.J = Set(initialize=clientes)
    model.K = Set(initialize=productos)

    Capacidad_Produccion_data = planta_capacidad.set_index(["Planta", "Producto"])["Capacidad_Produccion"].to_dict()
    model.capacidad_produccion = Param(model.P, model.K, initialize=Capacidad_Produccion_data)

    costo_produccion_data = planta_capacidad.set_index(["Planta", "Producto"])["Costo_Produccion"].to_dict()
    model.costo_produccion = Param(model.P, model.K, initialize=costo_produccion_data)

    capacidad_almacenamiento_data = capacidad_centro.set_index(["Centro", "Producto"])["Capacidad_Almacenamiento"].to_dict()
    model.capacidad_almacenamiento = Param(model.C, model.K, initialize=capacidad_almacenamiento_data)

    demanda_data = Demanda.set_index(["Cliente", "Producto"])["Demanda"].to_dict()
    model.demanda = Param(model.J, model.K, initialize=demanda_data)

    costo_transporte_pc_data = costos.set_index(["Planta", "Centro", "Producto", "Cliente"])["Costo_Plant_Centro"]\
        .groupby(level=["Planta", "Centro", "Producto"]).first().to_dict() #agrupamos para evitar duplicados
    model.costo_transporte_pc = Param(model.P, model.C, model.K, initialize=costo_transporte_pc_data, default=0) #Agregamos default 0? Para valores que no existan

    costo_transporte_cc_data = costos.set_index(["Planta", "Centro", "Producto", "Cliente"])["Costo_Centro_Cliente"]\
        .groupby(level=["Centro", "Cliente", "Producto"]).first().to_dict()
    model.costo_transporte_cc = Param(model.C, model.J, model.K, initialize=costo_transporte_cc_data, default=0)

    #Variables
    model.x = Var(model.P, model.C, model.K, domain=NonNegativeReals)
    model.y = Var(model.C, model.J, model.K, domain=NonNegativeReals)

    #Funcion Objetivo
    def funcion_objetivo(model):
        #Costo_Produccion = sum(model.Costo_Produccion[p, k] * model.x[p, c, k] for p in model.P for c in model.C for k in model.K)
        costo_produccion = sum(model.costo_produccion[p, k] * sum(model.x[p, c, k] for c in model.C) 
                            for k in model.K 
                            for p in model.P)

        costo_transporte_pc = sum(model.costo_transporte_pc[p, c, k] * model.x[p, c, k] 
                                for p in model.P 
                                for c in model.C 
                                for k in model.K)
        
        costo_transporte_cc = sum(model.costo_transporte_cc[c, j, k] * model.y[c, j, k] 
                                for c in model.C 
                                for j in model.J 
                                for k in model.K)
        
        return costo_produccion + costo_transporte_pc + costo_transporte_cc

    model.objective = Objective(rule=funcion_objetivo, sense=minimize)

    #Restricciones
    def restriccion_demanda(model, j, k):
        return sum(model.y[c, j, k] for c in model.C) == model.demanda[j, k]
    model.restriccion_demanda = Constraint(model.J, model.K, rule=restriccion_demanda)

    def restriccion_balance(model, c, k):
        return sum(model.x[p, c, k] for p in model.P) == sum(model.y[c, j, k] for j in model.J)
    model.restriccion_balance = Constraint(model.C, model.K, rule=restriccion_balance)

    def restriccion_capacidad_produccion(model, p, k):
        return sum(model.x[p, c, k] for c in model.C) <= model.capacidad_produccion[p, k]
    model.restriccion_capacidad_produccion = Constraint(model.P, model.K, rule=restriccion_capacidad_produccion)

    def restriccion_almacenamiento(model, c, k):
        return sum(model.y[c, j, k] for j in model.J) <= model.capacidad_almacenamiento[c, k]
    model.restriccion_almacenamiento = Constraint(model.C, model.K, rule=restriccion_almacenamiento)

    solver = SolverFactory("glpk")
    solution = solver.solve(model)

    if solution.solver.status == SolverStatus.ok and solution.solver.termination_condition == TerminationCondition.optimal:
        costo = model.objective()
        print(f"Costo = {costo:.2f}")
        plant_to_center = []
        center_to_plant = []

        # Plant_to_center
        for p in model.P:
            for c in model.C:
                for k in model.K:
                    if model.x[p, c, k].value > 0:
                        # value = f"Planta {p} a Centro {c}, Producto {k}: {model.x[p, c, k].value:.2f}"
                        value = f"{k}: {p} -> {c} {model.x[p, c, k].value:.2f}"
                        print(value)
                        plant_to_center.append(value)

        # center_to_plant
        for c in model.C:
            for j in model.J:
                for k in model.K:
                    if model.y[c, j, k].value > 0:  
                        # value = f"Centro {c} a Cliente {j}, Producto {k}: {model.y[c, j, k].value:.2f}"
                        value = f"{k}: {c} -> {j} {model.y[c, j, k].value:.2f}"
                        print(value)
                        center_to_plant.append(value)
        
        return costo, plant_to_center, center_to_plant, model
    else:
        print("Sin solucion optima")
