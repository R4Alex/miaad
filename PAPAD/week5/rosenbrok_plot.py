import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir los parámetros
a = 1
b = 100

# Crear una malla de puntos en el dominio x e y
x = np.linspace(-2, 2, 400)
y = np.linspace(-1, 3, 400)
X, Y = np.meshgrid(x, y)

# Calcular la función de Rosenbrock
Z = (a - X)**2 + b * (Y - X**2)**2

# Crear la gráfica 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# Configurar etiquetas y título
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('f(X, Y)')
ax.set_title('Función de Rosenbrock')

# Mostrar la grafica
# plt.show()
plt.savefig("matplotlib.png") 