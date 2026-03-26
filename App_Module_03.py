import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Library.byte_ndt_physics import calculate_beam_field, apply_db_mask

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Byte NDT - Conception Mécanique", layout="wide")

st.title("⚙️ Conception d'Outil de Scan - Turbine LSB 941")
st.markdown("---")

# --- PARAMÈTRES DANS LA BARRE LATÉRALE ---
st.sidebar.header("🛠️ Configuration du Test")

# Réglages pour votre monocristal 6mm 5MHz
L1 = st.sidebar.slider("Nombre d'éléments (1 = Monocristal)", 1, 12, 1)
probe_size = st.sidebar.number_input("Diamètre du cristal (mm)", value=6.0)
freq = st.sidebar.number_input("Fréquence (MHz)", value=5.0)
theta2 = st.sidebar.slider("Angle de réfraction souhaité (°)", 35, 70, 45)
Dt0 = st.sidebar.slider("Hauteur du sabot (Wedge Height) [mm]", 10.0, 40.0, 30.0)

# Profondeur de la Gorge n°1 (Z négatif pour le milieu de la pièce)
target_z = -27.15

# Calcul de l'Offset X pour Fusion 360 (Offset = |Z| * tan(theta))
offset_x = abs(target_z) * np.tan(np.radians(theta2))

st.sidebar.markdown("---")
st.sidebar.write(f"🎯 **Cible : {target_z} mm**")
st.sidebar.write(f"📏 **Offset de guidage : {offset_x:.2f} mm**")
st.sidebar.info("L'offset est la distance horizontale entre le centre de la sonde et la dent.")

# --- ZONE DE CALCUL (ROI) ---
# On définit une grille qui va de la surface (0) à l'intérieur de la pièce (-50mm)
ROI = {
    'xs': np.linspace(-40, 40, 160),
    'zs': np.linspace(0, 50, 100) # Le moteur utilise des distances positives en interne
}

# Matériau Maquette (Vitesse Plastique ~2300 m/s)
mat = [1.0, 1480, 1.2, 2300, 2300, 'p']

# --- BOUTON DE SIMULATION ---
if st.button("🚀 Lancer la Simulation (Cible -27.15 mm)"):
    with st.spinner("Calcul du faisceau en cours..."):
        # Appel au moteur Sommerfeld
        vmag = calculate_beam_field(L1, 1, probe_size, probe_size, freq, mat, Dt0, theta2, 0, abs(target_z), ROI)
        heatmap = apply_db_mask(vmag)
        
        # --- AFFICHAGE GRAPHIQUE ---
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # On affiche avec Z négatif pour la métrologie
        # Extent : [Xmin, Xmax, Zmax(fond), Zmin(surface)]
        im = ax.imshow(heatmap, extent=[-40, 40, -50, 0], cmap='jet', aspect='auto')
        
        # Ligne de la Gorge n°1 à -27.15 mm
        ax.axhline(y=target_z, color='gold', linestyle='--', linewidth=2, label=f"Gorge n°1 ({target_z}mm)")
        
        # Point d'impact théorique
        ax.scatter([0], [target_z], color='white', s=100, marker='X', label="Impact Cible")

        ax.set_xlabel("Position Latérale X (mm)")
        ax.set_ylabel("Profondeur Z (mm)")
        ax.set_title(f"Faisceau Monocristal {probe_size}mm à {theta2}°")
        ax.legend()
        plt.colorbar(im, label="Intensité Relative (dB)")
        st.pyplot(fig)

        # --- GÉNÉRATION DES COORDONNÉES POUR FUSION 360 ---
        st.divider()
        st.subheader("📈 Export de Courbe pour Fusion 360 & Micromoteur")
        
        # Génération d'une trajectoire sur 50 mm de course de l'aube
        x_aube = np.linspace(-25, 25, 25)
        
        df_coords = pd.DataFrame({
            'Course_Aube_X': x_aube,
            'Position_Sonde_X': x_aube - offset_x,
            'Hauteur_Appui_Z': [0.0] * len(x_aube), # Surface de contact
            'Profondeur_Dent_Z': [target_z] * len(x_aube)
        })
        
        st.write("Tableau de positionnement (X sonde) pour maintenir le tir à 45° sur la dent :")
        st.dataframe(df_coords.style.format("{:.2f}"))
        
        # Export CSV
        csv = df_coords.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les points pour Fusion 360",
            data=csv,
            file_name="trajectoire_scan_LSB941.csv",
            mime="text/csv",
        )
        st.success("Données prêtes pour importation Spline dans Fusion 360.")
