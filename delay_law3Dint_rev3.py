import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- LIAISON AVEC LA LIBRAIRIE ---
from Library.byte_ndt_physics import ferrari2, discrete_windows

st.set_page_config(page_title="Byte NDT - Design 2D PA", layout="wide")

# --- TRADUCTION ---
lang = st.sidebar.selectbox("Langue / Language", ["Français", "English"])
T = {
    "Français": {
        "title": "🛡️ Interface Design 2D PA (Jumeau Numérique)",
        "params": "Paramètres d'entrée",
        "viz_ray": "🔦 Tracé de Rayons (Ray Plot 3D)",
        "viz_delay": "📈 Profil des Retards (µs)",
        "matrix": "📊 Matrice des Retards et Export",
        "export_btn": "📥 Télécharger Loi Focale (CSV)",
        "info": "Moteur Physique : Snell-Descartes 3D / Méthode de Ferrari"
    },
    "English": {
        "title": "🛡️ 2D PA Design Interface (Digital Twin)",
        "params": "Input Parameters",
        "viz_ray": "🔦 3D Ray Plotting",
        "viz_delay": "📈 Delay Profile (µs)",
        "matrix": "📊 Delay Matrix and Export",
        "export_btn": "📥 Download Focal Law (CSV)",
        "info": "Physics Engine: 3D Snell's Law / Ferrari Method"
    }
}

# --- CALCUL ---
def calculate_paut_delays(Mx, My, sx, sy, thetat, phi, theta2, DT0, DF, c1, c2):
    cr = c1 / c2
    ex = (np.arange(Mx) - (Mx - 1) / 2) * sx
    ey = (np.arange(My) - (My - 1) / 2) * sy
    Ex, Ey = np.meshgrid(ex, ey)
    ang1_rad = np.arcsin(c1 * np.sin(np.radians(theta2)) / c2)
    DQ = DT0 * np.tan(ang1_rad) + DF * np.tan(np.radians(theta2))
    tx, ty = DQ * np.cos(np.radians(phi)), DQ * np.sin(np.radians(phi))
    Db = np.sqrt((tx - Ex * np.cos(np.radians(thetat)))**2 + (ty - Ey)**2)
    De = DT0 + Ex * np.sin(np.radians(thetat))
    xi = np.zeros((My, Mx))
    for i in range(My):
        for j in range(Mx):
            xi[i, j] = ferrari2(cr, DF, De[i, j], Db[i, j])
    t = 1000 * np.sqrt(xi**2 + De**2) / c1 + 1000 * np.sqrt(DF**2 + (Db - xi)**2) / c2
    return np.max(t) - t, Ex, Ey, De, tx, ty, xi

# --- INTERFACE ---
st.title(T[lang]["title"])
st.sidebar.header(T[lang]["params"])
Mx = st.sidebar.number_input("Mx (Elements X)", 1, 32, 8)
My = st.sidebar.number_input("My (Elements Y)", 1, 32, 8)
sx = st.sidebar.number_input("Pitch X (mm)", 0.1, 2.0, 0.6)
sy = st.sidebar.number_input("Pitch Y (mm)", 0.1, 2.0, 0.6)
thetat = st.sidebar.slider("Angle Sonde/Wedge (°)", 0, 60, 0)
theta2 = st.sidebar.slider("Sector θ2 (°)", 35, 70, 55)
phi = st.sidebar.slider("Skew φ (°)", -30, 30, 0)
f_depth = st.sidebar.number_input("Focus Depth DF (mm)", 10.0, 300.0, 30.0)
c1 = st.sidebar.slider("Vitesse C1 (m/s) - Couplant/Sabot", 900, 3000, 2340, step=20)
c2 = st.sidebar.slider("Vitesse C2 (m/s) - Pièce (Shear)", 2000, 4000, 3240, step=20)
DT0 = st.sidebar.number_input("Height DT0 (mm)", value=30.0)

td, Ex, Ey, De, tx, ty, xi = calculate_paut_delays(Mx, My, sx, sy, thetat, phi, theta2, DT0, f_depth, c1, c2)

col1, col2 = st.columns(2)
with col1:
    st.subheader(T[lang]["viz_ray"])
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for i in range(My):
        for j in range(Mx):
            x1, y1, z1 = Ex[i,j]*np.cos(np.radians(thetat)), Ey[i,j], De[i,j]
            dist_xy = np.sqrt((tx-x1)**2 + (ty-y1)**2)
            x_int = x1 + xi[i,j]*(tx-x1)/dist_xy if dist_xy > 0 else x1
            y_int = y1 + xi[i,j]*(ty-y1)/dist_xy if dist_xy > 0 else y1
            ax.plot([x1, x_int], [y1, y_int], [z1, 0], color='blue', alpha=0.2)
            ax.plot([x_int, tx], [y_int, ty], [0, -f_depth], color='red', alpha=0.2)
    ax.view_init(elev=20, azim=45)
    st.pyplot(fig)

with col2:
    st.subheader(T[lang]["viz_delay"])
    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(range(len(td.flatten())), td.flatten(), color='royalblue')
    st.pyplot(fig_bar)

st.subheader(T[lang]["matrix"])
df_td = pd.DataFrame(td)
st.dataframe(df_td.style.format("{:.3f}"))
st.download_button(T[lang]["export_btn"], df_td.to_csv(index=False).encode('utf-8'), "loi_focale.csv", "text/csv")
st.caption(f"© 2026 Byte NDT | {T[lang]['info']}")

# --- 5. VISUALISATION DE LA CIBLE LSB 941 (GORGE N°1) ---
st.divider()
col_img, col_txt = st.columns([1, 2])

with col_img:
    # On va chercher l'image dans le dossier Assets
    st.image("Assets/LSB941_root.png", caption="Cible : Racine LSB 941 (L0)", use_container_width=True)

with col_txt:
    st.subheader("🎯 Cible Géométrique : Gorge n°1")
    st.write(f"Profondeur de référence : **-27.5 mm**")
    st.info("Le faisceau PAUT est focalisé précisément sur le rayon de raccordement de la première dent pour détecter d'éventuelles fissures de fatigue.")

# Ajout d'un repère visuel sur le graphique 3D (Ligne dorée)
z_gorge = -27.5
ax.plot([-50, 50], [0, 0], [z_gorge, z_gorge], color='gold', linestyle='--', linewidth=3, label="Gorge n°1")
ax.text(0, 0, z_gorge, "  Target: -27.5mm", color='gold', weight='bold')
ax.legend()
st.pyplot(fig) # On rafraîchit le graphique avec le nouveau repère
