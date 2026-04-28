import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

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
# DESIGN CSS UNIQUE ET MODERNE
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* Fond général avec dégradé subtil */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%);
        min-height: 100vh;
    }

    /* Barre latérale premium */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1729 0%, #1a2f5e 50%, #0f1729 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Logo sidebar */
    .sidebar-logo {
        text-align: center;
        padding: 30px 10px 20px 10px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    .sidebar-logo h1 {
        font-size: 1.3em;
        font-weight: 700;
        color: white !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 10px 0 5px 0;
    }
    .sidebar-logo p {
        font-size: 0.72em;
        color: rgba(255,255,255,0.5) !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .logo-icon {
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, #4f8ef7, #1a56db);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        font-size: 1.6em;
        box-shadow: 0 4px 15px rgba(79,142,247,0.4);
    }

    /* En-tête de page */
    .page-header {
        background: linear-gradient(135deg, #0f1729 0%, #1a2f5e 100%);
        border-radius: 16px;
        padding: 30px 35px;
        margin-bottom: 25px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(15,23,41,0.3);
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(79,142,247,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .page-header::after {
        content: '';
        position: absolute;
        bottom: -40%;
        right: 15%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(99,179,237,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .page-header h1 {
        font-size: 1.8em;
        font-weight: 700;
        margin: 0 0 6px 0;
        color: white;
        letter-spacing: 0.5px;
    }
    .page-header p {
        font-size: 0.88em;
        color: rgba(255,255,255,0.6);
        margin: 0;
        font-weight: 300;
    }
    .header-badge {
        display: inline-block;
        background: rgba(79,142,247,0.25);
        color: #7eb3ff !important;
        font-size: 0.72em;
        padding: 3px 12px;
        border-radius: 20px;
        margin-bottom: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 500;
        border: 1px solid rgba(79,142,247,0.3);
    }

    /* Cartes métriques */
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4f8ef7, #1a56db);
        border-radius: 14px 14px 0 0;
    }
    .metric-label {
        font-size: 0.75em;
        font-weight: 600;
        color: #8a9ab5;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: #0f1729;
        line-height: 1;
    }
    .metric-sub {
        font-size: 0.78em;
        color: #4f8ef7;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Cartes de section */
    .section-card {
        background: white;
        border-radius: 14px;
        padding: 25px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 20px;
        animation: fadeInUp 0.4s ease;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .section-title {
        font-size: 0.95em;
        font-weight: 700;
        color: #0f1729;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f0f4ff;
        margin-bottom: 18px;
    }

    /* Bouton principal */
    .stButton > button {
        background: linear-gradient(135deg, #1a56db 0%, #4f8ef7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 0.9em;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26,86,219,0.3);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26,86,219,0.4);
    }

    /* Bouton téléchargement */
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

    /* Champs de formulaire */
    .stTextInput > div > input,
    .stNumberInput > div > input,
    .stTextArea > div > textarea {
        border-radius: 8px;
        border: 1.5px solid #e2e8f0;
        padding: 10px 14px;
        font-size: 0.9em;
        transition: border-color 0.2s;
        background: #fafbff;
    }
    .stTextInput > div > input:focus,
    .stNumberInput > div > input:focus,
    .stTextArea > div > textarea:focus {
        border-color: #4f8ef7;
        box-shadow: 0 0 0 3px rgba(79,142,247,0.1);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1.5px solid #e2e8f0;
        background: #fafbff;
    }

    /* Alertes */
    .stSuccess {
        border-radius: 10px;
        border-left: 4px solid #10b981;
    }
    .stError {
        border-radius: 10px;
        border-left: 4px solid #ef4444;
    }
    .stWarning {
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
    }

    /* Notification succès personnalisée */
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

    /* Tableau */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    /* Divider personnalisé */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 20px 0;
    }

    /* Pied de page sidebar */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        padding: 0 20px;
        font-size: 0.72em;
        color: rgba(255,255,255,0.3) !important;
        text-align: center;
        width: 280px;
    }

    /* Masquer éléments Streamlit par défaut */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================
# FICHIER DE STOCKAGE
# ============================================
FICHIER_CSV   = "data/donnees.csv"
FICHIER_EXCEL = "data/donnees.xlsx"

if not os.path.exists("data"):
    os.makedirs("data")

# ============================================
# FONCTIONS
# ============================================
def charger_donnees():
    if os.path.exists(FICHIER_CSV):
        try:
            df = pd.read_csv(FICHIER_CSV)
            if df.empty or len(df.columns) == 0:
                return pd.DataFrame()
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def sauvegarder_donnees(nouvelle_ligne):
    df_existant = charger_donnees()
    df_nouveau  = pd.DataFrame([nouvelle_ligne])
    df_final    = pd.concat([df_existant, df_nouveau], ignore_index=True)
    df_final.to_csv(FICHIER_CSV, index=False, encoding="utf-8-sig")
    df_final.to_excel(FICHIER_EXCEL, index=False, engine="openpyxl")
    return df_final

def exporter_excel(df):
    chemin = "data/export_final.xlsx"
    with pd.ExcelWriter(chemin, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Données")
        workbook  = writer.book
        worksheet = writer.sheets["Données"]
        format_entete = workbook.add_format({
            "bold": True,
            "bg_color": "#0f1729",
            "font_color": "white",
            "border": 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, format_entete)
            worksheet.set_column(col_num, col_num, 22)
    return chemin

# ============================================
# BARRE LATERALE
# ============================================
st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">📊</div>
        <h1>DataCollect</h1>
        <p>Pro Edition</p>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("", [
    "Accueil",
    "Formulaire",
    "Analyse",
    "Données"
])

st.sidebar.markdown("""
    <div class="sidebar-footer">
        DataCollect Pro &copy; 2026<br>
        Commerce & Entreprise
    </div>
""", unsafe_allow_html=True)

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

    df = charger_donnees()
    total     = len(df) if not df.empty else 0
    secteurs  = df["Secteur"].nunique() if not df.empty and "Secteur" in df.columns else 0
    sat_moy   = round(df["Satisfaction"].mean(), 1) if not df.empty and "Satisfaction" in df.columns else 0
    ca_moy    = f"{int(df['Chiffre_Affaires'].mean()):,}".replace(",", " ") if not df.empty and "Chiffre_Affaires" in df.columns else "0"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Enregistrements</div>
                <div class="metric-value">{total}</div>
                <div class="metric-sub">Total collecté</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Secteurs</div>
                <div class="metric-value">{secteurs}</div>
                <div class="metric-sub">Secteurs couverts</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Satisfaction</div>
                <div class="metric-value">{sat_moy}</div>
                <div class="metric-sub">Moyenne sur 10</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CA Moyen</div>
                <div class="metric-value" style="font-size:1.3em;">{ca_moy}</div>
                <div class="metric-sub">FCFA</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="section-card" style="border-top: 3px solid #4f8ef7;">
                <div class="section-title">Collecte</div>
                <p style="color:#6b7280; font-size:0.88em; line-height:1.6;">
                    Saisissez les données de vos entreprises via un formulaire structuré et validé en temps réel.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="section-card" style="border-top: 3px solid #10b981;">
                <div class="section-title">Analyse</div>
                <p style="color:#6b7280; font-size:0.88em; line-height:1.6;">
                    Visualisez vos données avec des graphiques interactifs et des statistiques descriptives complètes.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="section-card" style="border-top: 3px solid #f59e0b;">
                <div class="section-title">Export</div>
                <p style="color:#6b7280; font-size:0.88em; line-height:1.6;">
                    Téléchargez vos données en format CSV ou Excel avec mise en forme professionnelle.
                </p>
            </div>
        """, unsafe_allow_html=True)

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

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Informations générales</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            nom_entreprise = st.text_input("Nom de l'entreprise *", placeholder="Ex : ABC Commerce")
            secteur = st.selectbox("Secteur d'activité *", [
                "Sélectionnez...",
                "Commerce de détail",
                "Commerce de gros",
                "Services",
                "Industrie",
                "Agriculture",
                "Technologie",
                "Autre"
            ])
        with col2:
            nom_repondant = st.text_input("Nom du répondant *", placeholder="Ex : Jean Dupont")
            taille_entreprise = st.selectbox("Taille de l'entreprise *", [
                "Sélectionnez...",
                "Micro (1-9 employés)",
                "Petite (10-49 employés)",
                "Moyenne (50-249 employés)",
                "Grande (250+ employés)"
            ])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Données commerciales</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            chiffre_affaires = st.number_input("Chiffre d'affaires annuel (FCFA)", min_value=0, step=100000)
            nb_clients = st.number_input("Nombre de clients actifs", min_value=0, step=1)
        with col4:
            nb_employes = st.number_input("Nombre d'employés", min_value=0, step=1)
            annee_creation = st.number_input("Année de création", min_value=1900, max_value=2026, step=1, value=2020)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Performance et satisfaction</div>', unsafe_allow_html=True)
        croissance = st.select_slider(
            "Taux de croissance estimé (%)",
            options=[-20, -10, -5, 0, 5, 10, 15, 20, 25, 30, 50],
            value=0
        )
        satisfaction = st.slider("Niveau de satisfaction client (1 à 10)", 1, 10, 5)
        defis = st.multiselect("Principaux défis rencontrés", [
            "Manque de financement",
            "Concurrence accrue",
            "Manque de personnel qualifié",
            "Problèmes logistiques",
            "Digitalisation",
            "Accès aux marchés",
            "Autre"
        ])
        commentaire = st.text_area("Commentaires supplémentaires", placeholder="Vos observations...")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        soumettre = st.form_submit_button("Soumettre les données")

        if soumettre:
            if not nom_entreprise or not nom_repondant or secteur == "Sélectionnez..." or taille_entreprise == "Sélectionnez...":
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                nouvelle_ligne = {
                    "Date"            : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Entreprise"      : nom_entreprise,
                    "Répondant"       : nom_repondant,
                    "Secteur"         : secteur,
                    "Taille"          : taille_entreprise,
                    "Chiffre_Affaires": chiffre_affaires,
                    "Nb_Clients"      : nb_clients,
                    "Nb_Employes"     : nb_employes,
                    "Annee_Creation"  : annee_creation,
                    "Croissance"      : croissance,
                    "Satisfaction"    : satisfaction,
                    "Defis"           : ", ".join(defis),
                    "Commentaire"     : commentaire
                }
                sauvegarder_donnees(nouvelle_ligne)
                st.markdown("""
                    <div class="success-banner">
                        Données enregistrées avec succès.
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
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Entreprises</div>
                    <div class="metric-value">{len(df)}</div>
                    <div class="metric-sub">Total</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            ca = f"{int(df['Chiffre_Affaires'].mean()):,}".replace(",", " ") if "Chiffre_Affaires" in df.columns else "N/A"
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">CA Moyen</div>
                    <div class="metric-value" style="font-size:1.2em;">{ca}</div>
                    <div class="metric-sub">FCFA</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            sat = round(df["Satisfaction"].mean(), 1) if "Satisfaction" in df.columns else "N/A"
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Satisfaction</div>
                    <div class="metric-value">{sat}</div>
                    <div class="metric-sub">Moyenne / 10</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            emp = round(df["Nb_Employes"].mean(), 1) if "Nb_Employes" in df.columns else "N/A"
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Employés</div>
                    <div class="metric-value">{emp}</div>
                    <div class="metric-sub">Moyenne</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Graphiques avec thème unifié
        COULEURS = px.colors.qualitative.Set2
        LAYOUT   = dict(
            paper_bgcolor="white",
            plot_bgcolor="#fafbff",
            font=dict(family="Inter", size=12, color="#0f1729"),
            margin=dict(t=40, b=20, l=20, r=20),
            showlegend=False
        )

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Répartition par secteur</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names="Secteur", hole=0.45,
                color_discrete_sequence=COULEURS)
            fig1.update_traces(textposition="inside", textinfo="percent+label")
            fig1.update_layout(**LAYOUT)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            sc = df["Secteur"].value_counts().reset_index()
            sc.columns = ["Secteur", "Nombre"]
            fig2 = px.bar(sc, x="Secteur", y="Nombre",
                color="Secteur", color_discrete_sequence=COULEURS)
            fig2.update_layout(**LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Chiffre d\'affaires</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig3 = px.box(df, x="Secteur", y="Chiffre_Affaires",
                color="Secteur", color_discrete_sequence=COULEURS)
            fig3.update_layout(**LAYOUT)
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            ca_m = df.groupby("Secteur")["Chiffre_Affaires"].mean().reset_index()
            ca_m.columns = ["Secteur", "CA_Moyen"]
            fig4 = px.bar(ca_m, x="Secteur", y="CA_Moyen",
                color="Secteur", color_discrete_sequence=COULEURS)
            fig4.update_layout(**LAYOUT)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Satisfaction client</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig5 = px.histogram(df, x="Satisfaction", nbins=10,
                color_discrete_sequence=["#4f8ef7"])
            fig5.update_layout(**LAYOUT)
            st.plotly_chart(fig5, use_container_width=True)
        with col2:
            ss = df.groupby("Secteur")["Satisfaction"].mean().reset_index()
            ss.columns = ["Secteur", "Satisfaction_Moyenne"]
            fig6 = px.bar(ss, x="Secteur", y="Satisfaction_Moyenne",
                color="Secteur", color_discrete_sequence=COULEURS)
            fig6.update_layout(**LAYOUT)
            st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Statistiques descriptives</div>', unsafe_allow_html=True)
        cols_num = ["Chiffre_Affaires", "Nb_Clients", "Nb_Employes", "Satisfaction", "Croissance"]
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
            <p>Tableau complet des enregistrements</p>
        </div>
    """, unsafe_allow_html=True)

    df = charger_donnees()
    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        st.markdown(f"""
            <div class="section-card">
                <div class="section-title">Enregistrements</div>
                <p style="color:#6b7280; font-size:0.88em;">{len(df)} enregistrement(s) disponible(s)</p>
            </div>
        """, unsafe_allow_html=True)

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