import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #0f172a; } .block-container { padding: 1.5rem 2rem; }
[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e293b; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.nav-label { color:#64748b; font-size:10px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em; padding:0 0 6px 0; margin-top:8px; }
.nav-pill { display:block; padding:9px 14px; border-radius:8px; color:#94a3b8;
    font-size:13px; font-weight:500; text-decoration:none; margin-bottom:3px; }
.nav-pill:hover { background:#1e293b; color:#f1f5f9; }
.nav-pill.active { background:linear-gradient(90deg,#3b82f6,#06b6d4); color:#fff; font-weight:600; }
.section-title { color:#e2e8f0; font-size:15px; font-weight:600;
    margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    def parse_nps(v):
        if pd.isna(v) or str(v).strip()=='': return np.nan
        try: return int(str(v).strip().split()[0])
        except: return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)

    num_cols = ['overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
                'overall_banking_hall_xyz','overall_sekuriti_xyz',
                'overall_operasional_xyz','overall_parkir_xyz','overall_toilet_xyz',
                'csi_xyz','waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi',
                'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi']
    teller_attrs = [c for c in df.columns if c.startswith('tp_teller_') and c.endswith('_xyz')]
    cs_attrs     = [c for c in df.columns if c.startswith('tp_cs_')     and c.endswith('_xyz')]
    atm_attrs    = [c for c in df.columns if c.startswith('tp_atm_')    and c.endswith('_xyz')]

    for c in num_cols + teller_attrs + cs_attrs + atm_attrs:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    for c in ['overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
              'overall_banking_hall_xyz','overall_sekuriti_xyz',
              'overall_operasional_xyz','overall_parkir_xyz','overall_toilet_xyz','csi_xyz']:
        df[c+'_pct'] = (df[c]/6*100).round(1)

    for c in teller_attrs + cs_attrs + atm_attrs:
        df[c+'_pct'] = (df[c]/6*100).round(1)

    return df, teller_attrs, cs_attrs, atm_attrs

df_raw, teller_attrs, cs_attrs, atm_attrs = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 8px 8px;'>
        <div style='font-size:18px;font-weight:700;color:#f1f5f9;'>Bank XYZ</div>
        <div style='font-size:11px;color:#64748b;margin-top:2px;'>Customer Experience Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {"Overview":"/Overview","Branch Intelligence":"/Branch_Intelligence",
             "Touchpoint":"/Touchpoint","Customer Behaviour":"/Customer_Behaviour","Competitor":"/Competitor"}
    icons = {"Overview":"▣","Branch Intelligence":"◈","Touchpoint":"◎",
             "Customer Behaviour":"◉","Competitor":"◆"}
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Menu</div>", unsafe_allow_html=True)
    for name, path in pages.items():
        active = "active" if name=="Touchpoint" else ""
        st.markdown(f"<a href='{path}' target='_self' class='nav-pill {active}'>{icons[name]}&nbsp;&nbsp;{name}</a>",
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = ["Semua"] + sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.selectbox("Provinsi", prov_opts)

    pool = df_raw if sel_prov=="Semua" else df_raw[df_raw["provinsi"]==sel_prov]
    branch_opts = sorted(pool["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect("Cabang", branch_opts, placeholder="Semua Cabang")

    tp_opts = ["Semua","Teller","CS"]
    sel_tp = st.selectbox("Touchpoint", tp_opts)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#475569;padding:0 4px;'>v2.0 · Bank XYZ Analytics</div>",
                unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov != "Semua": df = df[df["provinsi"]==sel_prov]
if sel_branch:           df = df[df["nama_cabang"].isin(sel_branch)]
if sel_tp == "Teller":   df = df[df["panel_transaksi"].str.contains("Teller", na=False)]
elif sel_tp == "CS":     df = df[df["panel_transaksi"].str.contains("CS", na=False)]

n = len(df)
PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11))
def safe_mean(s): return s.dropna().mean() if s.dropna().shape[0]>0 else 0

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-bottom:20px;'>
    <div style='font-size:26px;font-weight:700;color:#f1f5f9;letter-spacing:-0.3px;'>Touchpoint Intelligence</div>
    <div style='font-size:13px;color:#64748b;margin-top:4px;'>{n:,} responden terfilter</div>
</div>
""", unsafe_allow_html=True)

# ── IPA + KORELASI ────────────────────────────────────────────────────────────
col_ipa, col_corr = st.columns([3,2])

with col_ipa:
    st.markdown("<div class='section-title'>Importance Performance Analysis (IPA)</div>", unsafe_allow_html=True)

    ipa_items = {
        "Teller":       ("overall_teller_xyz_pct",       88),
        "Customer Svc": ("overall_cs_xyz_pct",           90),
        "ATM":          ("overall_atm_xyz_pct",          85),
        "Banking Hall": ("overall_banking_hall_xyz_pct", 75),
        "Sekuriti":     ("overall_sekuriti_xyz_pct",     70),
        "Operasional":  ("overall_operasional_xyz_pct",  80),
        "Parkir":       ("overall_parkir_xyz_pct",       60),
        "Toilet":       ("overall_toilet_xyz_pct",       65),
    }

    ipa_df = pd.DataFrame([{
        "Dimensi": k,
        "Performance": round(safe_mean(df[v[0]]),1) if v[0] in df.columns else 0,
        "Importance": v[1],
    } for k,v in ipa_items.items()])

    avg_p = ipa_df["Performance"].mean()
    avg_i = ipa_df["Importance"].mean()

    def quadrant(row):
        if row["Importance"]>=avg_i and row["Performance"]<avg_p:   return "Priority Improvement"
        elif row["Importance"]>=avg_i and row["Performance"]>=avg_p: return "Maintain Performance"
        elif row["Importance"]<avg_i  and row["Performance"]>=avg_p: return "Possible Overkill"
        else: return "Low Priority"

    ipa_df["Quadrant"] = ipa_df.apply(quadrant, axis=1)
    qcolor = {"Priority Improvement":"#ef4444","Maintain Performance":"#10b981",
               "Possible Overkill":"#f59e0b","Low Priority":"#6b7280"}

    fig_ipa = go.Figure()
    fig_ipa.add_shape(type="rect",x0=0,x1=avg_p,y0=avg_i,y1=100,fillcolor="rgba(239,68,68,0.05)",line_width=0)
    fig_ipa.add_shape(type="rect",x0=avg_p,x1=110,y0=avg_i,y1=100,fillcolor="rgba(16,185,129,0.05)",line_width=0)
    fig_ipa.add_shape(type="rect",x0=0,x1=avg_p,y0=0,y1=avg_i,fillcolor="rgba(107,114,128,0.05)",line_width=0)
    fig_ipa.add_shape(type="rect",x0=avg_p,x1=110,y0=0,y1=avg_i,fillcolor="rgba(245,158,11,0.05)",line_width=0)

    for _, row in ipa_df.iterrows():
        fig_ipa.add_trace(go.Scatter(
            x=[row["Performance"]], y=[row["Importance"]],
            mode="markers+text",
            marker=dict(size=16,color=qcolor[row["Quadrant"]],line=dict(color="#0f172a",width=1)),
            text=[row["Dimensi"]], textposition="top center",
            textfont=dict(color="#e2e8f0",size=10),
            name=row["Quadrant"], showlegend=False,
        ))

    fig_ipa.add_vline(x=avg_p, line_dash="dash", line_color="#334155")
    fig_ipa.add_hline(y=avg_i, line_dash="dash", line_color="#334155")

    for label, xf, yf, color in [
        ("Priority\nImprovement", 0.25, 0.92, "#ef4444"),
        ("Maintain\nPerformance", 0.75, 0.92, "#10b981"),
        ("Low Priority",          0.25, 0.08, "#6b7280"),
        ("Possible\nOverkill",    0.75, 0.08, "#f59e0b"),
    ]:
        fig_ipa.add_annotation(
            xref="paper", yref="paper", x=xf, y=yf,
            text=label.replace("\n","<br>"), showarrow=False,
            font=dict(color=color,size=9), opacity=0.7)

    fig_ipa.update_layout(**PLOT,
        xaxis=dict(title="Performance (%)",range=[50,110],color="#94a3b8",gridcolor="#1e293b"),
        yaxis=dict(title="Importance (%)",range=[50,100],color="#94a3b8",gridcolor="#1e293b"),
        margin=dict(t=10,b=10,l=10,r=10), height=380)
    st.plotly_chart(fig_ipa, use_container_width=True)

with col_corr:
    st.markdown("<div class='section-title'>Korelasi Touchpoint vs CSI</div>", unsafe_allow_html=True)

    corr_cols = {
        "Teller":"overall_teller_xyz_pct", "CS":"overall_cs_xyz_pct",
        "ATM":"overall_atm_xyz_pct",       "Banking Hall":"overall_banking_hall_xyz_pct",
        "Sekuriti":"overall_sekuriti_xyz_pct", "Operasional":"overall_operasional_xyz_pct",
        "Parkir":"overall_parkir_xyz_pct", "Toilet":"overall_toilet_xyz_pct",
    }
    corr_vals = []
    for label, col in corr_cols.items():
        if col in df.columns and "csi_xyz_pct" in df.columns:
            c = df[["csi_xyz_pct",col]].dropna().corr().iloc[0,1]
            corr_vals.append({"Touchpoint":label,"Korelasi":round(c,3)})

    if corr_vals:
        corr_df = pd.DataFrame(corr_vals).sort_values("Korelasi",ascending=True)
        fig_corr = go.Figure(go.Bar(
            x=corr_df["Korelasi"], y=corr_df["Touchpoint"], orientation="h",
            marker_color=["#10b981" if v>=0.3 else "#f59e0b" if v>=0.1 else "#ef4444"
                          for v in corr_df["Korelasi"]],
            text=[f"{v:.3f}" for v in corr_df["Korelasi"]],
            textposition="outside", textfont=dict(color="#94a3b8",size=10),
        ))
        fig_corr.update_layout(**PLOT,
            xaxis=dict(range=[-0.1,0.8],color="#94a3b8",gridcolor="#1e293b",title="Korelasi Pearson"),
            yaxis=dict(color="#94a3b8"),
            margin=dict(t=10,b=10,l=10,r=60), height=380)
        st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CRISIS TABLE ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Branch x Touchpoint — Crisis Table</div>", unsafe_allow_html=True)

crisis_cols = {
    "CSI":"csi_xyz_pct", "Teller":"overall_teller_xyz_pct",
    "CS":"overall_cs_xyz_pct", "ATM":"overall_atm_xyz_pct",
    "Banking Hall":"overall_banking_hall_xyz_pct", "Sekuriti":"overall_sekuriti_xyz_pct",
}
avail_cols = {k:v for k,v in crisis_cols.items() if v in df.columns}
if avail_cols:
    crisis_df = df.groupby("nama_cabang")[list(avail_cols.values())].mean().round(1)
    crisis_df.columns = list(avail_cols.keys())
    crisis_df = crisis_df.reset_index().sort_values("CSI" if "CSI" in crisis_df.columns else crisis_df.columns[1])

    def color_cell(val):
        if isinstance(val, float):
            if val < 65:   return "background-color: rgba(239,68,68,0.2); color: #fca5a5"
            elif val < 80: return "background-color: rgba(245,158,11,0.2); color: #fde68a"
            else:          return "background-color: rgba(16,185,129,0.1); color: #6ee7b7"
        return ""

    num_cols_crisis = [c for c in crisis_df.columns if c != "nama_cabang"]
    styled = crisis_df.style.map(color_cell, subset=num_cols_crisis)
    st.dataframe(styled, use_container_width=True, height=300)

st.markdown("<br>", unsafe_allow_html=True)

# ── WAITING TIME ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Waktu Tunggu vs Toleransi</div>", unsafe_allow_html=True)
col_wt, col_wcs = st.columns(2)

with col_wt:
    wt = df[["nama_cabang","waktu_tunggu_teller_aktual","waktu_tunggu_teller_toleransi"]].dropna()
    if len(wt) > 0:
        wt_grp = wt.groupby("nama_cabang").mean().reset_index()
        wt_grp = wt_grp.sort_values("waktu_tunggu_teller_aktual", ascending=False).head(15)
        fig_wt = go.Figure()
        fig_wt.add_trace(go.Bar(
            name="Aktual", x=wt_grp["nama_cabang"], y=wt_grp["waktu_tunggu_teller_aktual"],
            marker_color=["#ef4444" if a>t else "#3b82f6"
                          for a,t in zip(wt_grp["waktu_tunggu_teller_aktual"],
                                         wt_grp["waktu_tunggu_teller_toleransi"])],
        ))
        fig_wt.add_trace(go.Scatter(
            name="Toleransi", x=wt_grp["nama_cabang"], y=wt_grp["waktu_tunggu_teller_toleransi"],
            mode="lines+markers", line=dict(color="#10b981",dash="dash",width=2), marker=dict(size=6),
        ))
        fig_wt.update_layout(**PLOT,
            title=dict(text="Teller: Waktu Tunggu vs Toleransi",font=dict(color="#e2e8f0",size=13),x=0),
            xaxis=dict(color="#94a3b8",tickangle=-30,tickfont=dict(size=9)),
            yaxis=dict(color="#94a3b8",gridcolor="#1e293b",title="Menit"),
            legend=dict(font=dict(color="#94a3b8",size=10)),
            margin=dict(t=40,b=80,l=10,r=10), height=320)
        st.plotly_chart(fig_wt, use_container_width=True)

with col_wcs:
    wcs = df[["nama_cabang","waktu_tunggu_cs_aktual","waktu_tunggu_cs_toleransi"]].dropna()
    if len(wcs) > 0:
        wcs_grp = wcs.groupby("nama_cabang").mean().reset_index()
        wcs_grp = wcs_grp.sort_values("waktu_tunggu_cs_aktual", ascending=False).head(15)
        fig_wcs = go.Figure()
        fig_wcs.add_trace(go.Bar(
            name="Aktual", x=wcs_grp["nama_cabang"], y=wcs_grp["waktu_tunggu_cs_aktual"],
            marker_color=["#ef4444" if a>t else "#f59e0b"
                          for a,t in zip(wcs_grp["waktu_tunggu_cs_aktual"],
                                         wcs_grp["waktu_tunggu_cs_toleransi"])],
        ))
        fig_wcs.add_trace(go.Scatter(
            name="Toleransi", x=wcs_grp["nama_cabang"], y=wcs_grp["waktu_tunggu_cs_toleransi"],
            mode="lines+markers", line=dict(color="#10b981",dash="dash",width=2), marker=dict(size=6),
        ))
        fig_wcs.update_layout(**PLOT,
            title=dict(text="CS: Waktu Tunggu vs Toleransi",font=dict(color="#e2e8f0",size=13),x=0),
            xaxis=dict(color="#94a3b8",tickangle=-30,tickfont=dict(size=9)),
            yaxis=dict(color="#94a3b8",gridcolor="#1e293b",title="Menit"),
            legend=dict(font=dict(color="#94a3b8",size=10)),
            margin=dict(t=40,b=80,l=10,r=10), height=320)
        st.plotly_chart(fig_wcs, use_container_width=True)