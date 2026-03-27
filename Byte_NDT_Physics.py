mport. numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Paramètres
sector_start = 35
sector_end = 70
skew_start = -30
skew_end = 30
pas = 1.0
focal_point = (-27.16, 0, 0)  # x, y, z

# Calcul du faisceau (à compléter avec ta lib/méthode)
# Exemple bidon :
angles_sector = np.arange(sector_start, sector_end + pas, pas)
angles_skew = np.arange(skew_start, skew_end + pas, pas)

# Propagation 3D (exemple simplifié)
X, Y = np.meshgrid(angles_sector, angles_skew)
Z = np.sin(np.sqrt(X**2 + Y**2))  # Remplacer par calcul réel

# Affichage
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_title('Faisceau 3D (sectorial + skew)')
plt.show()

# Sauvegarde (ex : image)
