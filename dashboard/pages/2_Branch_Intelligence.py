import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #0f172a; }
.block-container { padding: 1.5rem 2rem; }
[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e293b; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.nav-label { color:#64748b; font-size:10px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em; padding:0 0 6px 0; margin-top:8px; }
.nav-pill { display:block; padding:9px 14px; border-radius:8px; color:#94a3b8;
    font-size:13px; font-weight:500; text-decoration:none; margin-bottom:3px; }
.nav-pill:hover { background:#1e293b; color:#f1f5f9; }
.nav-pill.active { background:linear-gradient(90deg,#3b82f6,#06b6d4); color:#fff; font-weight:600; }
.kpi-card { background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);
    border:1px solid #334155; border-radius:12px; padding:18px 16px;
    text-align:center; position:relative; overflow:hidden; }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0;
    height:3px; background:linear-gradient(90deg,#3b82f6,#06b6d4); }
.kpi-label { color:#94a3b8; font-size:11px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px; }
.kpi-value { color:#f1f5f9; font-size:26px; font-weight:700; }
.kpi-delta { font-size:11px; margin-top:5px; }
.kpi-green { color:#10b981; } .kpi-yellow { color:#f59e0b; } .kpi-red { color:#ef4444; }
.section-title { color:#e2e8f0; font-size:15px; font-weight:600;
    margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    def parse_nps(val):
        if pd.isna(val) or str(val).strip()=='': return np.nan
        try: return int(str(val).strip().split()[0])
        except: return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v>=9 else ('Passive' if v>=7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    num_cols = ['overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
                'overall_banking_hall_xyz','overall_sekuriti_xyz',
                'overall_operasional_xyz','csi_xyz','cli_xyz',
                'waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi',
                'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi']
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    for c in ['overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
              'overall_banking_hall_xyz','overall_sekuriti_xyz',
              'overall_operasional_xyz','csi_xyz','cli_xyz']:
        df[c+'_pct'] = (df[c]/6*100).round(1)
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

    pages = {
        "Overview":            "/Overview",
        "Branch Intelligence": "/Branch_Intelligence",
        "Touchpoint":          "/Touchpoint",
        "Customer Behaviour":  "/Customer_Behaviour",
        "Competitor":          "/Competitor",
    }
    icons = {"Overview":"▣","Branch Intelligence":"◈","Touchpoint":"◎",
             "Customer Behaviour":"◉","Competitor":"◆"}

    st.markdown("<div class='nav-label' style='padding:0 8px;'>Menu</div>", unsafe_allow_html=True)
    for name, path in pages.items():
        active = "active" if name=="Branch Intelligence" else ""
        st.markdown(
            f"<a href='{path}' target='_self' class='nav-pill {active}'>"
            f"{icons[name]}&nbsp;&nbsp;{name}</a>",
            unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = ["Semua"] + sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.selectbox("Provinsi", prov_opts)

    pool = df_raw if sel_prov=="Semua" else df_raw[df_raw["provinsi"]==sel_prov]
    kota_opts = ["Semua"] + sorted(pool["kab_kota"].dropna().unique().tolist())
    sel_kota = st.selectbox("Kota/Kabupaten", kota_opts)

    pool2 = pool if sel_kota=="Semua" else pool[pool["kab_kota"]==sel_kota]
    branch_opts = sorted(pool2["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect("Cabang", branch_opts, placeholder="Semua Cabang")

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#475569;padding:0 4px;'>v2.0 · Bank XYZ Analytics</div>",
                unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov   != "Semua": df = df[df["provinsi"]==sel_prov]
if sel_kota   != "Semua": df = df[df["kab_kota"]==sel_kota]
if sel_branch:             df = df[df["nama_cabang"].isin(sel_branch)]

n = len(df)
PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11))
def safe_mean(s): return s.dropna().mean() if s.dropna().shape[0]>0 else 0

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-bottom:20px;'>
    <div style='font-size:26px;font-weight:700;color:#f1f5f9;letter-spacing:-0.3px;'>Branch Intelligence</div>
    <div style='font-size:13px;color:#64748b;margin-top:4px;'>
        {n:,} responden &nbsp;·&nbsp; {df['nama_cabang'].nunique()} cabang aktif
    </div>
</div>
""", unsafe_allow_html=True)

# ── BRANCH HEALTH SCORE ───────────────────────────────────────────────────────
branch_stats = df.groupby(["nama_cabang","provinsi"]).agg(
    responden=("serial_id","count"),
    csi=("csi_xyz_pct","mean"),
    nps_avg=("nps_num","mean"),
    promoter_pct=("nps_category", lambda x: (x=="Promoter").mean()*100),
    wait_teller=("waktu_tunggu_teller_aktual","mean"),
    wait_cs=("waktu_tunggu_cs_aktual","mean"),
    tol_teller=("waktu_tunggu_teller_toleransi","mean"),
    tol_cs=("waktu_tunggu_cs_toleransi","mean"),
).reset_index()

branch_stats["sla_teller_ok"] = (branch_stats["wait_teller"] <= branch_stats["tol_teller"]).astype(float) * 100
branch_stats["health_score"] = (
    branch_stats["csi"].fillna(0) * 0.40 +
    branch_stats["promoter_pct"].fillna(0) * 0.30 +
    branch_stats["sla_teller_ok"].fillna(50) * 0.20 +
    (branch_stats["responden"].clip(0,30)/30*100) * 0.10
).clip(0,100).round(1)

# ── KPI ───────────────────────────────────────────────────────────────────────
def kpi(label, val, suffix="", cls="kpi-green", delta=""):
    return f"""<div class="kpi-card"><div class="kpi-label">{label}</div>
    <div class="kpi-value">{val}{suffix}</div>
    <div class="kpi-delta {cls}">{delta}</div></div>"""

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(kpi("Total Cabang", df['nama_cabang'].nunique(),"","kpi-green","Cabang aktif"), unsafe_allow_html=True)
with c2:
    if len(branch_stats) > 0:
        best = branch_stats.nlargest(1,"health_score").iloc[0]
        st.markdown(kpi("Best Branch", best["nama_cabang"][:20],"","kpi-green",f"Score: {best['health_score']:.1f}"), unsafe_allow_html=True)
with c3:
    if len(branch_stats) > 0:
        worst = branch_stats.nsmallest(1,"health_score").iloc[0]
        st.markdown(kpi("Needs Action", worst["nama_cabang"][:20],"","kpi-red",f"Score: {worst['health_score']:.1f}"), unsafe_allow_html=True)
with c4:
    if len(branch_stats) > 0:
        avg_h = branch_stats["health_score"].mean()
        cc = "kpi-green" if avg_h>=75 else "kpi-yellow" if avg_h>=60 else "kpi-red"
        st.markdown(kpi("Avg Health Score", f"{avg_h:.1f}","",cc,"Semua Cabang"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TOP & BOTTOM ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Top & Bottom Branch — Health Score</div>", unsafe_allow_html=True)
col_top, col_bot = st.columns(2)

top10 = branch_stats.nlargest(10,"health_score").sort_values("health_score")
bot10 = branch_stats.nsmallest(10,"health_score").sort_values("health_score", ascending=False)

with col_top:
    fig_top = go.Figure(go.Bar(
        x=top10["health_score"], y=top10["nama_cabang"],
        orientation="h", marker_color="#10b981",
        text=[f"{v:.1f}" for v in top10["health_score"]],
        textposition="outside", textfont=dict(color="#94a3b8",size=10),
    ))
    fig_top.update_layout(**PLOT,
        title=dict(text="Top 10 Cabang", font=dict(color="#e2e8f0",size=13), x=0),
        xaxis=dict(range=[0,115],color="#94a3b8",gridcolor="#1e293b"),
        yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
        margin=dict(t=30,b=10,l=10,r=50), height=320)
    st.plotly_chart(fig_top, use_container_width=True)

with col_bot:
    fig_bot = go.Figure(go.Bar(
        x=bot10["health_score"], y=bot10["nama_cabang"],
        orientation="h", marker_color="#ef4444",
        text=[f"{v:.1f}" for v in bot10["health_score"]],
        textposition="outside", textfont=dict(color="#94a3b8",size=10),
    ))
    fig_bot.update_layout(**PLOT,
        title=dict(text="Bottom 10 Cabang", font=dict(color="#e2e8f0",size=13), x=0),
        xaxis=dict(range=[0,115],color="#94a3b8",gridcolor="#1e293b"),
        yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
        margin=dict(t=30,b=10,l=10,r=50), height=320)
    st.plotly_chart(fig_bot, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── WAITING TIME ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Waktu Tunggu per Cabang — Teller vs CS</div>", unsafe_allow_html=True)

wait_data = df.groupby("nama_cabang").agg(
    wait_teller=("waktu_tunggu_teller_aktual","mean"),
    tol_teller=("waktu_tunggu_teller_toleransi","mean"),
    wait_cs=("waktu_tunggu_cs_aktual","mean"),
    tol_cs=("waktu_tunggu_cs_toleransi","mean"),
).reset_index().dropna(subset=["wait_teller","wait_cs"], how="all")
wait_data = wait_data.sort_values("wait_teller", ascending=False).head(20)

fig_wait = go.Figure()
fig_wait.add_trace(go.Bar(name="Teller (Aktual)", x=wait_data["nama_cabang"],
    y=wait_data["wait_teller"], marker_color="#3b82f6"))
fig_wait.add_trace(go.Bar(name="CS (Aktual)", x=wait_data["nama_cabang"],
    y=wait_data["wait_cs"], marker_color="#f59e0b"))
fig_wait.add_trace(go.Scatter(name="Toleransi Teller", x=wait_data["nama_cabang"],
    y=wait_data["tol_teller"], mode="lines",
    line=dict(color="#10b981", dash="dash", width=1.5)))
fig_wait.add_trace(go.Scatter(name="Toleransi CS", x=wait_data["nama_cabang"],
    y=wait_data["tol_cs"], mode="lines",
    line=dict(color="#a855f7", dash="dash", width=1.5)))
fig_wait.update_layout(**PLOT, barmode="group",
    xaxis=dict(color="#94a3b8",gridcolor="#1e293b",tickangle=-30,tickfont=dict(size=9)),
    yaxis=dict(color="#94a3b8",gridcolor="#1e293b",title="Menit"),
    legend=dict(font=dict(color="#94a3b8",size=10),orientation="h",x=0,y=1.08),
    margin=dict(t=40,b=80,l=10,r=10), height=380)
st.plotly_chart(fig_wait, use_container_width=True)

# ── KETERSEDIAAN SMARTAB ──────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Ketersediaan Smart Table per Cabang</div>", unsafe_allow_html=True)

if "smart_table_xyz" in df.columns:
    df["smart_table_xyz"] = pd.to_numeric(df["smart_table_xyz"], errors="coerce")
    smart = df.groupby("nama_cabang")["smart_table_xyz"].mean().reset_index()
    smart["smart_table_xyz"] = (smart["smart_table_xyz"]/6*100).round(1)
    smart = smart.sort_values("smart_table_xyz", ascending=False).head(20)

    fig_smart = go.Figure(go.Bar(
        x=smart["nama_cabang"], y=smart["smart_table_xyz"],
        marker_color=["#10b981" if v>=80 else "#f59e0b" if v>=65 else "#ef4444"
                      for v in smart["smart_table_xyz"]],
        text=[f"{v:.1f}%" for v in smart["smart_table_xyz"]],
        textposition="outside", textfont=dict(color="#94a3b8",size=9),
    ))
    fig_smart.update_layout(**PLOT,
        xaxis=dict(color="#94a3b8",tickangle=-30,tickfont=dict(size=9)),
        yaxis=dict(color="#94a3b8",gridcolor="#1e293b",range=[0,115],title="%"),
        margin=dict(t=10,b=80,l=10,r=10), height=320)
    st.plotly_chart(fig_smart, use_container_width=True)

# ── BRANCH TABLE ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Branch Benchmark Table</div>", unsafe_allow_html=True)
tbl = branch_stats[["nama_cabang","provinsi","responden","csi","promoter_pct",
                     "health_score","wait_teller","wait_cs"]].copy()
tbl.columns = ["Cabang","Provinsi","Responden","CSI (%)","Promoter (%)","Health Score",
               "Wait Teller (mnt)","Wait CS (mnt)"]
for c in ["CSI (%)","Promoter (%)","Health Score","Wait Teller (mnt)","Wait CS (mnt)"]:
    tbl[c] = tbl[c].round(1)
tbl = tbl.sort_values("Health Score", ascending=False).reset_index(drop=True)
tbl.index += 1
st.dataframe(tbl, use_container_width=True, height=350)