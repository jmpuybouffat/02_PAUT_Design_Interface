import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Surface extrados (mm)
def extrados(x):
    return 0.001808914648*x**2 - 0.1314763917*x + 17.33694558

# PA + wedge 55°
x = np.linspace(-35, 115, 100)
y = extrados(x)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, np.zeros_like(x), y, label='Extrados')
ax.view_init(elev=20, azim=-60)
plt.show()

3. Add + commit + push :

bash
git add scripts/extrados_wedge_pa.py
git commit -m "Add extrados wedge PA code"
git push origin main
