import pyomo.environ as pyo
import pandas as pd

def get_nutritional_requirements_from_user():
    print("=== Input the nutrional requirements ===\n")
    requirements = {
        "Calorias": float(input("Calories: ")),
        "Proteina": float(input("Protein: ")),
        "Fibra": float(input("Fiber: ")),
        "Carbohidratos": float(input("Carbohydrates: ")),
        "Vitamina_A": float(input("Vitamin A: ")),
        "Vitamina_C": float(input("Vitamin C: ")),
        "Vitamina_D": float(input("Vitamin D: ")),
        "Vitamina_K": float(input("Vitamin K: ")),
    }
    return requirements

def get_fixed_nutritional_requirements():
    print("\nFixed Initial Plan\n")
    return {
        "Calorias": 2000,
        "Proteina": 50,
        "Fibra": 30,
        "Carbohidratos": 250,
        "Vitamina_A": 700,
        "Vitamina_C": 60,
        "Vitamina_D": 15,
        "Vitamina_K": 90,
    }

def get_deficit_requirements():
    print("\nDeficit Plan\n")
    return {
        "Calorias": 1500,
        "Proteina": 60,
        "Fibra": 25,
        "Carbohidratos": 200,
        "Vitamina_A": 700,
        "Vitamina_C": 80,
        "Vitamina_D": 15,
        "Vitamina_K": 90,
    }

def get_athlete_requirements():
    print("\nAthlete Plan\n")
    return {
        "Calorias": 3000,
        "Proteina": 100,
        "Fibra": 35,
        "Carbohidratos": 400,
        "Vitamina_A": 900,
        "Vitamina_C": 100,
        "Vitamina_D": 20,
        "Vitamina_K": 120,
    }


# Create the model
model = pyo.ConcreteModel()

# Load Data
requirements = get_nutritional_requirements_from_user()
# requirements = get_fixed_nutritional_requirements()
# requirements = get_deficit_requirements()
# requirements = get_athlete_requirements()


# Load nutrients data
foods_nutrients = pd.read_csv("dieta_extendida_nutrientes.csv")
food_types = foods_nutrients['Alimento'].tolist()
food_costs = dict(zip(food_types, foods_nutrients['Costo']))
# Getting the columns names, in other words the nutrients as calories
nutrients_list = foods_nutrients.columns.to_list()
# Populate a dict where we can get how many nutrionts have each food type
nutrient_content = {}
for nutrient in nutrients_list:
    nutrient_content[nutrient] = dict(zip(food_types, foods_nutrients[nutrient]))


# Parameters
nutrients_list.remove("Alimento")
nutrients_list.remove("Costo")
model.food_types = pyo.Set(initialize=food_types)
model.Nutrients = pyo.Set(initialize=nutrients_list)
model.alpha = pyo.Param(initialize=10)
model.epsilon = pyo.Param(initialize=0.001)

# Decision variables and parameters
model.x = pyo.Var(model.food_types, domain=pyo.NonNegativeReals)

# Constrain, check the values if each nutrient in each food type, for example in ("Alimento_1") each nutrient as "Calories"
def nutrient_constraint_rule(model, nutrient):
    return sum(nutrient_content[nutrient][food_type] * model.x[food_type] for food_type in model.food_types) >= requirements[nutrient]

model.nutrient_constraint = pyo.Constraint(model.Nutrients, rule=nutrient_constraint_rule)

def objective_rule(model):
    # Separate the cost term and the penalty term sumatories
    cost_term = sum(food_costs[food_type] * model.x[food_type] for food_type in model.food_types)
    penalty_term = sum(1.0 / (sum(nutrient_content[nutrient][food_type] * model.x[food_type] for food_type in model.food_types) + model.epsilon) for nutrient in model.Nutrients)
    return cost_term + model.alpha * penalty_term

model.obj = pyo.Objective(rule=objective_rule, sense=pyo.minimize)

# Resolve
solver = pyo.SolverFactory("ipopt")

# Solver and Check if the solver found a solution
# result = solver.solve(model, tee=True)
result = solver.solve(model)
pyo.assert_optimal_termination(result)

# Showing results
print("Diet Cost:", model.obj())
for food_type in model.food_types:
        value = pyo.value(model.x[food_type])
        if value > 1e-4:
            print(f"{food_type}: {value:.4f}")

