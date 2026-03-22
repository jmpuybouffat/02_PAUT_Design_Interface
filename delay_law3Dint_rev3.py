import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ET TRADUCTION ---
st.set_page_config(page_title="Byte NDT - Design 2D PA", layout="wide")
lang = st.sidebar.selectbox("Langue / Language", ["Français", "English"])

T = {
    "Français": {
        "title": "🛡️ Interface Design 2D PA (Jumeau Numérique)",
        "params": "Paramètres d'entrée",
        "probe": "Géométrie Sonde",
        "target": "Cible (Balayage 2D)",
        "physics": "Physique des Milieux",
        "viz_ray": "🔦 Tracé de Rayons (Ray Plot 3D)",
        "viz_delay": "📈 Profil des Retards (µs)",
        "matrix": "📊 Matrice des Retards et Export",
        "export_btn": "📥 Télécharger Loi Focale (CSV)",
        "info": "Moteur Physique : Snell-Descartes 3D / Méthode de Ferrari"
    },
    "English": {
        "title": "🛡️ 2D PA Design Interface (Digital Twin)",
        "params": "Input Parameters",
        "probe": "Probe Geometry",
        "target": "Target (2D Steering)",
        "physics": "Media Physics",
        "viz_ray": "🔦 3D Ray Plotting",
        "viz_delay": "📈 Delay Profile (µs)",
        "matrix": "📊 Delay Matrix and Export",
        "export_btn": "📥 Download Focal Law (CSV)",
        "info": "Physics Engine: 3D Snell's Law / Ferrari Method"
    }
}

# --- 2. FONCTION DE CALCUL DES LOIS FOCALES ---
def calculate_paut_delays(Mx, My, sx, sy, thetat, phi, theta2, DT0, DF, c1, c2):
    cr = c1 / c2
    ex = (np.arange(Mx) - (Mx - 1) / 2) * sx
    ey = (np.arange(My) - (My - 1) / 2) * sy
    Ex, Ey = np.meshgrid(ex, ey)
    ang1_rad = np.arcsin(c1 * np.sin(np.radians(theta2)) / c2)
    
    # Calcul des coordonnées cibles
    DQ = DT0 * np.tan(ang1_rad) + DF * np.tan(np.radians(theta2))
    tx, ty = DQ * np.cos(np.radians(phi)), DQ * np.sin(np.radians(phi))
    
    # Distances et hauteurs
    Db = np.sqrt((tx - Ex * np.cos(np.radians(thetat)))**2 + (ty - Ey)**2)
    De = DT0 + Ex * np.sin(np.radians(thetat))
    
    # Appel de la fonction Ferrari depuis la Library
    xi = np.zeros((My, Mx))
    for i in range(My):
        for j in range(Mx):
            xi[i, j] = ferrari2(cr, DF, De[i, j], Db[i, j])
            
    # Temps de vol et Retards
    t = 1000 * np.sqrt(xi**2 + De**2) / c1 + 1000 * np.sqrt(DF**2 + (Db - xi)**2) / c2
    td = np.max(t) - t
    return td, Ex, Ey, De, tx, ty, xi

# --- 3. INTERFACE UTILISATEUR (SIDEBAR) ---
st.title(T[lang]["title"])
st.sidebar.header(T[lang]["params"])

# Géométrie
st.sidebar.subheader(T[lang]["probe"])
Mx = st.sidebar.number_input("Mx (Elements X)", 1, 32, 8)
My = st.sidebar.number_input("My (Elements Y)", 1, 32, 8)
sx = st.sidebar.number_input("Pitch X (mm)", 0.1, 2.0, 0.6)
sy = st.sidebar.number_input("Pitch Y (mm)", 0.1, 2.0, 0.6)
thetat = st.sidebar.slider("Angle Sonde/Wedge (°)", 0, 45, 0)

# Cibles (Sectoriel 35-70 et Skew -30-30)
st.sidebar.subheader(T[lang]["target"])
theta2 = st.sidebar.slider("Sector θ2 (°)", 35, 70, 55)
phi = st.sidebar.slider("Skew φ (°)", -30, 30, 0)
f_depth = st.sidebar.number_input("Focus Depth DF (mm)", 10.0, 150.0, 30.0)

# Milieux
st.sidebar.subheader(T[lang]["physics"])
c1 = st.sidebar.number_input("C1 (Wedge/Water) m/s", value=1480)
c2 = st.sidebar.number_input("C2 (Steel Shear) m/s", value=3240)
DT0 = st.sidebar.number_input("Height DT0 (mm)", value=10.0)

# --- 4. CALCUL ET AFFICHAGE ---
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
            # Calcul du point d'impact à l'interface Z=0
            x_int = x1 + xi[i,j]*(tx-x1)/dist_xy if dist_xy > 0 else x1
            y_int = y1 + xi[i,j]*(ty-y1)/dist_xy if dist_xy > 0 else y1
            # Rayons Milieu 1 (Bleu) et Milieu 2 (Rouge)
            ax.plot([x1, x_int], [y1, y_int], [z1, 0], color='blue', alpha=0.2)
            ax.plot([x_int, tx], [y_int, ty], [0, -f_depth], color='red', alpha=0.2)
    ax.view_init(elev=20, azim=45)
    st.pyplot(fig)

with col2:
    st.subheader(T[lang]["viz_delay"])
    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(range(len(td.flatten())), td.flatten(), color='royalblue', edgecolor='black')
    ax_bar.set_ylabel("µs")
    st.pyplot(fig_bar)

# --- 5. MATRICE ET EXPORT ---
st.subheader(T[lang]["matrix"])
df_td = pd.DataFrame(td)
st.dataframe(df_td.style.format("{:.3f}"))
st.download_button(T[lang]["export_btn"], df_td.to_csv(index=False).encode('utf-8'), "byte_ndt_focal_law.csv", "text/csv")

st.caption(f"© 2026 Byte NDT | {T[lang]['info']}")

