SIDEBAR_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── MAIN BACKGROUND ── */
.main { background-color: #f8f7ff !important; }
.block-container { padding: 2rem 2.5rem !important; background: #f8f7ff; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4c1d95 0%, #5b21b6 40%, #6d28d9 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(76,29,149,0.3);
}
[data-testid="stSidebar"] * { color: #ede9fe !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #c4b5fd !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: white !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

/* Hide default Streamlit nav pages in sidebar */
[data-testid="stSidebarNav"] { display: none !important; }

/* ── HIDE BRANDING ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── SECTION DIVIDER ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, #7c3aed, #a78bfa, transparent);
    margin: 28px 0 20px 0;
    border: none;
}

/* ── SECTION TITLE ── */
.section-title {
    color: #1e1b4b;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid #7c3aed;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── KPI CARD ── */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 20px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(109,40,217,0.1);
    border: 1px solid #ede9fe;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(109,40,217,0.18); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #7c3aed, #a78bfa);
}
.kpi-label {
    color: #6b7280;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}
.kpi-value {
    color: #1e1b4b;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.1;
}
.kpi-delta { font-size: 12px; margin-top: 6px; font-weight: 600; }
.kpi-green { color: #059669; }
.kpi-yellow { color: #d97706; }
.kpi-red { color: #dc2626; }

/* ── CHART CARD ── */
.chart-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(109,40,217,0.08);
    border: 1px solid #ede9fe;
    margin-bottom: 20px;
}

/* ── TOUCHPOINT CARD ── */
.tp-card {
    background: white;
    border: 1px solid #ede9fe;
    border-radius: 12px;
    padding: 16px 10px;
    text-align: center;
    box-shadow: 0 1px 8px rgba(109,40,217,0.08);
    transition: transform 0.2s;
}
.tp-card:hover { transform: translateY(-2px); }
.tp-label { color: #6b7280; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; }
.tp-value { font-size: 22px; font-weight: 800; }
.tp-green { color: #059669; }
.tp-yellow { color: #d97706; }
.tp-red { color: #dc2626; }
.tp-sub { color: #9ca3af; font-size: 10px; margin-top: 4px; font-weight: 500; }

/* ── PAGE HEADER ── */
.page-header {
    background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    color: white;
    box-shadow: 0 4px 20px rgba(109,40,217,0.3);
}
.page-header h2 { color: white; font-size: 22px; font-weight: 800; margin: 0 0 4px 0; }
.page-header p { color: #c4b5fd; font-size: 13px; margin: 0; }

/* ── HORIZONTAL TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 12px;
    padding: 6px;
    gap: 4px;
    box-shadow: 0 2px 12px rgba(109,40,217,0.1);
    border: 1px solid #ede9fe;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #6b7280 !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(109,40,217,0.4) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #ede9fe; }
</style>
"""

PLOT_LIGHT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color="#374151", size=12),
)

PURPLE_COLORS = [
    "#4c1d95", "#5b21b6", "#6d28d9", "#7c3aed",
    "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe",
]

ACCENT = "#7c3aed"
SUCCESS = "#059669"
WARNING = "#d97706"
DANGER  = "#dc2626"
