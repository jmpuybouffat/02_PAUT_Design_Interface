import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t = np.linspace(-50, 150, 1000)

x = t
y = 0.001808914648*t**2 - 0.1314763917*t + 17.33694558
z = -0.003862179289*t**2 + 0.1391544251*t + 276.4370567

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Courbe 3D', color='blue')
ax.view_init(elev=20, azim=-60)
plt.show()
