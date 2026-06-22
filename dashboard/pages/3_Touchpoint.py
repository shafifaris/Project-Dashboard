import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import sys

# ══════════════════════════════════════════════════════════════════════════════
# IMPORT CSS & ICONS DARI STYLE.PY
# ══════════════════════════════════════════════════════════════════════════════
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import SIDEBAR_CSS, PLOT, icon

# Inject Global CSS
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    def parse_nps(v):
        if pd.isna(v) or str(v).strip() == '': return np.nan
        try: return int(str(v).strip().split()[0])
        except: return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v >= 9 else ('Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    # Overall touchpoints + CSI
    overall_cols = [
        'csi_xyz',
        'overall_teller_xyz',   'overall_teller_komp',
        'overall_cs_xyz',       'overall_cs_komp',
        'overall_atm_xyz',      'overall_atm_komp',
        'overall_banking_hall_xyz', 'overall_banking_hall_komp',
        'overall_sekuriti_xyz', 'overall_sekuriti_komp',
        'overall_operasional_xyz','overall_operasional_komp',
        'overall_parkir_xyz',   'overall_parkir_komp',
        'overall_toilet_xyz',   'overall_toilet_komp',
        'waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi',
        'waktu_ideal_tambah_teller',
        'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi',
        'waktu_ideal_tambah_cs',
    ]

    # Brand image (Performance di IPA)
    img_cols = [
        'img_terkenal_xyz','img_rasa_aman_xyz','img_dihargai_xyz','img_reputasi_xyz',
        'img_produk_lengkap_xyz','img_investasi_xyz','img_kemudahan_transaksi_xyz',
        'img_teknologi_xyz','img_reward_xyz','img_echannel_xyz',
    ]
    
    # Importance
    imp_cols = [
        'imp_terkenal','imp_rasa_aman','imp_dihargai','imp_reputasi',
        'imp_produk_lengkap','imp_investasi','imp_kemudahan_transaksi',
        'imp_teknologi','imp_reward','imp_echannel',
    ]

    # Teller attrs
    teller_attrs = sorted([c for c in df.columns if c.startswith('tp_teller_') and c.endswith('_xyz')])
    cs_attrs     = sorted([c for c in df.columns if c.startswith('tp_cs_')     and c.endswith('_xyz')])
    atm_attrs    = sorted([c for c in df.columns if c.startswith('tp_atm_')    and c.endswith('_xyz')])
    bh_attrs     = sorted([c for c in df.columns if c.startswith('tp_bh_')     and c.endswith('_xyz')])
    satpam_attrs = sorted([c for c in df.columns if c.startswith('tp_satpam_') and c.endswith('_xyz')])
    ca_attrs     = sorted([c for c in df.columns if c.startswith('tp_ca_')     and c.endswith('_xyz')])

    all_tp_attrs = teller_attrs + cs_attrs + atm_attrs + bh_attrs + satpam_attrs + ca_attrs

    for c in overall_cols + img_cols + imp_cols + all_tp_attrs:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Convert scale 1-6 → 0-100 for overall + tp attrs
    scale6_cols = [c for c in overall_cols if c not in (
        'waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi','waktu_ideal_tambah_teller',
        'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi','waktu_ideal_tambah_cs'
    )]
    for c in scale6_cols + all_tp_attrs:
        if c in df.columns:
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    return df, teller_attrs, cs_attrs, atm_attrs, bh_attrs, satpam_attrs, ca_attrs

df_raw, teller_attrs, cs_attrs, atm_attrs, bh_attrs, satpam_attrs, ca_attrs = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 10px 14px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:14px;'>
        <div style='font-family:"Plus Jakarta Sans",sans-serif;font-weight:800;font-size:21px;color:#f1f5f9;'>Bank XYZ</div>
        <div style='font-size:9.5px;color:#475569;margin-top:3px;
                    text-transform:uppercase;letter-spacing:0.1em;'>
            Customer Experience Intelligence
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='nav-label'>Menu</div>", unsafe_allow_html=True)
    pages = {
        "Overview":            "/Overview",
        "Branch Intelligence": "/Branch_Intelligence",
        "Touchpoint":          "/Touchpoint",
        "Customer Behaviour":  "/Customer_Behaviour",
        "Competitor":          "/Competitor",
    }
    nav_icons = {
        "Overview":"layout-grid",
        "Branch Intelligence":"map-pin",
        "Touchpoint":"target",
        "Customer Behaviour":"users",
        "Competitor":"compass"
    }
    
    for name, path in pages.items():
        active = "active" if name == "Touchpoint" else ""
        st.markdown(
            f"<a href='{path}' target='_self' class='nav-pill {active}'>"
            f"{icon(nav_icons[name], size=15)}<span>{name}</span></a>",
            unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.multiselect("Provinsi", prov_opts, placeholder="Semua Provinsi")

    if sel_prov:
        pool = df_raw[df_raw["provinsi"].isin(sel_prov)]
    else:
        pool = df_raw
    
    kota_opts = sorted(pool["kab_kota"].dropna().unique().tolist())
    sel_kota = st.multiselect("Kota/Kabupaten", kota_opts, placeholder="Semua Kota/Kab")
    if sel_kota:
        pool2 = pool[pool["kab_kota"].isin(sel_kota)]
    else:
        pool2 = pool
    
    branch_opts = sorted(pool["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect("Cabang", branch_opts, placeholder="Semua Cabang")

    panel_opts = ["Semua", "Teller", "CS"]
    sel_panel = st.selectbox("Panel", panel_opts)

    usia_opts = sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.multiselect("Usia", usia_opts, placeholder="Semua Usia")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:#334155;padding:0 4px;'>v5.0 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov and "Semua" not in sel_prov:   
    df = df[df["provinsi"].isin(sel_prov)]
if sel_kota:
    df = df[df["kab_kota"].isin(sel_kota)]
if sel_branch:             
    df = df[df["nama_cabang"].isin(sel_branch)]
if sel_panel != "Semua":
    panel_map = {"Teller": "Teller (KUOTA 50%)", "CS": "CS (KUOTA 50%)"}
    df = df[df["panel_transaksi"] == panel_map[sel_panel]]
if sel_usia:
    df = df[df["range_usia"].isin(sel_usia)]

n = len(df)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def pct_label(v): return "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")
def pct_color(v): return "#16a34a" if v >= 80 else ("#d97706" if v >= 65 else "#dc2626")
def pct_bg(v):    return "#dcfce7" if v >= 80 else ("#fef9c3" if v >= 65 else "#fee2e2")
def pct_txt(v):   return "#166534" if v >= 80 else ("#854d0e" if v >= 65 else "#991b1b")

def render_html(html: str, container=None):
    cleaned = "\n".join(line.lstrip() for line in html.strip().split("\n"))
    target = container if container is not None else st
    target.markdown(cleaned, unsafe_allow_html=True)

# Clean label dari nama kolom
def clean_label(col, prefix):
    lbl = col.replace(prefix, "").replace("_xyz", "").replace("_", " ").title()
    return lbl

# ══════════════════════════════════════════════════════════════════════════════
# TOUCHPOINT DATA MASTER
# ══════════════════════════════════════════════════════════════════════════════
TOUCHPOINTS = [
    ("Sekuriti",     "overall_sekuriti_xyz",      "overall_sekuriti_komp",      "shield-check"),
    ("Banking Hall", "overall_banking_hall_xyz",  "overall_banking_hall_komp",  "building-2"),
    ("Teller",       "overall_teller_xyz",        "overall_teller_komp",        "user-check"),
    ("Customer Svc", "overall_cs_xyz",            "overall_cs_komp",            "users"),
    ("ATM",          "overall_atm_xyz",           "overall_atm_komp",           "layout-grid"),
    ("Operasional",  "overall_operasional_xyz",   "overall_operasional_komp",   "zap"),
    ("Parkir",       "overall_parkir_xyz",        "overall_parkir_komp",        "map-pin"),
    ("Toilet",       "overall_toilet_xyz",        "overall_toilet_komp",        "info"),
]

# Journey order untuk blueprint
BLUEPRINT_ORDER = [
    ("Parkir",       "overall_parkir_xyz"),
    ("Banking Hall", "overall_banking_hall_xyz"),
    ("Sekuriti",     "overall_sekuriti_xyz"),
    ("Teller",       "overall_teller_xyz"),
    ("Customer Svc", "overall_cs_xyz"),
    ("ATM",          "overall_atm_xyz"),
]

tp_data = []
for label, col_xyz, col_komp, icn_name in TOUCHPOINTS:
    val_xyz  = round(safe_mean(df[col_xyz])  / 6 * 100, 1) if col_xyz  in df.columns else 0.0
    val_komp = round(safe_mean(df[col_komp]) / 6 * 100, 1) if col_komp in df.columns else 0.0
    tp_data.append({
        "label": label, "icon": icn_name,
        "xyz": val_xyz, "komp": val_komp,
        "col_xyz": col_xyz, "col_komp": col_komp,
    })

tp_sorted = sorted(tp_data, key=lambda x: x["xyz"], reverse=True)

# IPA pairs Mapping Pasti (Berdasarkan instruksi "awalnya imp_")
IPA_PAIRS = [
    ("Terkenal",             "imp_terkenal",             "img_terkenal_xyz"),
    ("Rasa Aman",            "imp_rasa_aman",            "img_rasa_aman_xyz"),
    ("Dihargai",             "imp_dihargai",             "img_dihargai_xyz"),
    ("Reputasi",             "imp_reputasi",             "img_reputasi_xyz"),
    ("Produk Lengkap",       "imp_produk_lengkap",       "img_produk_lengkap_xyz"),
    ("Investasi",            "imp_investasi",            "img_investasi_xyz"),
    ("Kemudahan Transaksi",  "imp_kemudahan_transaksi",  "img_kemudahan_transaksi_xyz"),
    ("Teknologi",            "imp_teknologi",            "img_teknologi_xyz"),
    ("Reward",               "imp_reward",               "img_reward_xyz"),
    ("E-Channel",            "imp_echannel",             "img_echannel_xyz"),
]

# Deep-dive per touchpoint
DEEPDIVE_MAP = {
    "Teller":       (teller_attrs,  "tp_teller_",  "_xyz"),
    "Customer Svc": (cs_attrs,      "tp_cs_",      "_xyz"),
    "ATM":          (atm_attrs,     "tp_atm_",     "_xyz"),
    "Banking Hall": (bh_attrs,      "tp_bh_",      "_xyz"),
    "Sekuriti":     (satpam_attrs,  "tp_satpam_",  "_xyz"),
    "CA":           (ca_attrs,      "tp_ca_",      "_xyz"),
}

# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">{icon("target", size=13)} Bank XYZ · Touchpoint Intelligence</div>
    <h2>Touchpoint Analysis</h2>
    <p>{n:,} responden &nbsp;·&nbsp; {df['nama_cabang'].nunique()} kantor cabang
       &nbsp;·&nbsp; {df['provinsi'].nunique()} provinsi</p>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — DRIVER ANALYSIS (korelasi vs NPS)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("bar-chart-3", size=14)} Driver Analysis — Impact terhadap NPS</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_drv, col_ipa = st.columns([2, 3])

corr_rows = []
for tp in tp_data:
    col = tp["col_xyz"] + "_pct"
    if col in df.columns and "nps_num" in df.columns:
        sub = df[[col, "nps_num"]].dropna()
        if len(sub) > 10:
            c = sub.corr().iloc[0, 1]
            corr_rows.append({"label": tp["label"], "icon": tp["icon"],
                              "corr": round(c, 3), "xyz": tp["xyz"]})

corr_df = pd.DataFrame(corr_rows).sort_values("corr", ascending=False) if corr_rows else pd.DataFrame()

with col_drv:
    if not corr_df.empty:
        impact_labels = []
        for c in corr_df["corr"]:
            if c >= 0.35:
                impact_labels.append("Tinggi")
            elif c >= 0.15:
                impact_labels.append("Sedang")
            else:
                impact_labels.append("Rendah")

        fig_drv2 = go.Figure()

        # bubble background
        fig_drv2.add_trace(go.Scatter(
            x=corr_df["corr"],
            y=corr_df["label"],
            mode="markers",
            marker=dict(
                size=32,
                color=["rgba(220,38,38,0.12)" if c >= 0.35
                       else "rgba(245,158,11,0.12)" if c >= 0.15
                       else "rgba(148,163,184,0.15)"
                       for c in corr_df["corr"]],
                line=dict(width=0),
            ),
            hoverinfo="skip",
            showlegend=False,
        ))

        # stem (garis dari 0 ke titik)
        for i, (_, row) in enumerate(corr_df.iterrows()):
            clr = "#dc2626" if row["corr"] >= 0.35 else "#f59e0b" if row["corr"] >= 0.15 else "#94a3b8"
            fig_drv2.add_shape(
                type="line",
                x0=0, x1=row["corr"],
                y0=row["label"], y1=row["label"],
                line=dict(color=clr, width=2),
            )

        # lollipop dot
        fig_drv2.add_trace(go.Scatter(
            x=corr_df["corr"],
            y=corr_df["label"],
            mode="markers+text",
            marker=dict(
                size=14,
                color=["#dc2626" if c >= 0.35
                       else "#f59e0b" if c >= 0.15
                       else "#94a3b8"
                       for c in corr_df["corr"]],
                line=dict(color="white", width=2),
            ),
            text=[f"r={v:.3f}  {lbl}"
                  for v, lbl in zip(corr_df["corr"], impact_labels)],
            textposition="middle right",
            textfont=dict(size=10, color="#374151", family="Plus Jakarta Sans"),
            hovertemplate="<b>%{y}</b><br>Korelasi: %{x:.3f}<extra></extra>",
            showlegend=False,
        ))

        fig_drv2.add_vline(
            x=0.35, line_dash="dot",
            line=dict(color="#dc2626", width=1.5),
            annotation_text="Threshold Tinggi (0.35)",
            annotation_font=dict(size=9, color="#dc2626", family="Plus Jakarta Sans"),
        )

        fig_drv2.update_layout(
            **PLOT,
            xaxis=dict(
                title="Korelasi Pearson (r)",
                range=[-0.05, max(corr_df["corr"].max() + 0.25, 0.6)],
                gridcolor="#f1f5f9",
                tickfont=dict(color="#64748b", family="Plus Jakarta Sans"),
                zeroline=True,
                zerolinecolor="#cbd5e1",
                zerolinewidth=1.5,
            ),
            yaxis=dict(tickfont=dict(color="#1e293b", size=12, family="Plus Jakarta Sans")),
            margin=dict(t=10, b=10, l=10, r=80),
            height=460,
        )

        render_html("""
        <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;
                    padding:16px 20px 4px;box-shadow:0 2px 12px rgba(0,0,0,0.06);
                    height:88px;overflow:hidden;margin-bottom:12px;">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.09em;color:#64748b;margin-bottom:2px;">
                Pengaruh Touchpoint → NPS
            </div>
            <div style="font-size:11px;color:#94a3b8;margin-bottom:2px;">
                Korelasi Pearson · Merah = Tinggi · Kuning = Sedang · Abu = Rendah
            </div>
        </div>""")
        st.plotly_chart(fig_drv2, use_container_width=True, key="drv_left")

ipa_rows = []
for label, imp_col, perf_col in IPA_PAIRS:
    if imp_col in df.columns and perf_col in df.columns:
        imp_val  = round(safe_mean(df[imp_col])  / 6 * 100, 1)
        perf_val = round(safe_mean(df[perf_col]) / 6 * 100, 1)
        ipa_rows.append({
            "Atribut": label,
            "Importance": imp_val,
            "Performance": perf_val,
        })

with col_ipa:
    if ipa_rows:
        ipa_df = pd.DataFrame(ipa_rows)
        avg_i = ipa_df["Importance"].mean()
        avg_p = ipa_df["Performance"].mean()

        def get_quadrant(row):
            if row["Importance"] >= avg_i and row["Performance"] < avg_p:
                return "Priority Improvement", "#fee2e2", "#991b1b"
            elif row["Importance"] >= avg_i and row["Performance"] >= avg_p:
                return "Maintain Performance", "#dcfce7", "#166534"
            elif row["Importance"] < avg_i and row["Performance"] >= avg_p:
                return "Possible Overkill", "#fef9c3", "#854d0e"
            else:
                return "Low Priority", "#f1f5f9", "#475569"

        ipa_df[["Quadrant","QBG","QTX"]] = ipa_df.apply(
            lambda r: pd.Series(get_quadrant(r)), axis=1)

        QCOLORS = {
            "Priority Improvement": "#dc2626",
            "Maintain Performance": "#16a34a",
            "Possible Overkill":    "#d97706",
            "Low Priority":         "#64748b",
        }

        fig_ipa = go.Figure()

        # Quadrant background shading
        fig_ipa.add_shape(type="rect", x0=0, x1=avg_p, y0=avg_i, y1=110, fillcolor="rgba(220,38,38,0.10)", line_width=0)
        fig_ipa.add_shape(type="rect", x0=avg_p, x1=110, y0=avg_i, y1=110, fillcolor="rgba(22,163,74,0.10)", line_width=0)
        fig_ipa.add_shape(type="rect", x0=0, x1=avg_p, y0=0, y1=avg_i, fillcolor="rgba(100,116,139,0.10)", line_width=0)
        fig_ipa.add_shape(type="rect", x0=avg_p, x1=110, y0=0, y1=avg_i, fillcolor="rgba(217,119,6,0.10)", line_width=0)

        for q, clr in QCOLORS.items():
            sub = ipa_df[ipa_df["Quadrant"] == q]
            if sub.empty: continue
            fig_ipa.add_trace(go.Scatter(
                x=sub["Performance"], y=sub["Importance"],
                mode="markers+text",
                name=q,
                marker=dict(size=18, color=clr, line=dict(color="white", width=2), symbol="circle"),
                text=sub["Atribut"],
                textposition="top center",
                textfont=dict(size=10, color="#1e293b", family="Plus Jakarta Sans", weight="bold"),
            ))

        fig_ipa.add_vline(x=avg_p, line_dash="dash", line=dict(color="#94a3b8", width=1.5))
        fig_ipa.add_hline(y=avg_i, line_dash="dash", line=dict(color="#94a3b8", width=1.5))

        for lbl, xf, yf, clr in [
            ("PRIORITY\nIMPROVEMENT", 0.20, 0.93, "#dc2626"),
            ("MAINTAIN\nPERFORMANCE", 0.78, 0.93, "#16a34a"),
            ("LOW PRIORITY",           0.20, 0.07, "#64748b"),
            ("POSSIBLE OVERKILL",      0.78, 0.07, "#d97706"),
        ]:
            fig_ipa.add_annotation(
                xref="paper", yref="paper", x=xf, y=yf,
                text=lbl.replace("\n","<br>"), showarrow=False,
                font=dict(size=8, color=clr, family="Plus Jakarta Sans", weight="bold"), opacity=0.6,
            )

        fig_ipa.update_layout(
            **PLOT,
            xaxis=dict(title="Performance — Brand Image Score (%)", range=[94, 100], gridcolor="#f1f5f9", ticksuffix="%", tickfont=dict(color="#64748b", family="Plus Jakarta Sans")),
            yaxis=dict(title="Importance Score (%)", range=[94, 100], gridcolor="#f1f5f9", ticksuffix="%", tickfont=dict(color="#64748b", family="Plus Jakarta Sans")),
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center", font=dict(size=10, color="#374151", family="Plus Jakarta Sans"), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=10, b=60, l=10, r=10),
            height=460,
        )
        
        render_html("""
        <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:16px 20px 4px;box-shadow:0 2px 12px rgba(0,0,0,0.06);height:88px;overflow:hidden;margin-bottom:12px;">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:4px;">IPA Matrix — Importance vs Performance</div>
            <div style="font-size:11px;color:#94a3b8;line-height:1.4;">Importance: rata-rata skor imp_. Performance: rata-rata skor img_xyz. Garis putus = rata-rata masing-masing sumbu.</div>
        </div>""")
        st.plotly_chart(fig_ipa, use_container_width=True, key="ipa_matrix")
    else:
        st.warning("Data IPA Matrix kosong. Pastikan menekan 'C' di keyboard lalu 'R' untuk menghapus cache dan memuat ulang file Excel terbaru.")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — WAITING TIME ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("clock", size=14)} Waiting Time Analysis</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_wt1, col_wt2 = st.columns(2)

def render_waiting_card(col_obj, service, col_aktual, col_toleransi, col_ideal, chart_key):
    aktual_mean    = round(safe_mean(df[col_aktual]),   1)  if col_aktual    in df.columns else 0.0
    toleransi_mean = round(safe_mean(df[col_toleransi]),1)  if col_toleransi in df.columns else 0.0
    ideal_mean     = round(safe_mean(df[col_ideal]),    1)  if col_ideal     in df.columns else 0.0
    gap = round(aktual_mean - toleransi_mean, 1)
    gap_sign = "+" if gap >= 0 else ""
    gap_color = "#dc2626" if gap > 0 else "#16a34a"
    gap_label = f"Melebihi toleransi {abs(gap)} mnt" if gap > 0 else f"<=toleransi {abs(gap)} mnt"

    with col_obj:
        render_html(f"""
        <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:4px;">⏱ Waiting Time · {service}</div>
            <div style="font-size:11px;color:#94a3b8;margin-bottom:14px;">Aktual vs Toleransi nasabah</div>
            <div style="display:flex; gap:12px; margin-bottom:14px;">
                <div style="flex:1; background:#f8fafc; border-radius:10px; padding:10px 14px; border:1px solid #e2e8f0;">
                    <div style="font-size:9.5px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Aktual</div>
                    <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:22px; font-weight:800; color:#dc2626; line-height:1;">{aktual_mean}</div>
                    <div style="font-size:10px; color:#94a3b8; margin-top:2px;">menit</div>
                </div>
                <div style="flex:1; background:#f8fafc; border-radius:10px; padding:10px 14px; border:1px solid #e2e8f0;">
                    <div style="font-size:9.5px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Toleransi</div>
                    <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:22px; font-weight:800; color:#16a34a; line-height:1;">{toleransi_mean}</div>
                    <div style="font-size:10px; color:#94a3b8; margin-top:2px;">menit</div>
                </div>
                <div style="flex:1; background:#f8fafc; border-radius:10px; padding:10px 14px; border:1px solid #e2e8f0;">
                    <div style="font-size:9.5px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Gap</div>
                    <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:22px; font-weight:800; color:{gap_color}; line-height:1;">{gap_sign}{gap}</div>
                    <div style="font-size:10px; color:#94a3b8; margin-top:2px;">{gap_label}</div>
                </div>
                <div style="flex:1; background:#f8fafc; border-radius:10px; padding:10px 14px; border:1px solid #e2e8f0;">
                    <div style="font-size:9.5px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Ideal Staf</div>
                    <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:22px; font-weight:800; color:#d97706; line-height:1;">{ideal_mean}</div>
                    <div style="font-size:10px; color:#94a3b8; margin-top:2px;">menit</div>
                </div>
            </div>
        </div>""")

        # Chart per cabang
        wt_sub = df[["nama_cabang", col_aktual, col_toleransi]].dropna()
        if len(wt_sub) > 0:
            wt_grp = wt_sub.groupby("nama_cabang").mean().reset_index()
            wt_grp = wt_grp.sort_values(col_aktual, ascending=False).head(15)
            marker_clrs = [
                "#dc2626" if a > t else "#16a34a"
                for a, t in zip(wt_grp[col_aktual], wt_grp[col_toleransi])
            ]
            fig_wt = go.Figure()
            fig_wt.add_trace(go.Bar(
                name="Aktual", x=wt_grp["nama_cabang"], y=wt_grp[col_aktual],
                marker=dict(color=marker_clrs, line=dict(color="white", width=1)),
            ))
            fig_wt.add_trace(go.Scatter(
                name="Toleransi", x=wt_grp["nama_cabang"], y=wt_grp[col_toleransi],
                mode="lines+markers",
                line=dict(color="#f59e0b", dash="dash", width=2),
                marker=dict(size=6, color="#f59e0b"),
            ))
            fig_wt.update_layout(
                **PLOT,
                xaxis=dict(
                    tickangle=-35, tickfont=dict(size=9, color="#64748b", family="Plus Jakarta Sans"),
                    gridcolor="#f1f5f9",
                ),
                yaxis=dict(
                    title="Menit",
                    gridcolor="#f1f5f9",
                    tickfont=dict(color="#64748b", family="Plus Jakarta Sans"),
                ),
                legend=dict(
                    orientation="h", y=-0.3, x=0.5, xanchor="center",
                    font=dict(size=10, color="#374151", family="Plus Jakarta Sans"),
                ),
                margin=dict(t=10, b=80, l=10, r=10),
                height=300,
            )
            render_html(f"""
            <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06);margin-top:10px;">
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:10px;">Per Cabang — {service} (Top 15 Tunggu Terlama)</div>
            """)
            st.plotly_chart(fig_wt, use_container_width=True, key=chart_key)
            render_html("</div>")

render_waiting_card(col_wt1, "Teller",
                    "waktu_tunggu_teller_aktual", "waktu_tunggu_teller_toleransi",
                    "waktu_ideal_tambah_teller", "wt_teller")
render_waiting_card(col_wt2, "Customer Service",
                    "waktu_tunggu_cs_aktual", "waktu_tunggu_cs_toleransi",
                    "waktu_ideal_tambah_cs", "wt_cs")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — PAIN POINT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
render_html(f"""<div class="section-label">
<span class="section-label-text">{icon("alert-triangle", size=14)} Pain Point Analysis — 5 Atribut Terendah per Touchpoint</span>
<div class="section-label-line"></div>
</div>""")

PAIN_MAP = {
    "ATM":          (atm_attrs,     "tp_atm_",     "layout-grid"),
    "Customer Svc": (cs_attrs,      "tp_cs_",      "users"),
    "Teller":       (teller_attrs,  "tp_teller_",  "user-check"),
    "Banking Hall": (bh_attrs,      "tp_bh_",      "building-2"),
    "Sekuriti":     (satpam_attrs,  "tp_satpam_",  "shield-check"),
    "CA":           (ca_attrs,      "tp_ca_",      "info"),
}

pain_cols = st.columns(6)

for col_pain, (tp_label, (attrs_list, prefix_str, icn_name)) in zip(pain_cols, PAIN_MAP.items()):
    avail = [c for c in attrs_list if c in df.columns]
    if not avail:
        render_html("""
        <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;
                    padding:16px 14px;box-shadow:0 2px 12px rgba(0,0,0,0.06);
                    min-height:260px;display:flex;align-items:center;justify-content:center;">
            <div style="text-align:center;color:#94a3b8;font-size:11px;">Tidak ada data</div>
        </div>""", container=col_pain)
        continue

    pain_rows = []
    for col in avail:
        pct_col = col + "_pct"
        val = round(
            safe_mean(df[pct_col]) if pct_col in df.columns
            else safe_mean(df[col]) / 6 * 100, 1
        )
        lbl = clean_label(col, prefix_str).replace(" Xyz", "").strip()
        pain_rows.append({"attr": lbl, "val": val})

    pain_df_plot = pd.DataFrame(pain_rows).sort_values("val").head(5).reset_index(drop=True)
    max_v = pain_df_plot["val"].max() if len(pain_df_plot) > 0 else 1

    rows_html = ""
    for i, row in pain_df_plot.iterrows():
        v       = row["val"]
        bar_w   = int(v / 100 * 100)
        bar_clr = pct_color(v)
        
        rank_style = (
            "background:#dc2626;color:white;" if i == 0 else
            "background:#f59e0b;color:white;" if i == 1 else
            "background:#f1f5f9;color:#64748b;"
        )
        rows_html += f"""
        <tr style="height: 48px;"> <td style="padding:4px 4px 4px 0;vertical-align:middle;width:20px;">
                <span style="display:inline-flex;align-items:center;justify-content:center;
                             width:18px;height:18px;border-radius:50%;font-size:9px;
                             font-weight:700;flex-shrink:0;{rank_style}">
                    {i+1}
                </span>
            </td>
            <td style="padding:4px 4px;vertical-align:middle;">
                <div style="font-size:10.5px;font-weight:{'700' if i==0 else '500'};
                            color:#1e293b;line-height:1.2; min-height: 26px; display: flex; align-items: center;">
                    {row['attr']}
                </div>
                <div style="margin-top:4px;height:4px;background:#f1f5f9;
                            border-radius:99px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{bar_clr};
                                border-radius:99px;"></div>
                </div>
            </td>
            <td style="padding:4px 0 4px 4px;vertical-align:middle;
                       text-align:right;white-space:nowrap;width:45px;">
                <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;
                             color:{bar_clr};font-weight:700;">
                    {v}%
                </span>
            </td>
        </tr>"""

    render_html(f"""
    <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;
                padding:16px 14px 10px;box-shadow:0 2px 12px rgba(0,0,0,0.06);
                height:100%;">
        <div style="margin-bottom:8px;color:#1e40af;">{icon(icn_name, size=18)}</div>
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.09em;color:#1e293b;margin-bottom:2px;">
            {tp_label}
        </div>
        <div style="font-size:10px;color:#64748b;margin-bottom:10px;
                    padding-bottom:8px;border-bottom:1px solid #f1f5f9;">
            5 atribut terendah
        </div>
        <table style="width:100%;border-collapse:collapse;table-layout:fixed;">
            {rows_html}
        </table>
    </div>""", container=col_pain)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — SERVICE BLUEPRINT (Customer Journey)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("map-pin", size=14)} Service Blueprint — Customer Journey</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

bp_data = []
for label, col in BLUEPRINT_ORDER:
    val = round(safe_mean(df[col]) / 6 * 100, 1) if col in df.columns else 0.0
    bp_data.append({"label": label, "val": val, "col": col})

best_val  = max(d["val"] for d in bp_data) if bp_data else 100
worst_val = min(d["val"] for d in bp_data) if bp_data else 0

# Horizontal journey bar
fig_bp = go.Figure()
bp_colors = []
for d in bp_data:
    if d["val"] == best_val:   bp_colors.append("#16a34a")
    elif d["val"] == worst_val: bp_colors.append("#dc2626")
    elif d["val"] < 65:        bp_colors.append("#dc2626")
    elif d["val"] < 80:        bp_colors.append("#d97706")
    else:                      bp_colors.append("#16a34a")

fig_bp.add_trace(go.Bar(
    x=[d["label"] for d in bp_data],
    y=[d["val"]   for d in bp_data],
    marker=dict(
        color=bp_colors,
        line=dict(color="white", width=2),
        cornerradius=6,
    ),
    text=[f"<b>{d['val']}%</b><br><span style='font-size:9.5px;font-family:Plus Jakarta Sans;'>{pct_label(d['val'])}</span>"
          for d in bp_data],
    textposition="inside",
    textfont=dict(size=12, color="white", family="Plus Jakarta Sans"),
    width=0.55,
))
fig_bp.add_hline(y=80, line_dash="dot", line_color="#16a34a",
                 annotation_text="Target 80%",
                 annotation_font=dict(size=9, color="#16a34a", family="Plus Jakarta Sans"))
fig_bp.add_hline(y=65, line_dash="dot", line_color="#d97706",
                 annotation_text="Batas Kritis 65%",
                 annotation_font=dict(size=9, color="#d97706", family="Plus Jakarta Sans"))

# Arrow annotations between bars
for i in range(len(bp_data) - 1):
    fig_bp.add_annotation(
        x=i + 0.5, y=max(bp_data[i]["val"], bp_data[i+1]["val"]) + 4,
        text="→", showarrow=False,
        font=dict(size=20, color="#94a3b8"),
    )

fig_bp.update_layout(
    **PLOT,
    xaxis=dict(
        tickfont=dict(size=12, color="#1e293b", family="Plus Jakarta Sans", weight="bold"),
        gridcolor="rgba(0,0,0,0)",
    ),
    yaxis=dict(
        range=[0, 115], ticksuffix="%",
        gridcolor="#f1f5f9",
        tickfont=dict(color="#64748b", family="Plus Jakarta Sans"),
        title="Skor (%)",
    ),
    margin=dict(t=20, b=10, l=10, r=10),
    height=360,
)

render_html("""
<div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:4px;">Perjalanan Nasabah — Skor per Tahap</div>
    <div style="font-size:11px;color:#94a3b8;margin-bottom:14px;">Urutan berdasarkan journey fisik nasabah dari parkir hingga ATM. Identifikasi bottleneck di mana pengalaman mulai menurun.</div>
""")
st.plotly_chart(fig_bp, use_container_width=True, key="blueprint")
render_html("</div>")


# Journey insight text
st.markdown("<br>", unsafe_allow_html=True)
bp_sorted_insight = sorted(bp_data, key=lambda x: x["val"])
worst_bp = bp_sorted_insight[0]
best_bp  = bp_sorted_insight[-1]

# Find where score drops
drop_point = None
for i in range(1, len(bp_data)):
    if bp_data[i]["val"] < bp_data[i-1]["val"] - 5:
        drop_point = bp_data[i]
        break

insight_html = f"""
<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;
            padding:16px 20px;display:flex;gap:24px;flex-wrap:wrap;
            box-shadow:0 2px 8px rgba(0,0,0,0.05);">
    <div style="flex:1;min-width:200px;">
        <div style="font-size:9.5px;font-weight:700;color:#64748b;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
            {icon("check-circle", size=13)} Touchpoint Terbaik
        </div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;font-weight:800;color:#16a34a;letter-spacing:-0.02em;">
            {best_bp['label']}
        </div>
        <div style="font-size:12px;color:#16a34a;font-weight:700;">{best_bp['val']}%</div>
    </div>
    <div style="flex:1;min-width:200px;">
        <div style="font-size:9.5px;font-weight:700;color:#64748b;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
            {icon("alert-triangle", size=13)} Touchpoint Terlemah
        </div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;font-weight:800;color:#dc2626;letter-spacing:-0.02em;">
            {worst_bp['label']}
        </div>
        <div style="font-size:12px;color:#dc2626;font-weight:700;">{worst_bp['val']}%</div>
    </div>
    {"<div style='flex:2;min-width:280px;'><div style='font-size:9.5px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>" + icon("arrow-down-right", size=13) + " Drop Signifikan Ditemukan</div><div style='font-size:13px;color:#1e293b;font-weight:500;line-height:1.5;'>Skor turun tajam di tahap <b>" + drop_point['label'] + f"</b> ({drop_point['val']}%). Ini titik di mana pengalaman nasabah mulai rusak.</div></div>" if drop_point else ''}
</div>"""
render_html(insight_html)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — BRANCH × TOUCHPOINT CRISIS TABLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("building-2", size=14)} Branch × Touchpoint Heatmap</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

crisis_map = {
    "CSI":         "csi_xyz_pct",
    "Teller":      "overall_teller_xyz_pct",
    "CS":          "overall_cs_xyz_pct",
    "ATM":         "overall_atm_xyz_pct",
    "Banking Hall":"overall_banking_hall_xyz_pct",
    "Sekuriti":    "overall_sekuriti_xyz_pct",
    "Operasional": "overall_operasional_xyz_pct",
    "Parkir":      "overall_parkir_xyz_pct",
    "Toilet":      "overall_toilet_xyz_pct",
}
avail_crisis = {k: v for k, v in crisis_map.items() if v in df.columns}

if avail_crisis:
    crisis_df = (
        df.groupby("nama_cabang")[list(avail_crisis.values())]
        .mean().round(1).reset_index()
    )
    crisis_df.columns = ["Cabang"] + list(avail_crisis.keys())
    num_sort = list(avail_crisis.keys())[0]
    crisis_df = crisis_df.sort_values(num_sort)

    def color_cell(val):
        if isinstance(val, (int, float)):
            if val < 65:   return "background-color:#fee2e2;color:#991b1b;font-weight:600;"
            elif val < 80: return "background-color:#fef9c3;color:#854d0e;font-weight:600;"
            else:          return "background-color:#dcfce7;color:#166534;font-weight:600;"
        return ""

    numeric_cols = [c for c in crisis_df.columns if c != "Cabang"]
    styled = crisis_df.style.map(color_cell, subset=numeric_cols)

    render_html("""
    <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:4px;">Heatmap Performa Cabang per Touchpoint</div>
        <div style="font-size:11px;color:#94a3b8;margin-bottom:14px;">Merah &lt; 65% (Kritis) · Kuning 65–79% (Perhatian) · Hijau ≥ 80% (Baik)</div>
    """)
    st.dataframe(styled, use_container_width=True, height=320)
    render_html("</div>")