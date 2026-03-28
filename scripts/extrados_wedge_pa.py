import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t = np.linspace(-30, 110, 1000)

x = t
y = -0.003609426882*t**2 + 0.3901521821*t + 19.70318543
z = -0.005488853532*t**2 + 0.4063539903*t + 322.5637160

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Courbe 3D', color='blue')
ax.view_init(elev=20, azim=-60)
plt.show()
