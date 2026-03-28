import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Surface intrados (mm)
def intrados(x):
    return -0.001808914648*x**2 + 0.1314763917*x - 17.33694558

# PA + wedge 55°
x = np.linspace(-35, 115, 100)
y = intrados(x)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, np.zeros_like(x), y, label='Intrados')
ax.view_init(elev=20, azim=-60)
plt.show()
