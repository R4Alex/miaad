import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.u = pyo.Var(initialize=2.0)


# Unexpected expression instead of value
a = model.u - 1

print(a)
# "u - 1"

print(type(a))
# <class 'pyomo.core.expr.numeric_expr.SumExpression'>

b = pyo.value(model.u) - 1
# correct way to access the value

print(b)
# 1.0

print(type(b))
# <class 'float'>
