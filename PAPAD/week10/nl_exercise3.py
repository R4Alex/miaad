import pyomo.environ as pyo

# Create the model
model = pyo.ConcreteModel()

model.warehouses = pyo.Set(initialize=[1, 2])
model.locations = pyo.Set(initialize=[1, 2, 3])

# Parameters
model.capacity = pyo.Param(model.warehouses, initialize={1: 100, 2: 120})
model.demand = pyo.Param(model.locations, initialize={1: 80, 2: 70, 3: 60})

costs_penalty = {
    (1, 1): (4, 0.01),
    (1, 2): (6, 0.015),
    (1, 3): (9, 0.02),
    (2, 1): (5, 0.012),
    (2, 2): (4, 0.018),
    (2, 3): (7, 0.01)
}

model.costs_penalty = pyo.Param(model.warehouses, model.locations, initialize=costs_penalty, within=pyo.Any)

# Decision variable
# Use NonNegativeReals to acomplish no negative constraint
model.x = pyo.Var(model.warehouses, model.locations, domain=pyo.NonNegativeReals)


###################### Constraints

# Capacity Constraint (per warehouse)
def capacity_constraint_rule(model, warehouse):
    # Sum over all locations for the given warehouse
    capacity = sum(
        model.x[warehouse, location] for location in model.locations
    )
    return capacity <= model.capacity[warehouse]

# Sending mode.warehouses to the function, will be iterate over the set once per "warehouse"
model.capacity_constraint = pyo.Constraint(model.warehouses, rule=capacity_constraint_rule)



# Demand Constraint (per location)
def demand_constraint_rule(model, location):
    # Sum over all warehouses for the given location
    demand = sum(
        model.x[warehouse, location] for warehouse in model.warehouses
    )
    return demand >= model.demand[location]
model.demand_constraint = pyo.Constraint(model.locations, rule=demand_constraint_rule)


# Objective function
def objective_function(model):
    # Cost Penalty index 0 is the base cost and index 1 is the penalty coefficient
    # The sum consists in base cost + penalty * x^2
    return sum(
        model.x[warehouse, location] *
        (model.costs_penalty[warehouse, location][0] + 
        model.costs_penalty[warehouse, location][1] * model.x[warehouse, location]**2)
        for warehouse in model.warehouses for location in model.locations
    )


model.obj = pyo.Objective(rule=objective_function, sense=pyo.minimize)

# Resolve
solver = pyo.SolverFactory("ipopt")

# Solver and Check if the solver found a solution
result = solver.solve(model)
pyo.assert_optimal_termination(result)

# Showing results
print("Final Minimal Cost:", model.obj())
for warehouse in model.warehouses:
    for location in model.locations:
        value = pyo.value(model.x[warehouse, location])
        print(f"{warehouse} -> {location}: {value:.2f} unidades")
