import io
import os
import re
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Simulateur Commercial Madagascar", layout="wide"
)

# ==========================================
# THÈME GLOBAL - CHARTE GRAPHIQUE STAR
# ==========================================
st.markdown(
    """
    <style>
    /* Importation des polices */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&display=swap');

    /* Typographie globale */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* --- EN-TÊTE PRINCIPAL --- */
    .header-star {
        background: #ffffff;
        padding: 35px 40px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 35px;
        position: relative;
        overflow: hidden;
        border-left: 8px solid transparent;
        border-image: linear-gradient(to bottom, #E3000F 50%, #009639 50%) 1;
    }
    
    .header-star::before {
        content: '';
        position: absolute;
        top: -80px;
        right: -80px;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(227,0,15,0.05) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .header-star::after {
        content: '';
        position: absolute;
        bottom: -80px;
        left: 20%;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(0,150,57,0.05) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .header-title-star {
        font-size: 2.4rem;
        font-weight: 900;
        color: #1a1a1a;
        margin: 0;
        line-height: 1.2;
        text-transform: uppercase;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
        display: inline-block;
    }

    .text-red {
        color: #E3000F;
    }

    .star-icon {
        color: #E3000F;
        font-size: 2rem;
        margin-left: 15px;
        display: inline-block;
        animation: spin-star 4s linear infinite;
        text-shadow: 2px 2px 4px rgba(227,0,15,0.2);
    }

    @keyframes spin-star {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.1); }
        100% { transform: rotate(360deg) scale(1); }
    }

    /* --- SOUS-TITRES ENCADRÉS (CENTRÉS ET SANS RETOUR À LA LIGNE) --- */
    h2, h3, .custom-subtitle {
        color: #E3000F !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700 !important;
        background-color: #ffffff;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1.5px solid #E3000F; /* Contour rouge STAR fin */
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-top: 30px;
        margin-bottom: 20px;
        
        /* Centrage et gestion de ligne */
        display: flex;
        justify-content: center;
        align-items: center;
        white-space: nowrap; /* Force sur une seule ligne */
        overflow: hidden;
        text-overflow: ellipsis; /* Ajoute "..." si c'est trop long */
    }

    /* Ajustement de la taille pour les titres plus longs */
    h2 { font-size: 1.5rem !important; }
    h3, .custom-subtitle { font-size: 1.3rem !important; }

    /* --- BARRE LATÉRALE (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 4px solid #009639;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #009639 !important;
        background-color: transparent;
        border: none;
        box-shadow: none;
        padding: 0;
        border-left: none;
        display: block;
        white-space: normal;
    }

    /* --- BOUTONS --- */
    .stButton>button, .stDownloadButton>button {
        background-color: #E3000F !important;
        color: white !important;
        border-radius: 5px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: 0.3s;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #b3000b !important;
    }

    /* --- EXPANDERS --- */
    .streamlit-expanderHeader {
        background-color: #f0f4f8 !important;
        color: #E3000F !important;
        font-weight: 700;
        border-left: 4px solid #009639;
    }

    /* --- ONGLETS --- */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent;
        color: #333;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #E3000F !important;
        border-bottom-color: #E3000F !important;
    }

    /* --- MÉTRIQUES STANDARDS --- */
    [data-testid="stMetricValue"] {
        color: #E3000F;
        font-size: 1.6rem !important;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #009639;
        font-size: 0.9rem !important;
        font-weight: 600;
    }

    /* --- TABLEAUX --- */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }

    /* ==========================================
       STYLE CARTES KPI
       ========================================== */
    .kpi-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        flex: 1;
        background-color: #ffffff;
        border-radius: 6px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea;
        overflow: hidden;
        text-align: center;
        padding-bottom: 20px;
        position: relative;
    }
    .kpi-header {
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 8px 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .bg-dark-blue { background-color: #1f4e79; }
    .bg-light-blue { background-color: #5b9bd5; }
    .bg-red { background-color: #c00000; }
    .bg-yellow { background-color: #ffc000; color: #333; }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #333333;
        margin: 20px 0 5px 0;
        line-height: 1;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #666666;
        font-weight: 500;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
    }
    .kpi-arrow-up {
        color: #70ad47;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-star">
        <div class="header-title-star">
            <span class="text-red">Simulateur Stratégique & Optimisation Commerciale</span>
            <span class="star-icon">★</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# COMPATIBILITÉ PLOTLY 5 / 6
# ==========================================
_HAS_SCATTER_MAPBOX = hasattr(px, "scatter_mapbox")

def scatter_map_auto(df, **kwargs):
    if _HAS_SCATTER_MAPBOX:
        return px.scatter_mapbox(df, **kwargs)
    if "mapbox_style" in kwargs:
        kwargs["map_style"] = kwargs.pop("mapbox_style")
    return px.scatter_map(df, **kwargs)

def apply_marker_style(fig, size=6, opacity=0.75, line_width=None, line_color=None):
    for trace in fig.data:
        try:
            trace.marker.size = size
            trace.marker.opacity = opacity
            if line_width is not None:
                trace.marker.line.width = line_width
            if line_color is not None:
                trace.marker.line.color = line_color
        except Exception:
            pass

# ==========================================
# 1. DONNÉES DE BASE
# ==========================================
@st.cache_data
def load_base_data():
    data = {
        "Région": [
            "Centre", "Centre", "Est", "Est", "Nord", "Nord", "Nord",
            "Nord", "Nord", "Sud", "Sud", "Sud", "Sud", "Sud", "Sud",
        ],
        "Agence": [
            "11-Andranomahery", "12-Antsirabe", "01-Tanjombato", "09-Tamatave",
            "03-Usine-Diego", "07-Majunga", "18-Ambanja", "19-Sambava",
            "21-Nosy-Be", "04-Tulear", "05-Fianarantsoa", "06-Ihosy",
            "08-Manakara", "23-Morondava", "24-Fort-Dauphin",
        ],
        "MV": [5, 2, 5, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        "CS_Actuels": [32, 13, 31, 18, 6, 10, 6, 5, 4, 7, 8, 3, 4, 4, 5],
        "Ajustement_CS_DRV": [6, 3, 6, 3, 1, 3, 2, 2, 1, 2, 0, 1, 2, 2, 1],
        "Vol_2026_Hls": [
            843256, 306183, 878064, 511164, 189959, 338706, 213219,
            150744, 142658, 202606, 138452, 86860, 202880, 85204, 113113,
        ],
        "Vol_2027_Hls": [
            902190, 339742, 976891, 547209, 187677, 366320, 238634,
            172094, 161164, 227276, 155168, 97400, 235379, 96757, 119372,
        ],
        "Nbre_PDV_Tradi": [
            5950, 2450, 5987, 5307, 1009, 2830, 2400, 800, 1300,
            1365, 1500, 700, 1550, 930, 950,
        ],
        "Temps_Dispo_Mois_Min": [
            601920, 253440, 586080, 332640, 110880, 205920, 126720,
            110880, 79200, 142560, 126720, 63360, 95040, 95040, 95040,
        ],
        "Vol_ZB_Inclut_Mois_Hls": [
            215, 0, 4005, 0, 70, 2950, 0, 0, 0, 2473, 0, 0, 0, 0, 0,
        ],
        "PDV_Estimes_ZB": [50, 0, 850, 0, 30, 600, 0, 0, 0, 500, 0, 0, 0, 0, 0],
        "Lat": [
            -18.8792, -19.8658, -18.9667, -18.1492, -12.2786, -15.7167,
            -13.6773, -14.2667, -13.3167, -23.3500, -21.4333, -22.4000,
            -22.1333, -20.2833, -25.0200,
        ],
        "Lon": [
            47.5079, 47.0333, 47.5333, 49.4023, 49.2917, 46.3167,
            48.4501, 50.1667, 48.2667, 43.6667, 47.0833, 46.1333,
            48.0167, 44.2833, 46.9900,
        ],
    }
    return pd.DataFrame(data)

df_raw = load_base_data()

# ==========================================
# 2. PARSING DMS
# ==========================================
def _dms_to_dec_single(txt):
    if not isinstance(txt, str):
        return None, None
    s = (txt.replace("?", "°")
            .replace("’", "'").replace("′", "'")
            .replace("″", '"').replace("”", '"')
            .replace(",", " "))
    pattern = r"(\d+)\s*°\s*(\d+)\s*'\s*([\d.]+)\s*\"?\s*([NSEW])"
    matches = re.findall(pattern, s)
    if len(matches) < 2:
        return None, None
    lat = lon = None
    for d, m, sec, dir_ in matches:
        val = float(d) + float(m) / 60 + float(sec) / 3600
        if dir_ in ("S", "W"):
            val = -val
        if dir_ in ("N", "S"):
            lat = val
        else:
            lon = val
    return lat, lon

# ==========================================
# 3. CHARGEMENT GPS
# ==========================================
def _find_gps_column(columns):
    alias = (
        "gps", "coordonnees", "coordonnées", "coordonnee", "coordonnée",
        "position", "localisation", "coordonnees_gps", "point_gps",
        "gps_coord", "coord",
    )
    for col in columns:
        if str(col).strip().lower() in alias:
            return col
    return None

@st.cache_data
def load_gps_data(_uploaded_file=None):
    if _uploaded_file is None:
        return pd.DataFrame()

    source = _uploaded_file

    try:
        xls = pd.ExcelFile(source)
        sheet_names = xls.sheet_names
    except Exception as e:
        st.error(f"❌ Impossible d'ouvrir le classeur : {e}")
        return pd.DataFrame()

    sheet_to_use = None
    for sh in sheet_names:
        try:
            tmp = pd.read_excel(source, sheet_name=sh, nrows=5)
            tmp.columns = [str(c).strip() for c in tmp.columns]
            if _find_gps_column(tmp.columns) is not None:
                sheet_to_use = sh
                break
        except Exception:
            continue

    if sheet_to_use is None:
        for c in ["Feuil1", "Feuille1", "Sheet1", "GPS", "Coordonnees",
                  "Coordonnées", "Data", "Clients"]:
            if c in sheet_names:
                sheet_to_use = c
                break

    if sheet_to_use is None:
        sheet_to_use = sheet_names[0]

    try:
        df_gps = pd.read_excel(source, sheet_name=sheet_to_use)
    except Exception as e:
        st.error(f"❌ Erreur de lecture de la feuille `{sheet_to_use}` : {e}")
        return pd.DataFrame()

    df_gps.columns = [str(c).strip() for c in df_gps.columns]

    if not df_gps.empty and str(df_gps.iloc[0].get("Ag", "")).strip() == "Ag":
        df_gps = df_gps.iloc[1:].reset_index(drop=True)

    gps_col = _find_gps_column(df_gps.columns)
    if gps_col is None:
        st.error(
            f"❌ Aucune colonne GPS trouvée. Colonnes disponibles : "
            f"{list(df_gps.columns)}"
        )
        return pd.DataFrame()

    coords = df_gps[gps_col].apply(_dms_to_dec_single)
    df_gps["Lat"] = [c[0] for c in coords]
    df_gps["Lon"] = [c[1] for c in coords]

    df_gps = df_gps.dropna(subset=["Lat", "Lon"])
    df_gps = df_gps[
        df_gps["Lat"].between(-26, -11) & df_gps["Lon"].between(42, 51)
    ]

    st.success(
        f"✅ Fichier GPS chargé — feuille `{sheet_to_use}` — "
        f"{len(df_gps):,} points valides."
    )
    return df_gps.reset_index(drop=True)

# --- CHARGEMENT SYSTÉMATIQUE DU FICHIER GPS ---
_uploaded = st.file_uploader(
    "Charger le fichier Excel des coordonnées GPS (Coord_GPS.xlsx)",
    type=["xlsx", "xls"],
)
df_clients_gps = load_gps_data(_uploaded) if _uploaded else pd.DataFrame()

# ==========================================
# 4. SIDEBAR — PARAMÈTRES
# ==========================================
st.sidebar.header("⚙️ Paramètres & Seuils d'Évaluation")

obj_visites_jour = st.sidebar.number_input(
    "Objectif Visites max / Commercial / Jour", 1, 35, 22
)
jours_travailles_mois = st.sidebar.number_input(
    "Jours travaillés / mois", 15, 26, 20
)
temps_moyen_visite_min = st.sidebar.number_input(
    "Temps moyen par visite (min)", 10, 90, 30
)
cible_vol_cs = st.sidebar.number_input(
    "Volume Cible par CS (Hls/an)", 1000, 50000, 25000, 1000
)

st.sidebar.subheader("Seuils de Charge")
seuil_surcharge_cs = st.sidebar.number_input("Seuil Surcharge CS (> X PDV)", 200, 500, 250)
seuil_risque_cs = st.sidebar.number_input("Seuil Risque CS (> X PDV)", 180, 400, 210)
seuil_sous_charge_cs = st.sidebar.number_input("Seuil Sous-charge CS (< X PDV)", 50, 200, 150)
seuil_surcharge_mv = st.sidebar.number_input(
    "Seuil Surcharge MV (> X Hls vol)", 20000, 500000, 200000
)

st.sidebar.subheader("🎯 Simulation Zones Blanches par Agence")
selected_agence_zb = st.sidebar.selectbox(
    "Sélectionner une Agence", df_raw["Agence"].unique()
)
default_zb_vol = int(
    df_raw.loc[df_raw["Agence"] == selected_agence_zb, "Vol_ZB_Inclut_Mois_Hls"].values[0]
)
default_zb_pdv = int(
    df_raw.loc[df_raw["Agence"] == selected_agence_zb, "PDV_Estimes_ZB"].values[0]
)

sim_zb_vol_mois = st.sidebar.number_input(
    f"Volume ZB Mensuel ({selected_agence_zb})", 0, 10000, default_zb_vol
)
sim_zb_pdv = st.sidebar.number_input(
    f"PDV ZB ({selected_agence_zb})", 0, 2000, default_zb_pdv
)

df = df_raw.copy()
df.loc[df["Agence"] == selected_agence_zb, "Vol_ZB_Inclut_Mois_Hls"] = sim_zb_vol_mois
df.loc[df["Agence"] == selected_agence_zb, "PDV_Estimes_ZB"] = sim_zb_pdv

# ==========================================
# 5. CALCULS DYNAMIQUES
# ==========================================
df["Total_CS_Propose"] = df["CS_Actuels"] + df["Ajustement_CS_DRV"]
df["Evol_Vol_Abs"] = df["Vol_2027_Hls"] - df["Vol_2026_Hls"]
df["Evol_Vol_Pct"] = (df["Evol_Vol_Abs"] / df["Vol_2026_Hls"]) * 100
df["PDV_Total_Ajuste"] = df["Nbre_PDV_Tradi"] + df["PDV_Estimes_ZB"]

df["Vol_2027_Par_CS"] = df["Vol_2027_Hls"] / df["Total_CS_Propose"]
df["Vol_2027_Par_MV"] = df["Vol_2027_Hls"] / df["MV"]
df["PDV_Par_CS"] = df["PDV_Total_Ajuste"] / df["Total_CS_Propose"]
df["PDV_Par_MV"] = df["PDV_Total_Ajuste"] / df["MV"]
df["Ratio_CS_MV"] = df["Total_CS_Propose"] / df["MV"]

nat_vol_cs = df["Vol_2027_Hls"].sum() / df["Total_CS_Propose"].sum()
nat_vol_mv = df["Vol_2027_Hls"].sum() / df["MV"].sum()
nat_pdv_cs = df["PDV_Total_Ajuste"].sum() / df["Total_CS_Propose"].sum()
nat_pdv_mv = df["PDV_Total_Ajuste"].sum() / df["MV"].sum()

st.subheader("🇲🇬 Indicateurs Clés de Référence (Moyenne Nationale)")

# ==========================================
# AFFICHAGE KPI CARDS
# ==========================================
st.markdown(f"""
    <div class="kpi-container">
        <!-- Carte 1 -->
        <div class="kpi-card">
            <div class="kpi-header bg-dark-blue">Volume Moyen / CS</div>
            <div class="kpi-value">{nat_vol_cs:,.0f}</div>
            <div class="kpi-sub"><span class="kpi-arrow-up">↑</span> Cible : {cible_vol_cs:,.0f} Hecto</div>
        </div>
        <!-- Carte 2 -->
        <div class="kpi-card">
            <div class="kpi-header bg-light-blue">Volume Moyen / MV</div>
            <div class="kpi-value">{nat_vol_mv:,.0f}</div>
            <div class="kpi-sub">Hecto</div>
        </div>
        <!-- Carte 3 -->
        <div class="kpi-card">
            <div class="kpi-header bg-red">PDV Moyens / CS</div>
            <div class="kpi-value">{nat_pdv_cs:.1f}</div>
            <div class="kpi-sub">Points de Vente</div>
        </div>
        <!-- Carte 4 -->
        <div class="kpi-card">
            <div class="kpi-header bg-yellow">PDV Moyens / MV</div>
            <div class="kpi-value">{nat_pdv_mv:.1f}</div>
            <div class="kpi-sub">Points de Vente</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

def get_statut_cs(pdv_cs):
    if pdv_cs >= seuil_surcharge_cs:
        return "🔴 Surcharge CS"
    elif pdv_cs >= seuil_risque_cs:
        return "🟡 Risque Surcharge CS"
    elif pdv_cs <= seuil_sous_charge_cs:
        return "🔵 Sous-charge CS"
    else:
        return "🟢 Équilibré CS"

def get_statut_mv(vol_mv):
    if vol_mv >= seuil_surcharge_mv:
        return "🔴 Surcharge MV"
    return "🟢 Équilibré MV"

df["Statut_CS"] = df["PDV_Par_CS"].apply(get_statut_cs)
df["Statut_MV"] = df["Vol_2027_Par_MV"].apply(get_statut_mv)

def color_status_cells(val):
    if "🔴" in str(val):
        return "background-color: #ffcccc; color: #900000; font-weight: bold;"
    elif "🟡" in str(val):
        return "background-color: #fff3cd; color: #856404; font-weight: bold;"
    elif "🟢" in str(val):
        return "background-color: #d4edda; color: #155724; font-weight: bold;"
    elif "🔵" in str(val):
        return "background-color: #cce5ff; color: #004085; font-weight: bold;"
    return ""

# ==========================================
# 6. TABLEAU RÉCAPITULATIF
# ==========================================
st.subheader("📊 Tableau Récapitulatif : Volumes 2026 vs 2027 & Effectifs")
st.markdown(
    "*(Les cellules surlignées en fond jaune indiquent les variables dynamiques "
    "modifiées par vos paramètres ou la sélection des zones blanches)*"
)

df_recap = pd.DataFrame({
    "Agence": df["Agence"],
    "Région": df["Région"],
    "MV": df["MV"],
    "CS": df["Total_CS_Propose"],
    "Vol 2026 (Hls)": df["Vol_2026_Hls"],
    "Vol 2027 (Hls)": df["Vol_2027_Hls"],
    "Evol (+/- Hls)": df["Evol_Vol_Abs"],
    "Evol (%)": df["Evol_Vol_Pct"],
    "Vol / CS": df["Vol_2027_Par_CS"].round(0),
    "Vol / MV": df["Vol_2027_Par_MV"].round(0),
    "PDV / CS": df["PDV_Par_CS"].round(1),
    "Statut CS": df["Statut_CS"],
    "Statut MV": df["Statut_MV"],
})

def highlight_dynamic_cols(col):
    if col.name in [
        "Vol 2027 (Hls)", "Evol (+/- Hls)", "Evol (%)",
        "Vol / CS", "Vol / MV", "PDV / CS",
    ]:
        return ["background-color: #fffacd; font-weight: bold;"] * len(col)
    return [""] * len(col)

st.dataframe(
    df_recap.style
    .apply(highlight_dynamic_cols, axis=0)
    .map(color_status_cells, subset=["Statut CS", "Statut MV"])
    .format({
        "Vol 2026 (Hls)": "{:,.0f}",
        "Vol 2027 (Hls)": "{:,.0f}",
        "Evol (+/- Hls)": "{:+,.0f}",
        "Evol (%)": "{:+.2f}%",
        "Vol / CS": "{:,.0f}",
        "Vol / MV": "{:,.0f}",
        "PDV / CS": "{:.1f}",
    }),
    use_container_width=True,
)

# ==========================================
# 7. SIMULATEUR AVANT / APRÈS
# ==========================================
st.markdown("---")
st.markdown(
    """
    <style>
    .sim-container {
        background-color: #f0f4f8;
        border-left: 6px solid #E3000F;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="sim-container">', unsafe_allow_html=True)
st.subheader("🔄 Module de Simulation Avant / Après : Ajustement des Effectifs (CS & MV)")
st.markdown(
    "Simulez l'impact d'un **recrutement ou transfert d'effectifs** (+/- CS et MV) "
    "pour une agence et observez le recalcul automatique de la charge (Volume & PDV) "
    "et du **code couleur de situation** :"
)

sc1, sc2, sc3 = st.columns(3)
selected_sim_agence = sc1.selectbox(
    "Sélectionner l'Agence à simuler", df["Agence"].unique(), key="sim_agence_select"
)
delta_cs = sc2.number_input(
    "Ajustement CS (+/- Recrutement/Transfert)", -15, 15, 0, step=1, key="sim_delta_cs"
)
delta_mv = sc3.number_input(
    "Ajustement MV (+/- Recrutement/Transfert)", -5, 5, 0, step=1, key="sim_delta_mv"
)

row_sim_orig = df.loc[df["Agence"] == selected_sim_agence].iloc[0]
mv_avant = row_sim_orig["MV"]
cs_avant = row_sim_orig["Total_CS_Propose"]
vol_2027_sim = row_sim_orig["Vol_2027_Hls"]
pdv_tot_sim = row_sim_orig["PDV_Total_Ajuste"]

vol_cs_avant = row_sim_orig["Vol_2027_Par_CS"]
vol_mv_avant = row_sim_orig["Vol_2027_Par_MV"]
pdv_cs_avant = row_sim_orig["PDV_Par_CS"]
statut_cs_avant = row_sim_orig["Statut_CS"]
statut_mv_avant = row_sim_orig["Statut_MV"]

cs_apres = max(1, cs_avant + delta_cs)
mv_apres = max(1, mv_avant + delta_mv)
vol_cs_apres = vol_2027_sim / cs_apres
vol_mv_apres = vol_2027_sim / mv_apres
pdv_cs_apres = pdv_tot_sim / cs_apres
statut_cs_apres = get_statut_cs(pdv_cs_apres)
statut_mv_apres = get_statut_mv(vol_mv_apres)

df_sim_comp = pd.DataFrame({
    "Dimension": [
        "Effectif MV", "Effectif CS", "Ratio CS / 1 MV",
        "Volume / CS (Hls/an)", "Volume / MV (Hls/an)",
        "Charge PDV / CS", "Statut Charge CS", "Statut Charge MV",
    ],
    "Situation AVANT": [
        f"{mv_avant}", f"{cs_avant}", f"{cs_avant / mv_avant:.1f}",
        f"{vol_cs_avant:,.0f}", f"{vol_mv_avant:,.0f}",
        f"{pdv_cs_avant:.1f}", statut_cs_avant, statut_mv_avant,
    ],
    "Situation APRÈS (Simulation)": [
        f"{mv_apres} ({delta_mv:+d})", f"{cs_apres} ({delta_cs:+d})",
        f"{cs_apres / mv_apres:.1f}", f"{vol_cs_apres:,.0f}",
        f"{vol_mv_apres:,.0f}", f"{pdv_cs_apres:.1f}",
        statut_cs_apres, statut_mv_apres,
    ],
})

st.dataframe(
    df_sim_comp.style.map(
        color_status_cells, subset=["Situation AVANT", "Situation APRÈS (Simulation)"]
    ),
    use_container_width=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 8. GRAPHIQUES
# ==========================================
st.markdown("---")
st.subheader("📈 Visualisation Interactive : Agence vs Moyenne Nationale")

g_cols = st.columns(2)
with g_cols[0]:
    fig_vol = px.bar(
        df, x="Agence", y="Vol_2027_Par_CS", color="Région",
        title="Volume Moyen par CS par Agence vs Cible Nationale",
        labels={"Vol_2027_Par_CS": "Volume / CS (Hls)"},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_vol.add_hline(y=nat_vol_cs, line_dash="dash", line_color="#E3000F",
                      annotation_text=f"Moyenne Nat ({nat_vol_cs:,.0f} Hls)")
    fig_vol.add_hline(y=cible_vol_cs, line_dash="dot", line_color="#009639",
                      annotation_text=f"Cible CS ({cible_vol_cs:,.0f} Hls)")
    fig_vol.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_vol, use_container_width=True)

with g_cols[1]:
    fig_pdv = px.bar(
        df, x="Agence", y="PDV_Par_CS", color="Région",
        title="Charge PDV par CS par Agence vs Moyenne Nationale",
        labels={"PDV_Par_CS": "PDV / CS"},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_pdv.add_hline(y=nat_pdv_cs, line_dash="dash", line_color="#E3000F",
                      annotation_text=f"Moyenne Nat ({nat_pdv_cs:.1f} PDV)")
    fig_pdv.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_pdv, use_container_width=True)

# ==========================================
# 9. SIMULATION FINANCIÈRE
# ==========================================
st.markdown("---")
st.subheader("💰 Simulation Financière & Point Mort (Break-even) par Agence")

fin_cols = st.columns(3)
selected_fin_agence = fin_cols[0].selectbox(
    "Choisir l'Agence pour la simulation financière", df["Agence"].unique()
)
cout_mensuel_cs = fin_cols[1].number_input(
    "Coût mensuel d'un CS (MGA)", 500000, 5000000, 1500000, 100000
)
marge_nette_hl = fin_cols[2].number_input(
    "Marge nette par Hectolitre (MGA/Hl)", 10000, 500000, 50000, 5000
)

row_fin = df.loc[df["Agence"] == selected_fin_agence].iloc[0]
vol_agence = row_fin["Vol_2027_Hls"]
cs_agence = row_fin["Total_CS_Propose"]
vol_par_cs_agence = row_fin["Vol_2027_Par_CS"]

cout_annuel_cs = cout_mensuel_cs * 12
seuil_rentabilite_hl = cout_annuel_cs / marge_nette_hl if marge_nette_hl > 0 else 0
couverture_besoin = (
    (vol_par_cs_agence / seuil_rentabilite_hl) * 100 if seuil_rentabilite_hl > 0 else 0
)

st.markdown(
    f'<div class="custom-subtitle">📋 Mode de calcul & Résultats pour : {selected_fin_agence}</div>', 
    unsafe_allow_html=True
)

st.latex(
    r"\text{Seuil de Rentabilité (Break-even)} = "
    r"\frac{\text{Coût Annuel du CS}}{\text{Marge Nette par Hl}}"
)
st.markdown(
    f"- **Coût Annuel par CS :** {cout_mensuel_cs:,.0f} MGA $\\times$ 12 mois = "
    f"**{cout_annuel_cs:,.0f} MGA**"
)
st.markdown(
    f"- **Volume nécessaire par CS :** "
    f"$\\frac{{{cout_annuel_cs:,.0f}}}{{{marge_nette_hl:,.0f}}}=$ "
    f"**{seuil_rentabilite_hl:,.1f} Hls/an**"
)
st.markdown(
    f"- **Performance actuelle :** {vol_par_cs_agence:,.1f} Hls/an/CS "
    f"({vol_agence:,.0f} Hls / {cs_agence} CS)"
)

if vol_par_cs_agence >= seuil_rentabilite_hl:
    st.success(
        f"✅ L'agence {selected_fin_agence} est **rentable** "
        f"(Couverture : **{couverture_besoin:.1f}%**)."
    )
else:
    st.warning(
        f"⚠️ Productivité en deçà du seuil de rentabilité "
        f"(Couverture : **{couverture_besoin:.1f}%**)."
    )

# ==========================================
# 10. CARTE INTERACTIVE (AGENCES + CLIENTS GPS)
# ==========================================
st.markdown("---")
st.subheader("🗺️ Carte Interactive : Agences & Points de Vente Détaillés")

if not df_clients_gps.empty:
    map_mode = st.radio(
        "Mode d'affichage de la carte :",
        [
            "Vue d'ensemble des Agences",
            "Détail des Points de Vente par Type & Commercial",
        ],
        horizontal=True,
    )

    if map_mode == "Vue d'ensemble des Agences":
        fig_map = scatter_map_auto(
            df,
            lat="Lat", lon="Lon",
            size="Vol_2027_Hls",
            color="Région",
            hover_name="Agence",
            hover_data={
                "Vol_2027_Hls": ":,.0f",
                "Statut_CS": True, "Statut_MV": True,
                "Lat": False, "Lon": False,
            },
            zoom=4.8,
            center={"lat": -18.79, "lon": 46.85},
            mapbox_style="open-street-map",
            height=600,
            title="Emplacement des Agences (taille ∝ Volume 2027)",
        )

    else:
        ag_col = None
        for c in df_clients_gps.columns:
            if str(c).strip().lower() in ("ag", "agence", "code_agence",
                                          "code agence", "id_agence"):
                ag_col = c
                break

        if ag_col is not None:
            selected_agence_map = st.selectbox(
                "Filtrer par Agence :",
                ["Toutes les agences"] + df["Agence"].tolist(),
            )
            df_map_filtered = df_clients_gps.copy()
            if selected_agence_map != "Toutes les agences":
                ag_id = str(int(selected_agence_map.split("-")[0])).zfill(2)
                df_map_filtered = df_map_filtered[
                    df_map_filtered[ag_col].astype(str).str.zfill(2) == ag_id
                ]
        else:
            st.info(
                "ℹ️ Colonne `Ag` absente du fichier — affichage de tous les "
                "points de vente."
            )
            df_map_filtered = df_clients_gps.copy()

        hover_cols = {}
        for c in ["Nom CS2", "Nom client", "Description activité",
                  "Activite", "CS"]:
            if c in df_map_filtered.columns:
                hover_cols[c] = True
        hover_cols["Lat"] = False
        hover_cols["Lon"] = False

        color_col = None
        for c in ["Description activité", "Activite", "Description activite"]:
            if c in df_map_filtered.columns:
                color_col = c
                break

        color_discrete_map = None
        if color_col is not None:
            unique_vals = df_map_filtered[color_col].astype(str).unique()
            default_palette = px.colors.qualitative.Plotly
            color_discrete_map = {}
            idx = 0
            for val in unique_vals:
                if str(val).strip().upper() == "ZONE BLANCHE":
                    color_discrete_map[val] = "#000000"
                else:
                    color_discrete_map[val] = default_palette[
                        idx % len(default_palette)
                    ]
                    idx += 1

        kwargs = dict(
            lat="Lat", lon="Lon",
            hover_name="Nom client" if "Nom client" in df_map_filtered.columns else None,
            hover_data=hover_cols,
            zoom=5.5,
            center={"lat": -18.79, "lon": 46.85},
            mapbox_style="open-street-map",
            height=650,
            title="Cartographie des Points de Vente",
        )
        if color_col is not None:
            kwargs["color"] = color_col
            if color_discrete_map is not None:
                kwargs["color_discrete_map"] = color_discrete_map

        fig_map = scatter_map_auto(df_map_filtered, **kwargs)
        apply_marker_style(fig_map, size=6, opacity=0.75)
        st.caption(f"📍 {len(df_clients_gps):,} points de vente chargés.")

    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.warning(
        "⚠️ Aucune donnée GPS disponible. Uploadez le fichier Excel "
        "pour afficher les points de vente."
    )

# ==========================================
# 11. RECOMMANDATIONS & EXPORT
# ==========================================
st.markdown("---")
st.subheader("📋 Recommandations Détaillées par Agence & Export")

recos_list = []
for _, row in df.iterrows():
    region_actuelle = row["Région"]
    agences_meme_region = df[
        (df["Région"] == region_actuelle) & (df["Agence"] != row["Agence"])
    ]

    conseil_transfert = "Equilibre regional stable."
    if "Surcharge" in row["Statut_CS"]:
        sous_charges = agences_meme_region[
            agences_meme_region["Statut_CS"].str.contains("Sous-charge")
        ]
        if not sous_charges.empty:
            noms_sc = ", ".join(sous_charges["Agence"].tolist())
            conseil_transfert = (
                f"Surcharge CS : Envisager un transfert depuis [{noms_sc}] "
                "(meme region) ou recrutement local."
            )
        else:
            conseil_transfert = (
                "Surcharge CS : Pas de sous-charge regionale. "
                "Recrutement local imperatif."
            )
    elif "Sous-charge" in row["Statut_CS"]:
        surcharges = agences_meme_region[
            agences_meme_region["Statut_CS"].str.contains("Surcharge")
        ]
        if not surcharges.empty:
            noms_sur = ", ".join(surcharges["Agence"].tolist())
            conseil_transfert = (
                f"Sous-charge CS : Detachement possible vers [{noms_sur}] "
                "(meme region)."
            )

    recos_list.append({
        "Agence": row["Agence"].replace("-", " "),
        "Region": row["Région"],
        "MV Actuels": row["MV"],
        "CS Actuels": row["Total_CS_Propose"],
        "Vol 2027 Hls": row["Vol_2027_Hls"],
        "Vol / CS": round(row["Vol_2027_Par_CS"], 0),
        "Vol / MV": round(row["Vol_2027_Par_MV"], 0),
        "PDV / CS": round(row["PDV_Par_CS"], 1),
        "Statut CS": row["Statut_CS"],
        "Statut MV": row["Statut_MV"],
        "Reco Regionale": conseil_transfert,
    })

df_recos = pd.DataFrame(recos_list)
csv_buffer = io.StringIO()
df_recos.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
st.download_button(
    label="📥 Télécharger le rapport des recommandations (CSV)",
    data=csv_buffer.getvalue(),
    file_name="recommandations_commerciales_madagascar.csv",
    mime="text/csv",
)

for _, row in df.iterrows():
    with st.expander(
        f"🏢 Agence : {row['Agence']} ({row['Région']}) — "
        f"[{row['Statut_CS']}] | [{row['Statut_MV']}]"
    ):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Effectifs", f"{row['MV']} MV | {row['Total_CS_Propose']} CS")
        c2.metric("Ratio Agence", f"{row['Ratio_CS_MV']:.1f} CS / 1 MV")
        c3.metric(
            "Vol / MV",
            f"{row['Vol_2027_Par_MV']:,.0f}",
            f"vs Nat: {row['Vol_2027_Par_MV'] - nat_vol_mv:+,.0f}",
        )
        c4.metric(
            "Vol / CS",
            f"{row['Vol_2027_Par_CS']:,.0f}",
            f"vs Nat: {row['Vol_2027_Par_CS'] - nat_vol_cs:+,.0f}",
        )

        st.markdown(
            f"- **Volume 2027 :** {row['Vol_2027_Hls']:,.0f} Hls "
            f"(Évolution: {row['Evol_Vol_Pct']:+.2f}%)"
        )
        st.markdown(
            f"- **Charge PDV :** {row['PDV_Par_CS']:.1f} PDV/CS | "
            f"**Zones Blanches :** {row['PDV_Estimes_ZB']} PDV "
            f"({row['Vol_ZB_Inclut_Mois_Hls']} Hls/mois)"
        )

        region_act = row["Région"]
        agences_reg = df[
            (df["Région"] == region_act) & (df["Agence"] != row["Agence"])
        ]
        if "Surcharge" in row["Statut_CS"]:
            sc_list = agences_reg[
                agences_reg["Statut_CS"].str.contains("Sous-charge")
            ]["Agence"].tolist()
            if sc_list:
                st.warning(
                    f"⚠️ **Suggestion Régionale :** Surcharge CS détectée. "
                    f"Possibilité d'effectuer un transfert depuis l'agence "
                    f"sous-chargée de la même région : **{', '.join(sc_list)}**, "
                    "ou recrutement local."
                )
            else:
                st.warning(
                    "⚠️ **Suggestion :** Surcharge CS sans sous-charge régionale. "
                    "**Recrutement local recommandé**."
                )
        elif "Sous-charge" in row["Statut_CS"]:
            sur_list = agences_reg[
                agences_reg["Statut_CS"].str.contains("Surcharge")
            ]["Agence"].tolist()
            if sur_list:
                st.info(
                    f"ℹ️ **Suggestion Régionale :** Sous-charge CS identifiée. "
                    f"Possibilité de détacher du personnel vers l'agence en "
                    f"surcharge de la même région : **{', '.join(sur_list)}**."
                )
        else:
            st.success("✅ **Équilibre opérationnel validé.**")

# ==========================================
# 12. RÉCAPITULATIF FINAL
# ==========================================
st.markdown("---")
st.subheader("🎯 Récapitulatif Stratégique : Propositions de Recrutement & Transferts")

recap_lignes = []
for _, row in df.iterrows():
    region_actuelle = row["Région"]
    agences_meme_region = df[
        (df["Région"] == region_actuelle) & (df["Agence"] != row["Agence"])
    ]

    action = "Maintien de l'effectif"
    if "Surcharge CS" in row["Statut_CS"]:
        sous_charges = agences_meme_region[
            agences_meme_region["Statut_CS"].str.contains("Sous-charge")
        ]
        if not sous_charges.empty:
            noms_sc = ", ".join(sous_charges["Agence"].tolist())
            action = f"Transfert depuis [{noms_sc}] (même région) ou Recrutement Local"
        else:
            action = "Recrutement Local CS (Pas de source de transfert régional)"
    elif "Sous-charge CS" in row["Statut_CS"]:
        surcharges = agences_meme_region[
            agences_meme_region["Statut_CS"].str.contains("Surcharge")
        ]
        if not surcharges.empty:
            noms_sur = ", ".join(surcharges["Agence"].tolist())
            action = f"Détachement / Transfert vers [{noms_sur}] (même région)"
        else:
            action = "Sous-charge locale (Maintien ou redéploiement zones blanches)"
    elif "Surcharge MV" in row["Statut_MV"]:
        action = "Renfort d'Encadrement MV"

    recap_lignes.append({
        "Région": row["Région"],
        "Agence": row["Agence"],
        "Volume 2027 (Hls)": f"{row['Vol_2027_Hls']:,.0f}",
        "PDV Totaux": f"{row['PDV_Total_Ajuste']:,.0f}",
        "Charge CS (PDV/CS)": f"{row['PDV_Par_CS']:.1f}",
        "Statut CS": row["Statut_CS"],
        "Statut MV": row["Statut_MV"],
        "Action Proposée": action,
    })

df_recap_final = pd.DataFrame(recap_lignes)
st.table(df_recap_final)
