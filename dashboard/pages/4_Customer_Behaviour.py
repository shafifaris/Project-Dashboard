import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v>=9 else ('Passive' if v>=7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    for c in ['csi_xyz','cli_xyz']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
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

    pages = {"Overview":"/Overview","Branch Intelligence":"/Branch_Intelligence",
             "Touchpoint":"/Touchpoint","Customer Behaviour":"/Customer_Behaviour","Competitor":"/Competitor"}
    icons = {"Overview":"▣","Branch Intelligence":"◈","Touchpoint":"◎",
             "Customer Behaviour":"◉","Competitor":"◆"}
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Menu</div>", unsafe_allow_html=True)
    for name, path in pages.items():
        active = "active" if name=="Customer Behaviour" else ""
        st.markdown(f"<a href='{path}' target='_self' class='nav-pill {active}'>{icons[name]}&nbsp;&nbsp;{name}</a>",
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Filter Data</div>", unsafe_allow_html=True)

    gender_opts = ["Semua"] + sorted(df_raw["jenis_kelamin"].dropna().unique().tolist())
    sel_gender = st.selectbox("Gender", gender_opts)

    usia_opts = ["Semua"] + sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.selectbox("Usia", usia_opts)

    job_opts = ["Semua"] + sorted(df_raw["pekerjaan"].dropna().unique().tolist())
    sel_job = st.selectbox("Pekerjaan", job_opts)

    seg_opts = ["Semua"] + sorted(df_raw["kategori_nasabah"].dropna().unique().tolist())
    sel_seg = st.selectbox("Kategori Nasabah", seg_opts)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#475569;padding:0 4px;'>v2.0 · Bank XYZ Analytics</div>",
                unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_gender != "Semua": df = df[df["jenis_kelamin"]==sel_gender]
if sel_usia   != "Semua": df = df[df["range_usia"]==sel_usia]
if sel_job    != "Semua": df = df[df["pekerjaan"]==sel_job]
if sel_seg    != "Semua": df = df[df["kategori_nasabah"]==sel_seg]

n = len(df)
PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11))
def safe_mean(s): return s.dropna().mean() if s.dropna().shape[0]>0 else 0

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-bottom:20px;'>
    <div style='font-size:26px;font-weight:700;color:#f1f5f9;letter-spacing:-0.3px;'>Customer Behaviour</div>
    <div style='font-size:13px;color:#64748b;margin-top:4px;'>{n:,} responden terfilter</div>
</div>
""", unsafe_allow_html=True)

# ── ROW 1 — DEMOGRAFI ─────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Profil Demografi</div>", unsafe_allow_html=True)
d1,d2,d3,d4 = st.columns(4)

def donut_chart(df, col, title, colors):
    counts = df[col].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index.tolist(), values=counts.values.tolist(),
        hole=0.55, marker_colors=colors,
        textfont=dict(size=10,color="white"), textinfo="percent",
    ))
    fig.update_layout(**PLOT, height=200, margin=dict(t=30,b=10,l=0,r=0),
        title=dict(text=title,font=dict(color="#e2e8f0",size=12),x=0.5),
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8",size=9),orientation="h",x=0,y=-0.2))
    return fig

with d1:
    st.plotly_chart(donut_chart(df,"jenis_kelamin","Gender",["#3b82f6","#f472b6"]),
                    use_container_width=True)
with d2:
    age_cols = px.colors.sequential.Blues_r[:8]
    st.plotly_chart(donut_chart(df,"range_usia","Kelompok Usia",age_cols),
                    use_container_width=True)
with d3:
    freq_counts = df["frekuensi_transaksi_xyz"].value_counts()
    fig_freq = go.Figure(go.Pie(
        labels=freq_counts.index.tolist(), values=freq_counts.values.tolist(),
        hole=0.55, marker_colors=["#10b981","#3b82f6","#f59e0b","#a855f7"],
        textfont=dict(size=10,color="white"), textinfo="percent",
    ))
    fig_freq.update_layout(**PLOT, height=200, margin=dict(t=30,b=10,l=0,r=0),
        title=dict(text="Frekuensi Transaksi",font=dict(color="#e2e8f0",size=12),x=0.5),
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8",size=9),orientation="h",x=0,y=-0.2))
    st.plotly_chart(fig_freq, use_container_width=True)
with d4:
    lama_counts = df["lama_menjadi_nasabah"].value_counts()
    fig_lama = go.Figure(go.Pie(
        labels=lama_counts.index.tolist(), values=lama_counts.values.tolist(),
        hole=0.55, marker_colors=["#06b6d4","#3b82f6","#6366f1","#a855f7","#ec4899"],
        textfont=dict(size=10,color="white"), textinfo="percent",
    ))
    fig_lama.update_layout(**PLOT, height=200, margin=dict(t=30,b=10,l=0,r=0),
        title=dict(text="Lama Menjadi Nasabah",font=dict(color="#e2e8f0",size=12),x=0.5),
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8",size=9),orientation="h",x=0,y=-0.2))
    st.plotly_chart(fig_lama, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 2 — LOYALITAS + FREKUENSI ────────────────────────────────────────────
col_loy, col_freq = st.columns(2)

with col_loy:
    st.markdown("<div class='section-title'>Loyalitas berdasarkan Pekerjaan</div>", unsafe_allow_html=True)
    loy_job = df.groupby("pekerjaan")["cli_xyz_pct"].mean().dropna().sort_values(ascending=True)
    fig_loy = go.Figure(go.Bar(
        x=loy_job.values, y=loy_job.index, orientation="h",
        marker_color=["#10b981" if v>=80 else "#f59e0b" if v>=65 else "#ef4444" for v in loy_job.values],
        text=[f"{v:.1f}%" for v in loy_job.values],
        textposition="outside", textfont=dict(color="#94a3b8",size=10),
    ))
    fig_loy.update_layout(**PLOT,
        xaxis=dict(range=[0,115],color="#94a3b8",gridcolor="#1e293b"),
        yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
        margin=dict(t=10,b=10,l=10,r=60), height=320)
    st.plotly_chart(fig_loy, use_container_width=True)

with col_freq:
    st.markdown("<div class='section-title'>Frekuensi Transaksi vs Kepuasan (CSI)</div>", unsafe_allow_html=True)
    freq_csi = df.groupby("frekuensi_transaksi_xyz").agg(
        csi=("csi_xyz_pct","mean"),
        count=("serial_id","count"),
        cli=("cli_xyz_pct","mean"),
    ).reset_index().dropna()

    fig_fc = go.Figure()
    fig_fc.add_trace(go.Bar(name="CSI (%)", x=freq_csi["frekuensi_transaksi_xyz"],
        y=freq_csi["csi"], marker_color="#3b82f6",
        text=[f"{v:.1f}%" for v in freq_csi["csi"]],
        textposition="outside", textfont=dict(color="#94a3b8",size=10)))
    fig_fc.add_trace(go.Scatter(name="CLI (%)", x=freq_csi["frekuensi_transaksi_xyz"],
        y=freq_csi["cli"], mode="lines+markers",
        line=dict(color="#10b981",width=2), marker=dict(size=8)))
    fig_fc.update_layout(**PLOT,
        xaxis=dict(color="#94a3b8",tickangle=-15,tickfont=dict(size=10)),
        yaxis=dict(color="#94a3b8",gridcolor="#1e293b",range=[0,115],title="Score (%)"),
        legend=dict(font=dict(color="#94a3b8",size=10)),
        margin=dict(t=10,b=60,l=10,r=10), height=320)
    st.plotly_chart(fig_fc, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 3 — SWITCHING RISK ────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Switching Risk Matrix</div>", unsafe_allow_html=True)

def switching_risk(row):
    csi = row["csi_xyz_pct"] if not pd.isna(row["csi_xyz_pct"]) else 0
    cli = row["cli_xyz_pct"] if not pd.isna(row["cli_xyz_pct"]) else 0
    nps = row["nps_num"]     if not pd.isna(row["nps_num"])     else 5
    if csi>=80 and cli>=80 and nps>=9:  return "Loyal"
    elif csi>=75 and nps<7:             return "Vulnerable"
    elif csi<70 and cli<70 and nps<7:   return "At Risk"
    else:                               return "Neutral"

df["switching_risk"] = df.apply(switching_risk, axis=1)
risk_colors = {"Loyal":"#10b981","Neutral":"#3b82f6","Vulnerable":"#f59e0b","At Risk":"#ef4444"}

col_sw1, col_sw2 = st.columns([2,1])

with col_sw1:
    sample = df[["csi_xyz_pct","cli_xyz_pct","nps_num","switching_risk","pekerjaan"]].dropna()
    sample = sample.sample(min(500,len(sample)), random_state=42)
    fig_sw = px.scatter(sample, x="csi_xyz_pct", y="cli_xyz_pct",
        color="switching_risk", color_discrete_map=risk_colors,
        size="nps_num", size_max=15,
        hover_data=["pekerjaan","nps_num"],
        labels={"csi_xyz_pct":"CSI (%)","cli_xyz_pct":"CLI (%)","switching_risk":"Risk Segment"})
    fig_sw.add_vline(x=75, line_dash="dash", line_color="#334155")
    fig_sw.add_hline(y=75, line_dash="dash", line_color="#334155")
    fig_sw.update_layout(**PLOT,
        xaxis=dict(color="#94a3b8",gridcolor="#1e293b",range=[40,115]),
        yaxis=dict(color="#94a3b8",gridcolor="#1e293b",range=[40,115]),
        legend=dict(font=dict(color="#94a3b8",size=10)),
        margin=dict(t=10,b=10,l=10,r=10), height=320)
    st.plotly_chart(fig_sw, use_container_width=True)

with col_sw2:
    risk_counts = df["switching_risk"].value_counts()
    fig_risk_bar = go.Figure(go.Bar(
        x=risk_counts.values, y=risk_counts.index, orientation="h",
        marker_color=[risk_colors.get(r,"#6b7280") for r in risk_counts.index],
        text=risk_counts.values,
        textposition="outside", textfont=dict(color="#94a3b8",size=11),
    ))
    fig_risk_bar.update_layout(**PLOT,
        xaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
        yaxis=dict(color="#94a3b8"),
        margin=dict(t=10,b=10,l=10,r=50), height=320)
    st.plotly_chart(fig_risk_bar, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 4 — XYZ ONLY VS MULTI BANK + ATM ─────────────────────────────────────
col_bank, col_atm = st.columns(2)

with col_bank:
    st.markdown("<div class='section-title'>XYZ Only vs Multi Bank</div>", unsafe_allow_html=True)
    def is_xyz_only(val):
        if pd.isna(val): return "Tidak Diketahui"
        banks = [b.strip() for b in str(val).split(";") if b.strip()]
        xyz_banks = [b for b in banks if "XYZ" in b]
        return "XYZ Only" if len(banks)==1 and len(xyz_banks)==1 else "Multi Bank"

    df["bank_usage_type"] = df["bank_aktif_digunakan"].apply(is_xyz_only)
    bank_usage = df["bank_usage_type"].value_counts()
    fig_bu = go.Figure(go.Pie(
        labels=bank_usage.index.tolist(), values=bank_usage.values.tolist(),
        hole=0.55, marker_colors=["#3b82f6","#f59e0b","#6b7280"],
        textfont=dict(size=11,color="white"), textinfo="label+percent",
    ))
    fig_bu.update_layout(**PLOT, height=300, margin=dict(t=10,b=10,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_bu, use_container_width=True)

with col_atm:
    st.markdown("<div class='section-title'>Penggunaan ATM</div>", unsafe_allow_html=True)
    atm_usage = df["penggunaan_atm"].value_counts()
    fig_atm = go.Figure(go.Bar(
        x=atm_usage.index, y=atm_usage.values,
        marker_color=["#10b981" if v=="Ya" else "#ef4444" for v in atm_usage.index],
        text=atm_usage.values,
        textposition="outside", textfont=dict(color="#94a3b8",size=12),
    ))
    fig_atm.update_layout(**PLOT,
        xaxis=dict(color="#94a3b8"),
        yaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
        margin=dict(t=10,b=10,l=10,r=10), height=300)
    st.plotly_chart(fig_atm, use_container_width=True)