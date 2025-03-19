import sympy

# Definir la variable y la función logística
x, x0 = sympy.symbols('x x0')
f_x = 1 / (1 + sympy.exp(-(x - x0)))

# Calcular la primera derivada
f_prime = sympy.diff(f_x, x)
f_prime = sympy.simplify(f_prime)

# Calcular la segunda derivada
f_two_prime = sympy.diff(f_prime, x)
f_two_prime = sympy.simplify(f_two_prime)

# Calcular la tercera derivada
f_three_prime = sympy.diff(f_two_prime, x)
f_three_prime = sympy.simplify(f_three_prime)

# Mostrar la derivada simplificada
print("\nPrimera Derivada:", f_prime)
print("\nSegunda Derivada:", f_two_prime)
print("\nTercera Derivada:", f_three_prime)
