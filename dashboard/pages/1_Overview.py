import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ── CSS & STYLE ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #0f172a; }
.block-container { padding: 1.5rem 2rem; }
[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e293b; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

/* Nav pills di sidebar */
.nav-label { color: #64748b; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    padding: 0 0 6px 0; margin-top: 8px; }
.nav-pill { display: block; padding: 9px 14px; border-radius: 8px;
    color: #94a3b8; font-size: 13px; font-weight: 500;
    text-decoration: none; margin-bottom: 3px;
    transition: background 0.15s; cursor: pointer; }
.nav-pill:hover { background: #1e293b; color: #f1f5f9; }
.nav-pill.active { background: linear-gradient(90deg,#3b82f6,#06b6d4);
    color: #fff; font-weight: 600; }

.kpi-card { background: linear-gradient(135deg,#1e293b 0%,#0f172a 100%);
    border: 1px solid #334155; border-radius: 12px; padding: 18px 16px;
    text-align: center; position: relative; overflow: hidden; }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0;
    height:3px; background:linear-gradient(90deg,#3b82f6,#06b6d4); }
.kpi-label { color:#94a3b8; font-size:11px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px; }
.kpi-value { color:#f1f5f9; font-size:26px; font-weight:700; line-height:1.1; }
.kpi-delta { font-size:11px; margin-top:5px; }
.kpi-green { color:#10b981; } .kpi-yellow { color:#f59e0b; } .kpi-red { color:#ef4444; }

.tp-card { background:#1e293b; border:1px solid #334155; border-radius:10px;
    padding:14px 12px; text-align:center; }
.tp-label { color:#94a3b8; font-size:11px; font-weight:500;
    text-transform:uppercase; letter-spacing:0.03em; margin-bottom:6px; }
.tp-value { font-size:22px; font-weight:700; }
.tp-green { color:#10b981; } .tp-yellow { color:#f59e0b; } .tp-red { color:#ef4444; }
.tp-sub { color:#64748b; font-size:10px; margin-top:3px; }

.section-title { color:#e2e8f0; font-size:15px; font-weight:600;
    margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    def parse_nps(val):
        if pd.isna(val) or str(val).strip() == '': return np.nan
        try: return int(str(val).strip().split()[0])
        except: return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v>=9 else ('Passive' if v>=7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    tp_cols = ['overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
               'overall_banking_hall_xyz','overall_sekuriti_xyz',
               'overall_operasional_xyz','overall_parkir_xyz','overall_toilet_xyz',
               'csi_xyz','cli_xyz']
    for c in tp_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        df[c+'_pct'] = (df[c] / 6 * 100).round(1)
    return df

df_raw = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 8px 8px;'>
        <div style='font-size:18px;font-weight:700;color:#f1f5f9;'>Bank XYZ</div>
        <div style='font-size:11px;color:#64748b;margin-top:2px;'>Customer Experience Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:4px 8px 2px;'>
        <div class='nav-label'>Menu</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "Overview":            "pages/1_Overview.py",
        "Branch Intelligence": "pages/2_Branch_Intelligence.py",
        "Touchpoint":          "pages/3_Touchpoint.py",
        "Customer Behaviour":  "pages/4_Customer_Behaviour.py",
        "Competitor":          "pages/5_Competitor.py",
    }
    icons = {
        "Overview":            "▣",
        "Branch Intelligence": "◈",
        "Touchpoint":          "◎",
        "Customer Behaviour":  "◉",
        "Competitor":          "◆",
    }
    for name, path in pages.items():
        is_active = "active" if name == "Overview" else ""
        st.markdown(
            f"<a href='/{name.replace(' ','_')}' target='_self' "
            f"class='nav-pill {is_active}'>{icons[name]}&nbsp;&nbsp;{name}</a>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = ["Semua"] + sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.selectbox("Provinsi", prov_opts)

    pool = df_raw if sel_prov=="Semua" else df_raw[df_raw["provinsi"]==sel_prov]
    branch_opts = sorted(pool["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect("Cabang", branch_opts, placeholder="Semua Cabang")

    panel_opts = ["Semua","Teller","CS"]
    sel_panel = st.selectbox("Panel", panel_opts)

    usia_opts = ["Semua"] + sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.selectbox("Usia", usia_opts)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px;color:#475569;padding:0 4px;'>v2.0 · Bank XYZ Analytics</div>",
                unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov != "Semua":   df = df[df["provinsi"]==sel_prov]
if sel_branch:             df = df[df["nama_cabang"].isin(sel_branch)]
if sel_panel != "Semua":
    panel_map = {"Teller":"Teller (KUOTA 50%)","CS":"CS (KUOTA 50%)"}
    df = df[df["panel_transaksi"]==panel_map[sel_panel]]
if sel_usia != "Semua":   df = df[df["range_usia"]==sel_usia]

n = len(df)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def safe_mean(s): return s.dropna().mean() if s.dropna().shape[0]>0 else 0

PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11))

def kpi_html(label, value, suffix="", cls="kpi-green", delta=""):
    return f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}{suffix}</div>
        <div class="kpi-delta {cls}">{delta}</div>
    </div>"""

# ── METRICS ───────────────────────────────────────────────────────────────────
promoters  = (df["nps_category"]=="Promoter").sum()
detractors = (df["nps_category"]=="Detractor").sum()
passives   = (df["nps_category"]=="Passive").sum()
nps_score  = round((promoters-detractors)/n*100,1) if n>0 else 0
prom_pct   = round(promoters/n*100,1) if n>0 else 0
detr_pct   = round(detractors/n*100,1) if n>0 else 0
csi_pct    = round(safe_mean(df["csi_xyz_pct"]),1)
cli_pct    = round(safe_mean(df["cli_xyz_pct"]),1)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:20px;'>
    <div style='font-size:26px;font-weight:700;color:#f1f5f9;
                letter-spacing:-0.3px;'>Bank XYZ Customer Experience Intelligence</div>
    <div style='font-size:13px;color:#64748b;margin-top:4px;'>
        Dashboard analisis kepuasan nasabah &nbsp;·&nbsp;
        {n:,} responden terpilih &nbsp;·&nbsp;
        {cabang} kantor cabang
    </div>
</div>
""".replace("{n:,}", f"{n:,}").replace("{cabang}", str(df['nama_cabang'].nunique())),
unsafe_allow_html=True)

# ── ROW 1 — KPI CARDS ─────────────────────────────────────────────────────────
c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown(kpi_html("Total Responden", f"{n:,}", "", "kpi-green", "nasabah tersurvei"), unsafe_allow_html=True)
with c2:
    nc = "kpi-green" if nps_score>=50 else "kpi-yellow" if nps_score>=20 else "kpi-red"
    st.markdown(kpi_html("NPS Score", nps_score, "",  nc,
                         f"Promoter {prom_pct}% | Detractor {detr_pct}%"), unsafe_allow_html=True)
with c3:
    cc = "kpi-green" if csi_pct>=80 else "kpi-yellow" if csi_pct>=65 else "kpi-red"
    st.markdown(kpi_html("Kepuasan Overall", round(csi_pct/100*6,2), "", cc, "skala 1–6"), unsafe_allow_html=True)
with c4:
    # Service failure = responden yg NPS Detractor
    sf = round(detractors/n*100,1) if n>0 else 0
    sc = "kpi-red" if sf>=5 else "kpi-yellow" if sf>=2 else "kpi-green"
    st.markdown(kpi_html("Service Failure", detractors, "", sc,
                         f"{sf}% dari total responden"), unsafe_allow_html=True)
with c5:
    # CES proxy: overall_operasional
    ces = round(safe_mean(df["overall_operasional_xyz"]) if "overall_operasional_xyz" in df.columns else 0, 2)
    cc2 = "kpi-green" if ces>=4.5 else "kpi-yellow" if ces>=3.5 else "kpi-red"
    st.markdown(kpi_html("Customer Effort Score", ces, "", cc2, "kemudahan layanan cabang (skala 1–6)"),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 2 — MAP CHOROPLETH (full-width) ──────────────────────────────────────
st.markdown("<div class='section-title'>Sebaran Responden per Provinsi</div>", unsafe_allow_html=True)

import json

# Mapping nama provinsi data → NAME_1 di GeoJSON
PROV_GEO_MAP = {
    "DKI Jakarta":      "JakartaRaya",
    "Jawa Barat":       "JawaBarat",
    "Jawa Tengah":      "JawaTengah",
    "Jawa Timur":       "JawaTimur",
    "Banten":           "Banten",
    "Bali":             "Bali",
    "Sumatera Utara":   "SumateraUtara",
    "Sumatera Selatan": "SumateraSelatan",
    "Lampung":          "Lampung",
    "Riau":             "Riau",
    "Kepulauan Riau":   "KepulauanRiau",
    "Kalimantan Selatan":"KalimantanSelatan",
    "Kalimantan Timur": "KalimantanTimur",
    "Sulawesi Selatan": "SulawesiSelatan",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEO_PATH = os.path.join(BASE_DIR, "..", "indonesia_provinces.json")

with open(GEO_PATH, "r") as f:
    geojson_data = json.load(f)

prov_stats = df.groupby("provinsi").agg(
    responden=("serial_id","count"),
    nps_avg=("nps_num","mean"),
).reset_index()
prov_stats["nps_avg"]   = prov_stats["nps_avg"].round(1)
prov_stats["geo_name"]  = prov_stats["provinsi"].map(PROV_GEO_MAP)
prov_stats = prov_stats.dropna(subset=["geo_name"])

fig_choropleth = go.Figure(go.Choropleth(
    geojson=geojson_data,
    featureidkey="properties.NAME_1",
    locations=prov_stats["geo_name"],
    z=prov_stats["responden"],
    colorscale=[[0,"#1e3a5f"],[0.4,"#3b82f6"],[0.7,"#06b6d4"],[1,"#10b981"]],
    zmin=0,
    zmax=prov_stats["responden"].max(),
    marker_line_color="#334155",
    marker_line_width=0.8,
    colorbar=dict(
        title=dict(text="Jumlah<br>Responden", font=dict(color="#94a3b8", size=11)),
        thickness=18,
        len=0.8,
        x=1.0,
        tickfont=dict(color="#94a3b8", size=10),
        bgcolor="rgba(15,23,42,0.7)",
        bordercolor="#334155",
        borderwidth=1,
    ),
    customdata=prov_stats[["provinsi","responden","nps_avg"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Responden: %{customdata[1]}<br>"
        "Avg NPS: %{customdata[2]}<extra></extra>"
    ),
))

# Label angka per provinsi — pakai scattergeo di atas choropleth
PROV_COORD = {
    "DKI Jakarta":(-6.21,106.85), "Jawa Barat":(-6.92,107.62),
    "Banten":(-6.41,106.06),      "Jawa Tengah":(-7.15,110.14),
    "Jawa Timur":(-7.54,112.24),  "Bali":(-8.34,115.09),
    "Sumatera Utara":(2.07,99.22),"Sumatera Selatan":(-3.32,104.91),
    "Lampung":(-4.56,105.41),     "Riau":(0.29,101.71),
    "Kepulauan Riau":(3.95,104.50),"Kalimantan Selatan":(-3.09,115.28),
    "Kalimantan Timur":(0.54,116.42),"Sulawesi Selatan":(-3.67,119.97),
}
prov_stats["lat"] = prov_stats["provinsi"].map(lambda x: PROV_COORD.get(x,(None,None))[0])
prov_stats["lon"] = prov_stats["provinsi"].map(lambda x: PROV_COORD.get(x,(None,None))[1])
prov_label = prov_stats.dropna(subset=["lat","lon"])

fig_choropleth.add_trace(go.Scattergeo(
    lat=prov_label["lat"], lon=prov_label["lon"],
    mode="text",
    text=prov_label["responden"].astype(str),
    textfont=dict(color="#f1f5f9", size=10, family="Inter"),
    hoverinfo="skip",
))

fig_choropleth.update_layout(
    **PLOT,
    geo=dict(
        scope="asia",
        center=dict(lat=-2.5, lon=118),
        projection_scale=4.2,
        bgcolor="rgba(0,0,0,0)",
        showland=True,  landcolor="#0f172a",
        showocean=True, oceancolor="#0a1628",
        showcoastlines=True, coastlinecolor="#334155",
        showcountries=False,
        showframe=False,
        lonaxis=dict(range=[94, 142]),
        lataxis=dict(range=[-11, 6]),
    ),
    margin=dict(t=10, b=10, l=0, r=80),
    height=400,
    showlegend=False,
)
st.plotly_chart(fig_choropleth, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 3 — TOUCHPOINT CARDS ──────────────────────────────────────────────────
st.markdown("<div class='section-title'>Touchpoint Satisfaction Score</div>", unsafe_allow_html=True)

TOUCHPOINTS = [
    ("Teller",       "overall_teller_xyz_pct"),
    ("Customer Svc", "overall_cs_xyz_pct"),
    ("ATM",          "overall_atm_xyz_pct"),
    ("Banking Hall", "overall_banking_hall_xyz_pct"),
    ("Sekuriti",     "overall_sekuriti_xyz_pct"),
    ("Operasional",  "overall_operasional_xyz_pct"),
    ("Parkir",       "overall_parkir_xyz_pct"),
    ("Toilet",       "overall_toilet_xyz_pct"),
]

cols_tp = st.columns(len(TOUCHPOINTS))
for col, (label, colname) in zip(cols_tp, TOUCHPOINTS):
    val = round(safe_mean(df[colname]),1) if colname in df.columns else 0
    cls = "tp-green" if val>=80 else "tp-yellow" if val>=65 else "tp-red"
    status = "Baik" if val>=80 else "Perhatian" if val>=65 else "Kritis"
    col.markdown(f"""
    <div class="tp-card">
        <div class="tp-label">{label}</div>
        <div class="tp-value {cls}">{val}%</div>
        <div class="tp-sub">{status}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 4 — NPS GAUGE + KATEGORI NPS TOP 5 ───────────────────────────────────
col_gauge, col_nps_cat = st.columns([1, 2])

with col_gauge:
    st.markdown("<div class='section-title'>NPS Gauge</div>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=nps_score,
        delta=dict(reference=50, valueformat=".1f",
                   increasing=dict(color="#10b981"),
                   decreasing=dict(color="#ef4444")),
        gauge=dict(
            axis=dict(range=[-100,100], tickcolor="#94a3b8",
                      tickfont=dict(color="#94a3b8",size=9)),
            bar=dict(color="#3b82f6"),
            bgcolor="#1e293b", bordercolor="#334155",
            steps=[
                dict(range=[-100,0],  color="rgba(239,68,68,0.12)"),
                dict(range=[0,30],    color="rgba(245,158,11,0.12)"),
                dict(range=[30,50],   color="rgba(59,130,246,0.12)"),
                dict(range=[50,100],  color="rgba(16,185,129,0.12)"),
            ],
            threshold=dict(line=dict(color="#10b981",width=2), value=50),
        ),
        number=dict(font=dict(color="#f1f5f9",size=36)),
        title=dict(
            text=f"NPS Score<br><span style='font-size:11px;color:#94a3b8'>Promoter: {prom_pct}% | Detractor: {detr_pct}%</span>",
            font=dict(color="#e2e8f0",size=13)
        ),
    ))
    fig_gauge.update_layout(**PLOT, height=250, margin=dict(t=30,b=10,l=20,r=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    fig_donut = go.Figure(go.Pie(
        labels=["Promoter","Passive","Detractor"],
        values=[promoters, passives, detractors],
        hole=0.6,
        marker_colors=["#10b981","#f59e0b","#ef4444"],
        textfont=dict(size=10, color="white"),
        textinfo="percent",
    ))
    fig_donut.update_layout(
        **PLOT, height=180,
        margin=dict(t=0,b=0,l=0,r=0),
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8",size=10), orientation="h", x=0, y=-0.15),
        annotations=[dict(text=f"<b>{nps_score}</b>", x=0.5, y=0.5,
                          font=dict(size=20,color="#f1f5f9"), showarrow=False)],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_nps_cat:
    st.markdown("<div class='section-title'>Kategori NPS — Top 5 (XYZ vs Kompetitor)</div>", unsafe_allow_html=True)

    xyz_cat  = df["nps_xyz_kategori"].value_counts().head(5).reset_index()
    komp_cat = df["nps_komp_kategori"].value_counts().head(5).reset_index()
    xyz_cat.columns  = ["Kategori", "XYZ"]
    komp_cat.columns = ["Kategori", "Kompetitor"]

    merged_cat = xyz_cat.merge(komp_cat, on="Kategori", how="outer").fillna(0)
    merged_cat["XYZ"]        = merged_cat["XYZ"].astype(int)
    merged_cat["Kompetitor"] = merged_cat["Kompetitor"].astype(int)
    merged_cat = merged_cat.sort_values("XYZ", ascending=False)

    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(
        name="XYZ",
        x=merged_cat["Kategori"],
        y=merged_cat["XYZ"],
        marker_color="#3b82f6",
        text=merged_cat["XYZ"],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
    ))
    fig_cat.add_trace(go.Bar(
        name="Kompetitor",
        x=merged_cat["Kategori"],
        y=merged_cat["Kompetitor"],
        marker_color="#f59e0b",
        text=merged_cat["Kompetitor"],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
    ))
    fig_cat.update_layout(
        **PLOT,
        barmode="group",
        xaxis=dict(
            color="#94a3b8",
            tickangle=-20,
            tickfont=dict(size=10),
            automargin=True,
        ),
        yaxis=dict(color="#94a3b8", gridcolor="#1e293b", title="Jumlah Responden"),
        legend=dict(font=dict(color="#94a3b8", size=11), orientation="h", x=0, y=1.12),
        margin=dict(t=40, b=80, l=10, r=10),
        height=430,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 5 — TOP 5 & BOTTOM 5 CABANG NPS ──────────────────────────────────────
st.markdown("<div class='section-title'>Top 5 & Bottom 5 Cabang — NPS</div>", unsafe_allow_html=True)

cabang_nps = df.groupby(["nama_cabang","provinsi"]).agg(
    responden=("serial_id","count"),
    nps_avg=("nps_num","mean"),
    promoter_pct=("nps_category", lambda x: (x=="Promoter").mean()*100),
).reset_index()
cabang_nps["nps_avg"]      = cabang_nps["nps_avg"].round(1)
cabang_nps["promoter_pct"] = cabang_nps["promoter_pct"].round(1)

top5    = cabang_nps.nlargest(5,"promoter_pct")[["nama_cabang","provinsi","responden","nps_avg","promoter_pct"]]
bottom5 = cabang_nps.nsmallest(5,"promoter_pct")[["nama_cabang","provinsi","responden","nps_avg","promoter_pct"]]
top5.columns = bottom5.columns = ["Cabang","Provinsi","Resp","NPS Avg","Promoter %"]

t1, t2 = st.columns(2)
with t1:
    st.markdown("<p style='color:#10b981;font-size:12px;font-weight:600;margin-bottom:6px;'>Top 5 Cabang</p>", unsafe_allow_html=True)
    st.dataframe(top5.reset_index(drop=True), use_container_width=True, height=220)
with t2:
    st.markdown("<p style='color:#ef4444;font-size:12px;font-weight:600;margin-bottom:6px;'>Bottom 5 Cabang</p>", unsafe_allow_html=True)
    st.dataframe(bottom5.reset_index(drop=True), use_container_width=True, height=220)