import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st

# Paramètres
sector_start = 35
sector_end = 70
skew_start = -30
skew_end = 30
pas = 1.0
focal_point = (-27.16, 0, 0)  # x, y, z

# Calcul du faisceau
angles_sector = np.arange(sector_start, sector_end + pas, pas)
angles_skew = np.arange(skew_start, skew_end + pas, pas)
X, Y = np.meshgrid(angles_sector, angles_skew)
Z = np.sin(np.sqrt(X**2 + Y**2))  # Remplacer par calcul réel

# Affichage Streamlit
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_title('Faisceau 3D (sectorial + skew)')
st.pyplot(fig)
plt.savefig('faisceau_3d.png')
