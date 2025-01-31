from pyomo.environ import *

# Crear un modelo simple
model = ConcreteModel()
model.x = Var(bounds=(0, 10))
model.y = Var(bounds=(0, 10))
model.obj = Objective(expr=model.x + model.y, sense=minimize)
model.con = Constraint(expr=model.x + 2 * model.y >= 10)

# Resolver con GLPK
solver = SolverFactory('glpk')
resultado = solver.solve(model)

# Mostrar resultados
if (resultado.solver.status == SolverStatus.ok):
    print("Solución encontrada:")
    print("x =", model.x.value)
    print("y =", model.y.value)
else:
    print("Error al resolver el modelo")
