import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Extrados
def extrados(x):
    return 0.001808914648*x**2 - 0.1314763917*x + 17.33694558

x = np.linspace(-35, 115, 100)
y_extrados = extrados(x)

# Indications extrados
def indication_extrados(x):
    return -0.002120007284*x**2 + 0.01039951273*x + 275.5911374

x_ind = np.linspace(-34, 113, 100)
z_ind = indication_extrados(x_ind)
y_ind = np.zeros_like(x_ind)  # y = 0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, np.zeros_like(x), y_extrados, label='Extrados')
ax.plot(x_ind, y_ind, z_ind, label='Indications Extrados', color='red')
ax.view_init(elev=20, azim=-60)
plt.show()
