import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Library.byte_ndt_physics import calculate_beam_field, apply_db_mask

st.set_page_config(page_title="Byte NDT - Guidage Mécanique LSB 941", layout="wide")

st.title("⚙️ Conception d'Outil de Scan - Turbine LSB 941")

# --- SIDEBAR : CONFIGURATION MONOCRISTAL ---
st.sidebar.header("🛠️ Paramètres du Test (Maquette)")
L1 = st.sidebar.slider("Nombre d'éléments (1 pour monocristal)", 1, 12, 1)
probe_size = st.sidebar.slider("Diamètre du cristal (mm)", 2.0, 20.0, 6.0)
freq = st.sidebar.slider("Fréquence (MHz)", 1.0, 10.0, 5.0)
theta2 = st.sidebar.slider("Angle de réfraction souhaité (°)", 35, 70, 45)
Dt0 = st.sidebar.slider("Hauteur du sabot (Wedge Height) [mm]", 10.0, 40.0, 30.0)

# --- CALCUL DE LA GÉOMÉTRIE DE GUIDAGE ---
target_z = 27.5  # Profondeur de la gorge n°1
# Calcul de l'offset X nécessaire pour que le tir à 45° frappe à 27.5mm
# Offset = Z * tan(theta)
offset_x = target_z * np.tan(np.radians(theta2))

st.sidebar.markdown("---")
st.sidebar.write(f"📏 **Offset de scan calculé : {offset_x:.2f} mm**")
st.sidebar.info("C'est la distance entre le centre de la sonde et la dent projetée verticalement.")

# --- ZONE D'INTÉRÊT (ROI) ---
ROI = {
    'xs': np.linspace(-30, 30, 150),
    'zs': np.linspace(10, 50, 150)
}

# Matériau (Maquette PLA/ABS ~2300 m/s)
mat = [1.0, 1480, 1.2, 2300, 2300, 'p']

if st.button("🚀 Simuler le faisceau à 45°"):
    vmag = calculate_beam_field(L1, 1, probe_size, probe_size, freq, mat, Dt0, theta2, 0, target_z, ROI)
    heatmap = apply_db_mask(vmag)
    
    # --- AFFICHAGE GRAPHIQUE ---
    fig, ax = plt.subplots(figsize=(10, 7))
    # Inversion pour avoir Z vers le bas
    im = ax.imshow(heatmap, extent=[-30, 30, 50, 10], cmap='jet', aspect='auto')
    
    # Ligne horizontale de la Gorge n°1
    ax.axhline(y=target_z, color='gold', linestyle='--', linewidth=2, label="Gorge n°1 (-27.5mm)")
    
    # Marqueur du point d'impact idéal
    ax.scatter([0], [target_z], color='white', s=100, marker='X', label="Cible")

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Profondeur Z (mm)")
    ax.set_title(f"Faisceau Monocristal 6mm à {theta2}°")
    ax.legend()
    plt.colorbar(im, label="Échelle dB")
    st.pyplot(fig)

    # --- GÉNÉRATION DE LA COURBE POUR FUSION 360 ---
    st.subheader("📈 Coordonnées de la rampe de guidage (Export Fusion 360)")
    
    # On génère une courbe de mouvement sur 40mm de large
    x_scan = np.linspace(-20, 20, 20)
    # Pour Fusion, on donne les positions réelles de la sonde
    df_coords = pd.DataFrame({
        'Position_Moteur_X': x_scan,
        'Position_Sonde_Z': [Dt0] * len(x_scan),
        'Cible_Gorge_X': x_scan + offset_x
    })
    
    st.write("Utilisez ces points pour dessiner la rainure dans votre esquisse Fusion 360.")
    st.dataframe(df_coords.style.format("{:.2f}"))
    
    csv = df_coords.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger points pour profil de guidage", csv, "tool_path_LSB941.csv", "text/csv")
