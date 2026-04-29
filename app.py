import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
from supabase import create_client

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="DataCollect Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# INITIALISATION SESSION STATE
# ============================================
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# ============================================
# CONNEXION SUPABASE
# ============================================
@st.cache_resource
def connexion_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def charger_donnees():
    try:
        supabase = connexion_supabase()
        response = supabase.table("donnees").select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()

def sauvegarder_donnees(nouvelle_ligne):
    try:
        supabase = connexion_supabase()
        supabase.table("donnees").insert(nouvelle_ligne).execute()
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")
        return False

def exporter_excel(df):
    chemin = "data/export_final.xlsx"
    if not os.path.exists("data"):
        os.makedirs("data")
    with pd.ExcelWriter(chemin, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Données")
        workbook  = writer.book
        worksheet = writer.sheets["Données"]
        format_entete = workbook.add_format({
            "bold": True, "bg_color": "#0f1729",
            "font_color": "white", "border": 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, format_entete)
            worksheet.set_column(col_num, col_num, 22)
    return chemin

# ============================================
# DESIGN CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .main { background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%); }

    /* Cache tout ce qui concerne la sidebar Streamlit */
    section[data-testid="stSidebar"] { display: none !important; }
    div[data-testid="collapsedControl"] { display: none !important; }

    /* Navigation fixe a gauche */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 240px;
        height: 100vh;
        background: linear-gradient(180deg, #0f1729 0%, #1a2f5e 50%, #0f1729 100%);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        padding: 0;
        box-shadow: 4px 0 20px rgba(0,0,0,0.3);
    }

    .nav-logo {
        text-align: center;
        padding: 30px 15px 20px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .nav-logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #4f8ef7, #1a56db);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        font-size: 1.5em;
        box-shadow: 0 4px 15px rgba(79,142,247,0.4);
    }
    .nav-logo h2 {
        color: white;
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0 0 4px 0;
    }
    .nav-logo p {
        color: rgba(255,255,255,0.4);
        font-size: 0.7em;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 0;
    }

    .nav-menu {
        padding: 20px 12px;
        flex: 1;
    }
    .nav-btn {
        display: block;
        width: 100%;
        padding: 12px 16px;
        margin-bottom: 6px;
        border-radius: 10px;
        color: rgba(255,255,255,0.6);
        font-size: 0.88em;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
        text-align: left;
        letter-spacing: 0.3px;
    }
    .nav-btn:hover {
        background: rgba(255,255,255,0.08);
        color: white;
    }
    .nav-btn.active {
        background: linear-gradient(135deg, #1a56db, #4f8ef7);
        color: white;
        box-shadow: 0 4px 12px rgba(26,86,219,0.4);
    }

    .nav-footer {
        padding: 15px;
        border-top: 1px solid rgba(255,255,255,0.08);
        text-align: center;
        font-size: 0.7em;
        color: rgba(255,255,255,0.25);
    }

    /* Contenu principal decale pour laisser place a la nav */
    .main-content {
        margin-left: 240px;
        padding: 25px 30px;
        min-height: 100vh;
    }

    /* En-tete */
    .page-header {
        background: linear-gradient(135deg, #0f1729 0%, #1a2f5e 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 25px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(15,23,41,0.3);
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(79,142,247,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .page-header h1 {
        font-size: 1.7em;
        font-weight: 700;
        margin: 0 0 5px 0;
        color: white;
    }
    .page-header p {
        font-size: 0.85em;
        color: rgba(255,255,255,0.6);
        margin: 0;
    }
    .header-badge {
        display: inline-block;
        background: rgba(79,142,247,0.25);
        color: #7eb3ff;
        font-size: 0.7em;
        padding: 3px 12px;
        border-radius: 20px;
        margin-bottom: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 500;
        border: 1px solid rgba(79,142,247,0.3);
    }

    /* Cartes metriques */
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 15px;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4f8ef7, #1a56db);
        border-radius: 14px 14px 0 0;
    }
    .metric-label {
        font-size: 0.72em;
        font-weight: 600;
        color: #8a9ab5;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1.9em;
        font-weight: 700;
        color: #0f1729;
        line-height: 1;
    }
    .metric-sub {
        font-size: 0.75em;
        color: #4f8ef7;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Formulaire */
    .form-card {
        background: white;
        border-radius: 16px;
        padding: 26px 30px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 18px;
        animation: fadeInUp 0.4s ease;
    }
    .form-section-title {
        font-size: 0.78em;
        font-weight: 700;
        color: #4f8ef7;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f0f4ff;
        margin-bottom: 16px;
    }

    /* Section card */
    .section-card {
        background: white;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 18px;
        animation: fadeInUp 0.4s ease;
    }
    .section-title {
        font-size: 0.88em;
        font-weight: 700;
        color: #0f1729;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f0f4ff;
        margin-bottom: 16px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* Boutons Streamlit */
    .stButton > button {
        background: linear-gradient(135deg, #1a56db 0%, #4f8ef7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 0.9em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26,86,219,0.3);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26,86,219,0.4);
    }
    .stDownloadButton > button {
        background: white;
        color: #1a56db;
        border: 2px solid #1a56db;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background: #f0f4ff;
        transform: translateY(-2px);
    }

    /* Champs formulaire */
    .stTextInput > div > input,
    .stNumberInput > div > input,
    .stTextArea > div > textarea {
        border-radius: 8px;
        border: 1.5px solid #e2e8f0;
        padding: 10px 14px;
        font-size: 0.9em;
        background: #fafbff;
        transition: border-color 0.2s;
    }
    .stTextInput > div > input:focus,
    .stNumberInput > div > input:focus,
    .stTextArea > div > textarea:focus {
        border-color: #4f8ef7;
        box-shadow: 0 0 0 3px rgba(79,142,247,0.1);
    }

    /* Notification succes */
    .success-banner {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1px solid #6ee7b7;
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 16px 20px;
        color: #065f46;
        font-weight: 500;
        font-size: 0.9em;
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 18px 0;
    }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    /* Masquer padding par defaut de Streamlit */
    .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# NAVIGATION FIXE PERSONNALISEE
# ============================================
pages = ["Accueil", "Formulaire", "Analyse", "Données"]

nav_buttons = ""
for p in pages:
    active = "active" if st.session_state.page == p else ""
    nav_buttons += f"""
        <button class="nav-btn {active}"
            onclick="window.location.href='?page={p}'">{p}
        </button>
    """

st.markdown(f"""
    <div class="nav-container">
        <div class="nav-logo">
            <div class="nav-logo-icon">📊</div>
            <h2>DataCollect</h2>
            <p>Pro Edition</p>
        </div>
        <div class="nav-menu">
            {nav_buttons}
        </div>
        <div class="nav-footer">
            DataCollect Pro &copy; 2026<br>Commerce & Entreprise
        </div>
    </div>
    <div class="main-content">
""", unsafe_allow_html=True)

# Lire le parametre de navigation dans l'URL
params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

menu = st.session_state.page

# ============================================
# NAVIGATION STREAMLIT CACHEE (pour garder
# la logique de session)
# ============================================
with st.sidebar:
    menu = st.radio("", pages,
        index=pages.index(st.session_state.page),
        key="nav_radio"
    )
    st.session_state.page = menu

# ============================================
# PAGE ACCUEIL
# ============================================
if menu == "Accueil":
    st.markdown("""
        <div class="page-header">
            <span class="header-badge">Tableau de bord</span>
            <h1>DataCollect Pro</h1>
            <p>Plateforme de collecte et d'analyse de données commerciales</p>
        </div>
    """, unsafe_allow_html=True)

    df    = charger_donnees()
    total = len(df) if not df.empty else 0
    sect  = df["secteur"].nunique() if not df.empty and "secteur" in df.columns else 0
    sat   = round(df["satisfaction"].mean(), 1) if not df.empty and "satisfaction" in df.columns else 0
    ca    = f"{int(df['chiffre_affaires'].mean()):,}".replace(",", " ") if not df.empty and "chiffre_affaires" in df.columns else "0"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Enregistrements</div>
            <div class="metric-value">{total}</div>
            <div class="metric-sub">Total collecté</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Secteurs</div>
            <div class="metric-value">{sect}</div>
            <div class="metric-sub">Secteurs couverts</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Satisfaction</div>
            <div class="metric-value">{sat}</div>
            <div class="metric-sub">Moyenne sur 10</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">CA Moyen</div>
            <div class="metric-value" style="font-size:1.3em;">{ca}</div>
            <div class="metric-sub">FCFA</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="section-card" style="border-top:3px solid #4f8ef7;">
            <div class="section-title">Collecte</div>
            <p style="color:#6b7280;font-size:0.88em;line-height:1.6;">
            Saisissez les données de vos entreprises via un formulaire structuré et validé.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="section-card" style="border-top:3px solid #10b981;">
            <div class="section-title">Analyse</div>
            <p style="color:#6b7280;font-size:0.88em;line-height:1.6;">
            Visualisez vos données avec des graphiques interactifs et statistiques complètes.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="section-card" style="border-top:3px solid #f59e0b;">
            <div class="section-title">Export</div>
            <p style="color:#6b7280;font-size:0.88em;line-height:1.6;">
            Téléchargez vos données en CSV ou Excel avec mise en forme professionnelle.</p>
        </div>""", unsafe_allow_html=True)

# ============================================
# PAGE FORMULAIRE
# ============================================
elif menu == "Formulaire":
    st.markdown("""
        <div class="page-header">
            <span class="header-badge">Saisie</span>
            <h1>Formulaire de collecte</h1>
            <p>Renseignez les informations de l'entreprise enquêtée</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("formulaire", clear_on_submit=True):

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">01 — Informations générales</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            nom_entreprise = st.text_input("Nom de l'entreprise *", placeholder="Ex : ABC Commerce")
            secteur = st.selectbox("Secteur d'activité *", [
                "Sélectionnez...", "Commerce de détail", "Commerce de gros",
                "Services", "Industrie", "Agriculture", "Technologie", "Autre"
            ])
        with col2:
            nom_repondant = st.text_input("Nom du répondant *", placeholder="Ex : Jean Dupont")
            taille_entreprise = st.selectbox("Taille de l'entreprise *", [
                "Sélectionnez...", "Micro (1-9 employés)", "Petite (10-49 employés)",
                "Moyenne (50-249 employés)", "Grande (250+ employés)"
            ])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">02 — Données commerciales</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            chiffre_affaires = st.number_input("Chiffre d'affaires annuel (FCFA)", min_value=0, step=100000)
            nb_clients = st.number_input("Nombre de clients actifs", min_value=0, step=1)
        with col4:
            nb_employes = st.number_input("Nombre d'employés", min_value=0, step=1)
            annee_creation = st.number_input("Année de création", min_value=1900, max_value=2026, step=1, value=2020)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">03 — Performance et satisfaction</div>', unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            croissance = st.select_slider(
                "Taux de croissance estimé (%)",
                options=[-20, -10, -5, 0, 5, 10, 15, 20, 25, 30, 50], value=0
            )
        with col6:
            satisfaction = st.slider("Niveau de satisfaction client (1 à 10)", 1, 10, 5)
        defis = st.multiselect("Principaux défis rencontrés", [
            "Manque de financement", "Concurrence accrue", "Manque de personnel qualifié",
            "Problèmes logistiques", "Digitalisation", "Accès aux marchés", "Autre"
        ])
        commentaire = st.text_area("Commentaires supplémentaires", placeholder="Vos observations...")
        st.markdown('</div>', unsafe_allow_html=True)

        soumettre = st.form_submit_button("Soumettre les données")

        if soumettre:
            if not nom_entreprise or not nom_repondant or secteur == "Sélectionnez..." or taille_entreprise == "Sélectionnez...":
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                nouvelle_ligne = {
                    "date"            : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "entreprise"      : nom_entreprise,
                    "repondant"       : nom_repondant,
                    "secteur"         : secteur,
                    "taille"          : taille_entreprise,
                    "chiffre_affaires": chiffre_affaires,
                    "nb_clients"      : nb_clients,
                    "nb_employes"     : nb_employes,
                    "annee_creation"  : annee_creation,
                    "croissance"      : croissance,
                    "satisfaction"    : satisfaction,
                    "defis"           : ", ".join(defis),
                    "commentaire"     : commentaire
                }
                if sauvegarder_donnees(nouvelle_ligne):
                    st.markdown("""
                        <div class="success-banner">
                            Données enregistrées avec succès dans Supabase.
                        </div>
                    """, unsafe_allow_html=True)

# ============================================
# PAGE ANALYSE
# ============================================
elif menu == "Analyse":
    st.markdown("""
        <div class="page-header">
            <span class="header-badge">Statistiques</span>
            <h1>Analyse descriptive</h1>
            <p>Visualisation et statistiques des données collectées</p>
        </div>
    """, unsafe_allow_html=True)

    df = charger_donnees()

    if df.empty:
        st.warning("Aucune donnée disponible. Veuillez remplir le formulaire d'abord.")
    else:
        COULEURS = px.colors.qualitative.Set2
        LAYOUT   = dict(
            paper_bgcolor="white", plot_bgcolor="#fafbff",
            font=dict(family="Inter", size=12, color="#0f1729"),
            margin=dict(t=40, b=20, l=20, r=20), showlegend=False
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Entreprises</div>
                <div class="metric-value">{len(df)}</div>
                <div class="metric-sub">Total</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            ca = f"{int(df['chiffre_affaires'].mean()):,}".replace(",", " ") if "chiffre_affaires" in df.columns else "N/A"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">CA Moyen</div>
                <div class="metric-value" style="font-size:1.2em;">{ca}</div>
                <div class="metric-sub">FCFA</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            sat = round(df["satisfaction"].mean(), 1) if "satisfaction" in df.columns else "N/A"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Satisfaction</div>
                <div class="metric-value">{sat}</div>
                <div class="metric-sub">Moyenne / 10</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            emp = round(df["nb_employes"].mean(), 1) if "nb_employes" in df.columns else "N/A"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Employés</div>
                <div class="metric-value">{emp}</div>
                <div class="metric-sub">Moyenne</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Répartition par secteur</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names="secteur", hole=0.45, color_discrete_sequence=COULEURS)
            fig1.update_traces(textposition="inside", textinfo="percent+label")
            fig1.update_layout(**LAYOUT)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            sc = df["secteur"].value_counts().reset_index()
            sc.columns = ["Secteur", "Nombre"]
            fig2 = px.bar(sc, x="Secteur", y="Nombre", color="Secteur", color_discrete_sequence=COULEURS)
            fig2.update_layout(**LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Chiffre d\'affaires</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig3 = px.box(df, x="secteur", y="chiffre_affaires", color="secteur", color_discrete_sequence=COULEURS)
            fig3.update_layout(**LAYOUT)
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            ca_m = df.groupby("secteur")["chiffre_affaires"].mean().reset_index()
            ca_m.columns = ["Secteur", "CA_Moyen"]
            fig4 = px.bar(ca_m, x="Secteur", y="CA_Moyen", color="Secteur", color_discrete_sequence=COULEURS)
            fig4.update_layout(**LAYOUT)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Satisfaction client</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig5 = px.histogram(df, x="satisfaction", nbins=10, color_discrete_sequence=["#4f8ef7"])
            fig5.update_layout(**LAYOUT)
            st.plotly_chart(fig5, use_container_width=True)
        with col2:
            ss = df.groupby("secteur")["satisfaction"].mean().reset_index()
            ss.columns = ["Secteur", "Satisfaction_Moyenne"]
            fig6 = px.bar(ss, x="Secteur", y="Satisfaction_Moyenne", color="Secteur", color_discrete_sequence=COULEURS)
            fig6.update_layout(**LAYOUT)
            st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Statistiques descriptives</div>', unsafe_allow_html=True)
        cols_num   = ["chiffre_affaires", "nb_clients", "nb_employes", "satisfaction", "croissance"]
        cols_dispo = [c for c in cols_num if c in df.columns]
        if cols_dispo:
            stats = df[cols_dispo].describe().round(2)
            stats.index = ["Nombre", "Moyenne", "Ecart-type", "Min", "Q1", "Mediane", "Q3", "Max"]
            st.dataframe(stats, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE DONNEES
# ============================================
elif menu == "Données":
    st.markdown("""
        <div class="page-header">
            <span class="header-badge">Base de données</span>
            <h1>Données collectées</h1>
            <p>Tableau complet — stockage permanent Supabase</p>
        </div>
    """, unsafe_allow_html=True)

    df = charger_donnees()
    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        st.markdown(f"""<div class="section-card">
            <div class="section-title">Enregistrements</div>
            <p style="color:#6b7280;font-size:0.88em;">
            {len(df)} enregistrement(s) — synchronisé avec Supabase</p>
        </div>""", unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Exporter les données</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Télécharger en CSV",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="donnees.csv",
                mime="text/csv"
            )
        with col2:
            chemin_excel = exporter_excel(df)
            with open(chemin_excel, "rb") as f:
                st.download_button(
                    label="Télécharger en Excel",
                    data=f,
                    file_name="donnees.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

st.markdown('</div>', unsafe_allow_html=True)