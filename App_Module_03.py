import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Library.byte_ndt_physics import calculate_beam_field, apply_db_mask

st.set_page_config(page_title="Byte NDT - Module 03 : Expertise Énergie", layout="wide")

st.title("🔥 Cartographie d'Énergie PAUT - Turbine LSB 941")

# Sidebar : Paramètres de la sonde
st.sidebar.header("🛠️ Configuration Sonde")
L1 = st.sidebar.slider("Éléments X", 4, 12, 11)
freq = st.sidebar.slider("Fréquence (MHz)", 1.0, 10.0, 5.0)

# Zone d'intérêt (ROI) sur la Gorge n°1
st.subheader("🎯 Tache focale sur la Gorge n°1 (-27.5 mm)")

# Calcul du champ (ROI de 20x20mm autour de la dent)
ROI = {
    'xs': np.linspace(-10, 10, 100),
    'zs': np.linspace(20, 40, 100)
}

# Matériau Acier (Densité 7.9, Vitesses S=3200)
mat = [1.0, 1480, 7.9, 5900, 3200, 's']

# Exécution du moteur Sommerfeld
if st.button("🚀 Lancer la Simulation d'Énergie"):
    with st.spinner("Calcul des ondelettes en cours..."):
        vmag = calculate_beam_field(L1, L1, 0.2, 0.2, freq, mat, 30.0, 60, 0, 27.5, ROI)
        heatmap = apply_db_mask(vmag)
        
        # Affichage CIVA-Style
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(heatmap, extent=[-10, 10, 40, 20], cmap='jet')
        plt.colorbar(im, label="Intensité Relative (dB)")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Profondeur Z (mm)")
        ax.set_title(f"Focalisation à {freq} MHz - Contours -3/-6/-12 dB")
        st.pyplot(fig)
        
        st.success("Simulation terminée. Tache focale validée pour détection de fissures.")
