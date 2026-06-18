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

    df['nps_num']      = df['nps_xyz'].apply(parse_nps)
    df['nps_komp_num'] = df['nps_kompetitor'].apply(parse_nps)

    for c in ['csi_xyz','cli_xyz','csi_kompetitor','cli_kompetitor']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        df[c+'_pct'] = (df[c]/6*100).round(1)

    # Kompetitor touchpoint — banyak blank, replace dulu
    komp_tp = ['overall_teller_komp','overall_cs_komp',
               'overall_atm_komp','overall_banking_hall_komp']
    for c in komp_tp:
        df[c] = df[c].replace(' ', np.nan)
        df[c] = pd.to_numeric(df[c], errors='coerce')
        df[c+'_pct'] = (df[c]/6*100).round(1)

    xyz_tp = ['overall_teller_xyz','overall_cs_xyz',
              'overall_atm_xyz','overall_banking_hall_xyz']
    for c in xyz_tp:
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
        active = "active" if name=="Competitor" else ""
        st.markdown(f"<a href='{path}' target='_self' class='nav-pill {active}'>{icons[name]}&nbsp;&nbsp;{name}</a>",
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label' style='padding:0 8px;'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = ["Semua"] + sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.selectbox("Provinsi", prov_opts)

    seg_opts = ["Semua"] + sorted(df_raw["kategori_nasabah"].dropna().unique().tolist())
    sel_seg = st.selectbox("Segmen Nasabah", seg_opts)

    st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#475569;padding:0 4px;'>v2.0 · Bank XYZ Analytics</div>",
                unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov != "Semua": df = df[df["provinsi"]==sel_prov]
if sel_seg  != "Semua": df = df[df["kategori_nasabah"]==sel_seg]

n = len(df)
PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11))
def safe_mean(s): return s.dropna().mean() if s.dropna().shape[0]>0 else 0

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-bottom:20px;'>
    <div style='font-size:26px;font-weight:700;color:#f1f5f9;letter-spacing:-0.3px;'>Competitor Benchmark</div>
    <div style='font-size:13px;color:#64748b;margin-top:4px;'>{n:,} responden terfilter</div>
</div>
""", unsafe_allow_html=True)

# ── ROW 1 — BANK LAIN ─────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Bank Lain yang Digunakan Nasabah</div>", unsafe_allow_html=True)

bank_selain = df["bank_aktif_selain_xyz"].dropna()
bank_selain = bank_selain[bank_selain.str.strip() != ""]
all_banks = []
for val in bank_selain:
    for b in str(val).split(";"):
        b = b.strip()
        if b: all_banks.append(b)

if all_banks:
    bank_counts = pd.Series(all_banks).value_counts().head(10).sort_values(ascending=True)
    fig_bank = go.Figure(go.Bar(
        x=bank_counts.values, y=bank_counts.index, orientation="h",
        marker_color=["#3b82f6" if i==len(bank_counts)-1 else "#334155"
                      for i in range(len(bank_counts))],
        text=bank_counts.values,
        textposition="outside", textfont=dict(color="#94a3b8",size=11),
    ))
    fig_bank.update_layout(**PLOT,
        xaxis=dict(color="#94a3b8",gridcolor="#1e293b",title="Jumlah Nasabah"),
        yaxis=dict(color="#94a3b8",tickfont=dict(size=10)),
        margin=dict(t=10,b=10,l=10,r=60), height=320)
    st.plotly_chart(fig_bank, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 2 — MARKET SHARE ──────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Market Share — Simpan Dana & Transaksi</div>", unsafe_allow_html=True)
col_ms1, col_ms2 = st.columns(2)

def market_share_chart(col, title):
    data = df[col].dropna()
    data = data[data.str.strip() != ""]
    counts = data.value_counts().head(6)
    colors = ["#3b82f6" if "XYZ" in str(i) else "#334155" for i in counts.index]
    fig = go.Figure(go.Pie(
        labels=counts.index.tolist(), values=counts.values.tolist(),
        hole=0.5, marker_colors=colors,
        textfont=dict(size=10,color="white"), textinfo="label+percent",
        pull=[0.05 if "XYZ" in str(i) else 0 for i in counts.index],
    ))
    fig.update_layout(**PLOT, height=300, margin=dict(t=30,b=10,l=0,r=0),
        title=dict(text=title,font=dict(color="#e2e8f0",size=13),x=0.5),
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8",size=9),orientation="v"))
    return fig

with col_ms1:
    st.plotly_chart(market_share_chart("bank_utama_simpan_dana","Market Share: Simpan Dana"),
                    use_container_width=True)
with col_ms2:
    st.plotly_chart(market_share_chart("bank_utama_transaksi","Market Share: Transaksi"),
                    use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 3 — RADAR XYZ VS KOMPETITOR ──────────────────────────────────────────
st.markdown("<div class='section-title'>XYZ vs Kompetitor — Radar Touchpoint</div>", unsafe_allow_html=True)

dims = ["Teller","CS","ATM","Banking Hall"]
xyz_vals  = [safe_mean(df["overall_teller_xyz_pct"]), safe_mean(df["overall_cs_xyz_pct"]),
             safe_mean(df["overall_atm_xyz_pct"]),    safe_mean(df["overall_banking_hall_xyz_pct"])]
komp_vals = [safe_mean(df["overall_teller_komp_pct"]), safe_mean(df["overall_cs_komp_pct"]),
             safe_mean(df["overall_atm_komp_pct"]),    safe_mean(df["overall_banking_hall_komp_pct"])]

dims_closed = dims + [dims[0]]
xyz_closed  = xyz_vals  + [xyz_vals[0]]
komp_closed = komp_vals + [komp_vals[0]]

fig_rad = go.Figure()
fig_rad.add_trace(go.Scatterpolar(
    r=xyz_closed, theta=dims_closed,
    fill="toself", fillcolor="rgba(59,130,246,0.2)",
    line=dict(color="#3b82f6",width=2), name="Bank XYZ"))
fig_rad.add_trace(go.Scatterpolar(
    r=komp_closed, theta=dims_closed,
    fill="toself", fillcolor="rgba(239,68,68,0.15)",
    line=dict(color="#ef4444",width=2), name="Kompetitor"))
fig_rad.update_layout(
    polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(range=[0,110],color="#94a3b8",gridcolor="#1e293b"),
        angularaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter",color="#94a3b8",size=11),
    legend=dict(font=dict(color="#94a3b8",size=11)),
    margin=dict(t=20,b=20,l=20,r=20), height=380)
st.plotly_chart(fig_rad, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 4 — CSI / NPS / CLI COMPARISON ───────────────────────────────────────
st.markdown("<div class='section-title'>XYZ vs Kompetitor — CSI, NPS, CLI</div>", unsafe_allow_html=True)

nps_n    = df["nps_num"].notna().sum()
nps_kn   = df["nps_komp_num"].notna().sum()
nps_xyz  = round(((df["nps_num"]>=9).sum()-(df["nps_num"]<=6).sum())/max(nps_n,1)*100,1)
nps_komp = round(((df["nps_komp_num"]>=9).sum()-(df["nps_komp_num"]<=6).sum())/max(nps_kn,1)*100,1)

metrics   = ["CSI (%)","CLI (%)","NPS Score"]
xyz_mets  = [safe_mean(df["csi_xyz_pct"]), safe_mean(df["cli_xyz_pct"]),  nps_xyz]
komp_mets = [safe_mean(df["csi_kompetitor_pct"]), safe_mean(df["cli_kompetitor_pct"]), nps_komp]

fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(name="Bank XYZ", x=metrics, y=xyz_mets,
    marker_color="#3b82f6",
    text=[f"{v:.1f}" for v in xyz_mets],
    textposition="outside", textfont=dict(color="#94a3b8",size=11)))
fig_comp.add_trace(go.Bar(name="Kompetitor", x=metrics, y=komp_mets,
    marker_color="#ef4444",
    text=[f"{v:.1f}" for v in komp_mets],
    textposition="outside", textfont=dict(color="#94a3b8",size=11)))
fig_comp.update_layout(**PLOT, barmode="group",
    xaxis=dict(color="#94a3b8"),
    yaxis=dict(color="#94a3b8",gridcolor="#1e293b",range=[0,115],title="Score"),
    legend=dict(font=dict(color="#94a3b8",size=11)),
    margin=dict(t=10,b=10,l=10,r=10), height=320)
st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 5 — ALASAN NPS ────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Alasan NPS — XYZ vs Kompetitor (per Kategori)</div>",
            unsafe_allow_html=True)
col_n1, col_n2 = st.columns(2)

with col_n1:
    nps_pos = df[df["nps_xyz_sentimen"]=="POSITIVE COMMENTS"]["nps_xyz_kategori"].dropna()
    nps_pos = nps_pos[nps_pos.str.strip()!=""].value_counts().head(8).sort_values(ascending=True)
    if len(nps_pos) > 0:
        fig_p = go.Figure(go.Bar(x=nps_pos.values, y=nps_pos.index, orientation="h",
            marker_color="#10b981", text=nps_pos.values, textposition="outside",
            textfont=dict(color="#94a3b8",size=10)))
        fig_p.update_layout(**PLOT,
            title=dict(text="Alasan Positif NPS — XYZ",font=dict(color="#e2e8f0",size=12),x=0),
            xaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
            yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
            margin=dict(t=30,b=10,l=10,r=50), height=300)
        st.plotly_chart(fig_p, use_container_width=True)

    nps_neg = df[df["nps_xyz_sentimen"]=="NEGATIVE COMMENTS"]["nps_xyz_kategori"].dropna()
    nps_neg = nps_neg[nps_neg.str.strip()!=""].value_counts().head(8).sort_values(ascending=True)
    if len(nps_neg) > 0:
        fig_n = go.Figure(go.Bar(x=nps_neg.values, y=nps_neg.index, orientation="h",
            marker_color="#ef4444", text=nps_neg.values, textposition="outside",
            textfont=dict(color="#94a3b8",size=10)))
        fig_n.update_layout(**PLOT,
            title=dict(text="Alasan Negatif NPS — XYZ",font=dict(color="#e2e8f0",size=12),x=0),
            xaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
            yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
            margin=dict(t=30,b=10,l=10,r=50), height=300)
        st.plotly_chart(fig_n, use_container_width=True)

with col_n2:
    komp_pos = df[df["nps_komp_sentimen"]=="POSITIVE COMMENTS"]["nps_komp_kategori"].dropna()
    komp_pos = komp_pos[komp_pos.str.strip()!=""].value_counts().head(8).sort_values(ascending=True)
    if len(komp_pos) > 0:
        fig_kp = go.Figure(go.Bar(x=komp_pos.values, y=komp_pos.index, orientation="h",
            marker_color="#06b6d4", text=komp_pos.values, textposition="outside",
            textfont=dict(color="#94a3b8",size=10)))
        fig_kp.update_layout(**PLOT,
            title=dict(text="Alasan Positif NPS — Kompetitor",font=dict(color="#e2e8f0",size=12),x=0),
            xaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
            yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
            margin=dict(t=30,b=10,l=10,r=50), height=300)
        st.plotly_chart(fig_kp, use_container_width=True)

    komp_neg = df[df["nps_komp_sentimen"]=="NEGATIVE COMMENTS"]["nps_komp_kategori"].dropna()
    komp_neg = komp_neg[komp_neg.str.strip()!=""].value_counts().head(8).sort_values(ascending=True)
    if len(komp_neg) > 0:
        fig_kn = go.Figure(go.Bar(x=komp_neg.values, y=komp_neg.index, orientation="h",
            marker_color="#a855f7", text=komp_neg.values, textposition="outside",
            textfont=dict(color="#94a3b8",size=10)))
        fig_kn.update_layout(**PLOT,
            title=dict(text="Alasan Negatif NPS — Kompetitor",font=dict(color="#e2e8f0",size=12),x=0),
            xaxis=dict(color="#94a3b8",gridcolor="#1e293b"),
            yaxis=dict(color="#94a3b8",tickfont=dict(size=9)),
            margin=dict(t=30,b=10,l=10,r=50), height=300)
        st.plotly_chart(fig_kn, use_container_width=True)