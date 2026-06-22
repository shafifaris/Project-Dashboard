import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loader import load_data
from style import SIDEBAR_CSS, PLOT

st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
df_raw = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 10px 14px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:14px;'>
        <div style='font-family:"DM Serif Display",serif;font-size:22px;color:#f1f5f9;'>Bank XYZ</div>
        <div style='font-size:9.5px;color:#475569;margin-top:3px;text-transform:uppercase;letter-spacing:0.1em;'>
            Customer Experience Intelligence
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='nav-label'>Menu</div>", unsafe_allow_html=True)
    pages = {"Overview":"/Overview","Branch Intelligence":"/Branch_Intelligence",
             "Touchpoint":"/Touchpoint","Customer Behaviour":"/Customer_Behaviour","Competitor":"/Competitor"}
    icons = {"Overview":"◈","Branch Intelligence":"▣","Touchpoint":"◎","Customer Behaviour":"◉","Competitor":"◆"}
    for name, path in pages.items():
        active = "active" if name == "Competitor" else ""
        st.markdown(f"<a href='{path}' target='_self' class='nav-pill {active}'><span>{icons[name]}</span><span>{name}</span></a>",
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov  = st.multiselect("Provinsi", prov_opts, placeholder="Semua Provinsi")

    seg_opts = ["Semua"] + sorted(df_raw["kategori_nasabah"].dropna().unique().tolist())
    sel_seg  = st.selectbox("Segmen Nasabah", seg_opts)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:#334155;padding:0 4px;'>v4.0 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov: df = df[df["provinsi"].isin(sel_prov)]
if sel_seg != "Semua": df = df[df["kategori_nasabah"] == sel_seg]
n = len(df)

def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def pct_color(v): return "#15803d" if v >= 80 else ("#b45309" if v >= 65 else "#b91c1c")
def pct_label(v): return "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")
def badge_cls(v, hi, mid): return "badge-green" if v >= hi else ("badge-yellow" if v >= mid else "badge-red")

# ── COMPUTED METRICS ──────────────────────────────────────────────────────────
nps_n      = int(df["nps_num"].notna().sum())
nps_komp_n = int(df["nps_komp_num"].notna().sum())
nps_xyz    = round(((df["nps_num"] >= 9).sum() - (df["nps_num"] <= 6).sum()) / max(nps_n,1) * 100, 1)
nps_komp   = round(((df["nps_komp_num"] >= 9).sum() - (df["nps_komp_num"] <= 6).sum()) / max(nps_komp_n,1) * 100, 1)
nps_gap    = round(nps_xyz - nps_komp, 1)

csi_xyz_val  = round(safe_mean(df["csi_xyz"])        / 6 * 100, 1) if "csi_xyz"        in df.columns else 0.0
csi_komp_val = round(safe_mean(df["csi_kompetitor"]) / 6 * 100, 1) if "csi_kompetitor" in df.columns else 0.0
cli_xyz_val  = round(safe_mean(df["cli_xyz"])        / 6 * 100, 1) if "cli_xyz"        in df.columns else 0.0
cli_komp_val = round(safe_mean(df["cli_kompetitor"]) / 6 * 100, 1) if "cli_kompetitor" in df.columns else 0.0

TOUCHPOINTS = [
    ("Teller","overall_teller_xyz","overall_teller_komp"),
    ("Customer Svc","overall_cs_xyz","overall_cs_komp"),
    ("ATM","overall_atm_xyz","overall_atm_komp"),
    ("Banking Hall","overall_banking_hall_xyz","overall_banking_hall_komp"),
    ("Sekuriti","overall_sekuriti_xyz","overall_sekuriti_komp"),
]
tp_data = []
for label, col_xyz, col_komp in TOUCHPOINTS:
    v_xyz  = round(safe_mean(df[col_xyz  + "_pct"]) if col_xyz  + "_pct" in df.columns else safe_mean(df[col_xyz])  / 6 * 100, 1) if col_xyz  in df.columns else 0.0
    v_komp = round(safe_mean(df[col_komp + "_pct"]) if col_komp + "_pct" in df.columns else safe_mean(df[col_komp]) / 6 * 100, 1) if col_komp in df.columns else 0.0
    tp_data.append({"label":label,"xyz":v_xyz,"komp":v_komp,"gap":round(v_xyz-v_komp,1)})

IMG_PAIRS = [
    ("Terkenal","img_terkenal_xyz","img_terkenal_komp"),
    ("Rasa Aman","img_rasa_aman_xyz","img_rasa_aman_komp"),
    ("Dihargai","img_dihargai_xyz","img_dihargai_komp"),
    ("Reputasi","img_reputasi_xyz","img_reputasi_komp"),
    ("Produk Lengkap","img_produk_lengkap_xyz","img_produk_lengkap_komp"),
    ("Investasi","img_investasi_xyz","img_investasi_komp"),
    ("Kemudahan Transaksi","img_kemudahan_transaksi_xyz","img_kemudahan_transaksi_komp"),
    ("Teknologi","img_teknologi_xyz","img_teknologi_komp"),
    ("Reward","img_reward_xyz","img_reward_komp"),
    ("E-Channel","img_echannel_xyz","img_echannel_komp"),
]
img_gap_data = []
for label, cxyz, ckomp in IMG_PAIRS:
    vx = safe_mean(df[cxyz])  if cxyz  in df.columns else 0.0
    vk = safe_mean(df[ckomp]) if ckomp in df.columns else 0.0
    img_gap_data.append({"label":label,"xyz":round(vx,2),"komp":round(vk,2),"gap":round(vx-vk,2)})
img_gap_data.sort(key=lambda x: x["gap"])

def get_bank_list(col):
    series = df[col].dropna() if col in df.columns else pd.Series([],dtype=str)
    series = series[series.astype(str).str.strip() != ""]
    banks  = []
    for val in series:
        for b in str(val).split(";"):
            b = b.strip()
            if b: banks.append(b)
    return pd.Series(banks).value_counts()

bank_aktif_counts = get_bank_list("bank_aktif_selain_xyz")
komp_dana_counts  = get_bank_list("kompetitor_simpan_dana")
komp_trx_counts   = get_bank_list("kompetitor_transaksi")

def xyz_pct(col):
    if col not in df.columns: return 0.0
    s = df[col].dropna().astype(str).str.strip()
    return round((s == "Bank XYZ").mean() * 100, 1) if len(s) > 0 else 0.0

pct_dana = xyz_pct("bank_utama_simpan_dana")
pct_trx  = xyz_pct("bank_utama_transaksi")

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">◆ Bank XYZ · Competitor Intelligence</div>
    <h2>Competitor Intelligence</h2>
    <p>{n:,} responden terfilter &nbsp;·&nbsp; Benchmarking vs kompetitor utama</p>
</div>""", unsafe_allow_html=True)

# ── KPI SUMMARY ───────────────────────────────────────────────────────────────
st.markdown("""<div class="section-label">
    <span class="section-label-text">KPI Summary — XYZ vs Kompetitor</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1:
    sign = "+" if nps_gap >= 0 else ""
    bc = "badge-green" if nps_gap >= 0 else "badge-red"
    lbl = "Unggul" if nps_gap >= 0 else "Tertinggal"
    st.markdown(f"""<div class="exec-card blue">
        <span class="exec-icon">📊</span>
        <div class="exec-label">NPS Gap</div>
        <div class="exec-value" style="color:#1e40af;">{sign}{nps_gap}</div>
        <div class="exec-sub">XYZ {nps_xyz} · Komp {nps_komp}</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)
with c2:
    csi_gap = round(csi_xyz_val - csi_komp_val, 1)
    sign = "+" if csi_gap >= 0 else ""
    bc = "badge-green" if csi_gap >= 0 else "badge-red"
    lbl = "Unggul" if csi_gap >= 0 else "Tertinggal"
    st.markdown(f"""<div class="exec-card cyan">
        <span class="exec-icon">⭐</span>
        <div class="exec-label">CSI Gap (%)</div>
        <div class="exec-value" style="color:#0e7490;">{sign}{csi_gap}</div>
        <div class="exec-sub">XYZ {csi_xyz_val}% · Komp {csi_komp_val}%</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)
with c3:
    cli_gap = round(cli_xyz_val - cli_komp_val, 1)
    sign = "+" if cli_gap >= 0 else ""
    bc = "badge-green" if cli_gap >= 0 else "badge-red"
    lbl = "Unggul" if cli_gap >= 0 else "Tertinggal"
    st.markdown(f"""<div class="exec-card teal">
        <span class="exec-icon">🔁</span>
        <div class="exec-label">CLI Gap (%)</div>
        <div class="exec-value" style="color:#0f5e5a;">{sign}{cli_gap}</div>
        <div class="exec-sub">XYZ {cli_xyz_val}% · Komp {cli_komp_val}%</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)
with c4:
    worst_img = img_gap_data[0]
    sign = "+" if worst_img["gap"] >= 0 else ""
    bc = "badge-red" if worst_img["gap"] < 0 else "badge-green"
    st.markdown(f"""<div class="exec-card red">
        <span class="exec-icon">⚠️</span>
        <div class="exec-label">Biggest Brand Gap</div>
        <div class="exec-value" style="color:#b91c1c;font-size:28px;">{worst_img['label']}</div>
        <div class="exec-sub">Gap {sign}{worst_img['gap']}/6 vs kompetitor</div>
        <span class="exec-badge {bc}">Prioritas</span>
    </div>""", unsafe_allow_html=True)

overall_pos = sum(1 for g in [nps_gap, csi_gap, cli_gap] if g > 0)
st.markdown(f'<div class="insight-box" style="margin-top:12px;">💡 Bank XYZ unggul di <b>{overall_pos}/3</b> KPI utama vs kompetitor. Atribut brand dengan gap terbesar adalah <b>{worst_img["label"]}</b> ({sign}{worst_img["gap"]}/6) — perlu campaign persepsi segera.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 1. COMPETITOR LANDSCAPE ───────────────────────────────────────────────────
st.markdown("""<div class="section-label">
    <span class="section-label-text">1 · Competitor Landscape — Peta Kompetitor Utama</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

def render_rank_table(col, counts, title, subtitle):
    top = counts.head(8).reset_index()
    top.columns = ["bank","count"]
    max_c = top["count"].max() if len(top) > 0 else 1
    rows = ""
    for i, row in top.iterrows():
        badge_cls_r = "top1" if i==0 else ("top2" if i==1 else ("top3" if i==2 else ""))
        bar_w = int(row["count"] / max_c * 100)
        bar_clr = "#1e40af" if i==0 else ("#3b82f6" if i==1 else ("#0e7490" if i==2 else "#d1d5db"))
        rows += f"""<tr>
            <td><span class="rank-badge {badge_cls_r}">{i+1}</span></td>
            <td style="font-weight:{'700' if i<3 else '500'};color:#1e293b;">{row['bank']}</td>
            <td style="text-align:right;">
                <div style="display:flex;align-items:center;gap:8px;justify-content:flex-end;">
                    <div style="width:60px;height:6px;background:#f1f5f9;border-radius:99px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{bar_clr};border-radius:99px;"></div>
                    </div>
                    <span style="font-family:'DM Serif Display',serif;font-size:15px;color:#1e40af;">{row['count']}</span>
                </div>
            </td>
        </tr>"""
    col.markdown(f"""
    <div class="card card-accent-blue">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:2px;">{title}</div>
        <div style="font-size:11px;color:#94a3b8;margin-bottom:14px;">{subtitle}</div>
        <table class="rank-table">{rows}</table>
    </div>""", unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns(3)
with col_l1: render_rank_table(col_l1, bank_aktif_counts, "Bank Aktif Digunakan", "Selain Bank XYZ")
with col_l2: render_rank_table(col_l2, komp_dana_counts,  "Kompetitor Simpan Dana", "Bank lain untuk menyimpan dana")
with col_l3: render_rank_table(col_l3, komp_trx_counts,   "Kompetitor Transaksi", "Bank lain untuk bertransaksi")

if len(bank_aktif_counts) > 0:
    top_comp = bank_aktif_counts.index[0]
    st.markdown(f'<div class="insight-box">💡 Kompetitor paling aktif digunakan nasabah selain XYZ adalah <b>{top_comp}</b>. Prioritaskan analisis gap dengan bank ini untuk strategi diferensiasi yang efektif.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 3. BRAND ATTRIBUTE GAP ────────────────────────────────────────────────────
st.markdown("""<div class="section-label">
    <span class="section-label-text">3 · Brand Attribute Gap Ranking — Dimana Kita Tertinggal?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_bg1, col_bg2 = st.columns([3,2])

with col_bg1:
    gap_labels = [d["label"] for d in img_gap_data]
    gap_vals   = [d["gap"]   for d in img_gap_data]
    bar_colors = ["#15803d" if g >= 0 else "#b91c1c" for g in gap_vals]

    fig_brand_gap = go.Figure(go.Bar(
        x=gap_vals, y=gap_labels, orientation="h",
        marker_color=bar_colors,
        text=[f"{'+' if g>=0 else ''}{g:.2f}" for g in gap_vals],
        textposition="outside", textfont=dict(color="#374151",size=11,family="Inter")))
    fig_brand_gap.add_vline(x=0, line_color="#e2e8f0", line_width=1.5)
    fig_brand_gap.update_layout(**PLOT,
        xaxis=dict(color="#64748b",gridcolor="#f1f5f9",title="Gap (XYZ − Kompetitor, skala /6)"),
        yaxis=dict(color="#374151",tickfont=dict(size=11,family="Inter"),autorange="reversed"),
        margin=dict(t=10,b=20,l=10,r=70), height=360)

    st.markdown("""<div class="card card-accent-blue">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:12px;">
            Gap per Atribut Brand — Merah = XYZ tertinggal · Hijau = XYZ unggul
        </div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_brand_gap, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    neg_gaps = [d for d in img_gap_data if d["gap"] < 0]
    if neg_gaps:
        worst_brand = neg_gaps[0]
        st.markdown(f'<div class="insight-box">💡 Atribut brand terlemah vs kompetitor: <b>{worst_brand["label"]}</b> (gap {worst_brand["gap"]:+.2f}/6). Investasi kampanye persepsi di area ini dapat meningkatkan posisi kompetitif secara signifikan.</div>', unsafe_allow_html=True)

with col_bg2:
    neg_gaps_list = [d for d in img_gap_data if d["gap"] < 0]
    pos_gaps_list = [d for d in img_gap_data if d["gap"] >= 0]
    neg_rows = "".join([f'<div class="gap-item"><span class="gap-label">{d["label"]}</span><span class="gap-val-neg">{d["gap"]:+.2f}</span></div>' for d in neg_gaps_list])
    pos_rows = "".join([f'<div class="gap-item"><span class="gap-label">{d["label"]}</span><span class="gap-val-pos">{d["gap"]:+.2f}</span></div>' for d in pos_gaps_list])

    st.markdown(f"""
    <div class="card card-accent-red" style="margin-bottom:12px;">
        <div class="reason-title reason-neg-title">▼ Atribut Tertinggal dari Kompetitor</div>
        {neg_rows if neg_rows else '<div style="font-size:12px;color:#64748b;">Tidak ada gap negatif</div>'}
    </div>
    <div class="card card-accent-teal">
        <div class="reason-title" style="color:#166534;">▲ Atribut Unggul vs Kompetitor</div>
        {pos_rows if pos_rows else '<div style="font-size:12px;color:#64748b;">Tidak ada gap positif</div>'}
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 4. TOUCHPOINT GAP RANKING ─────────────────────────────────────────────────
st.markdown("""<div class="section-label">
    <span class="section-label-text">4 · Touchpoint Gap Ranking — Di Experience Mana Kompetitor Unggul?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_tp1, col_tp2 = st.columns([2,3])

with col_tp1:
    tp_sorted_comp = sorted(tp_data, key=lambda x: x["gap"])
    rows_tp = ""
    for d in tp_sorted_comp:
        gap_clr = "#15803d" if d["gap"] >= 0 else "#b91c1c"
        sign    = "+" if d["gap"] >= 0 else ""
        xyz_clr = pct_color(d["xyz"])
        rows_tp += f"""<tr>
            <td style="font-weight:600;color:#1e293b;">{d['label']}</td>
            <td style="text-align:right;font-family:'DM Serif Display',serif;font-size:18px;color:{xyz_clr};">{d['xyz']}%</td>
            <td style="text-align:right;font-size:12px;color:#64748b;">{d['komp']}%</td>
            <td style="text-align:right;font-weight:700;color:{gap_clr};">{sign}{d['gap']}%</td>
        </tr>"""

    st.markdown(f"""
    <div class="card card-accent-blue">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#64748b;margin-bottom:12px;">Ranking Gap Touchpoint</div>
        <table class="rank-table">
            <thead><tr>
                <th>Touchpoint</th><th class="right">XYZ</th>
                <th class="right">Komp</th><th class="right">Gap</th>
            </tr></thead>
            <tbody>{rows_tp}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)
    worst_tp = tp_sorted_comp[0]
    st.markdown(f'<div class="insight-box">💡 Touchpoint dengan gap terburuk: <b>{worst_tp["label"]}</b> (XYZ {worst_tp["xyz"]}% vs Komp {worst_tp["komp"]}%, gap {worst_tp["gap"]:+}%). Prioritaskan perbaikan SOP di area ini.</div>', unsafe_allow_html=True)

with col_tp2:
    tp_labels_c = [d["label"] for d in tp_sorted_comp]
    tp_xyz_c    = [d["xyz"]   for d in tp_sorted_comp]
    tp_komp_c   = [d["komp"]  for d in tp_sorted_comp]

    fig_tp = go.Figure()
    fig_tp.add_trace(go.Bar(name="Bank XYZ", x=tp_labels_c, y=tp_xyz_c,
        marker_color="#1e40af",
        text=[f"{v}%" for v in tp_xyz_c],
        textposition="outside", textfont=dict(color="#374151",size=10,family="Inter")))
    fig_tp.add_trace(go.Bar(name="Kompetitor", x=tp_labels_c, y=tp_komp_c,
        marker_color="#3b82f6",
        text=[f"{v}%" for v in tp_komp_c],
        textposition="outside", textfont=dict(color="#374151",size=10,family="Inter")))
    fig_tp.update_layout(**PLOT, barmode="group",
        xaxis=dict(color="#64748b",gridcolor="#f1f5f9"),
        yaxis=dict(color="#64748b",gridcolor="#f1f5f9",range=[0,115],title="Score (%)"),
        legend=dict(font=dict(color="#374151",size=11,family="Inter"),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=10,b=10,l=10,r=10), height=280)
    st.plotly_chart(fig_tp, use_container_width=True)

    # Radar
    dims   = [d["label"] for d in tp_data]
    xyz_r  = [d["xyz"]   for d in tp_data]
    komp_r = [d["komp"]  for d in tp_data]
    dims_c = dims + [dims[0]]
    xyz_c  = xyz_r  + [xyz_r[0]]
    komp_c = komp_r + [komp_r[0]]

    fig_rad = go.Figure()
    fig_rad.add_trace(go.Scatterpolar(
        r=xyz_c, theta=dims_c, fill="toself",
        fillcolor="rgba(30,64,175,0.10)", line=dict(color="#1e40af",width=2.5), name="Bank XYZ"))
    fig_rad.add_trace(go.Scatterpolar(
        r=komp_c, theta=dims_c, fill="toself",
        fillcolor="rgba(59,130,246,0.10)", line=dict(color="#3b82f6",width=2,dash="dot"), name="Kompetitor"))
    fig_rad.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(range=[0,110],color="#64748b",gridcolor="#e2e8f0"),
                   angularaxis=dict(color="#64748b",gridcolor="#e2e8f0",tickfont=dict(size=9))),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter",color="#374151",size=11),
        legend=dict(font=dict(color="#374151",size=11,family="Inter"),bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20,b=20,l=20,r=20), height=280)
    st.plotly_chart(fig_rad, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 5. REASON ANALYSIS ────────────────────────────────────────────────────────
st.markdown("""<div class="section-label">
    <span class="section-label-text">5 · Reason Analysis — Mengapa Nasabah Merekomendasikan / Puas?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

def get_top_reasons(df, sentiment_col, category_col, sentiment_val, n=8):
    if sentiment_col not in df.columns or category_col not in df.columns:
        return pd.Series(dtype=int)
    sub = df[df[sentiment_col] == sentiment_val][category_col].dropna()
    sub = sub[sub.astype(str).str.strip() != ""]
    return sub.value_counts().head(n)

def get_text_top(col, n=8):
    if col not in df.columns: return pd.Series(dtype=int)
    words = []
    for v in df[col].dropna():
        for w in str(v).split(","):
            w = w.strip()
            if len(w) > 3: words.append(w)
    return pd.Series(words).value_counts().head(n)

def reason_card(col, counts, title, title_cls_color, color):
    if len(counts) == 0:
        col.markdown(f"""<div class="reason-card">
            <div class="reason-title" style="color:{title_cls_color};">{title}</div>
            <div style="font-size:12px;color:#64748b;">Tidak ada data</div>
        </div>""", unsafe_allow_html=True)
        return
    fig = go.Figure(go.Bar(
        x=counts.values, y=counts.index, orientation="h",
        marker_color=color,
        text=counts.values, textposition="outside",
        textfont=dict(color="#374151",size=10,family="Inter")))
    fig.update_layout(**PLOT,
        xaxis=dict(color="#64748b",gridcolor="#f1f5f9"),
        yaxis=dict(color="#374151",tickfont=dict(size=9,family="Inter"),autorange="reversed"),
        margin=dict(t=6,b=6,l=6,r=50), height=260)
    col.markdown(f"""<div class="reason-card">
        <div class="reason-title" style="color:{title_cls_color};">{title}</div>
    </div>""", unsafe_allow_html=True)
    col.plotly_chart(fig, use_container_width=True)

tab_nps, tab_csi = st.tabs(["NPS — Alasan Rekomendasi","CSI — Alasan Kepuasan"])

with tab_nps:
    col_r1,col_r2,col_r3,col_r4 = st.columns(4)
    nps_xyz_pos  = get_top_reasons(df,"nps_xyz_sentimen", "nps_xyz_kategori", "POSITIVE COMMENTS")
    nps_xyz_neg  = get_top_reasons(df,"nps_xyz_sentimen", "nps_xyz_kategori", "NEGATIVE COMMENTS")
    nps_komp_pos = get_top_reasons(df,"nps_komp_sentimen","nps_komp_kategori","POSITIVE COMMENTS")
    nps_komp_neg = get_top_reasons(df,"nps_komp_sentimen","nps_komp_kategori","NEGATIVE COMMENTS")
    reason_card(col_r1, nps_xyz_pos,  "▲ Positif NPS — XYZ",        "#166534", "#0f5e5a")
    reason_card(col_r2, nps_xyz_neg,  "▼ Negatif NPS — XYZ",        "#991b1b", "#b91c1c")
    reason_card(col_r3, nps_komp_pos, "▲ Positif NPS — Kompetitor", "#854d0e", "#b45309")
    reason_card(col_r4, nps_komp_neg, "▼ Negatif NPS — Kompetitor", "#64748b", "#94a3b8")

with tab_csi:
    col_c1,col_c2,col_c3,col_c4 = st.columns(4)
    csi_xyz_pos  = get_top_reasons(df,"alasan_csi_xyz","alasan_csi_xyz","POSITIVE COMMENTS")
    csi_xyz_neg  = get_top_reasons(df,"alasan_csi_xyz","alasan_csi_xyz","NEGATIVE COMMENTS")
    csi_komp_pos = get_top_reasons(df,"alasan_csi_kompetitor","alasan_csi_kompetitor","POSITIVE COMMENTS")
    csi_komp_neg = get_top_reasons(df,"alasan_csi_kompetitor","alasan_csi_kompetitor","NEGATIVE COMMENTS")
    if len(csi_xyz_pos)  == 0: csi_xyz_pos  = get_text_top("alasan_csi_xyz")
    if len(csi_komp_pos) == 0: csi_komp_pos = get_text_top("alasan_csi_kompetitor")
    reason_card(col_c1, csi_xyz_pos,  "▲ Alasan CSI Positif — XYZ",        "#166534", "#0f5e5a")
    reason_card(col_c2, csi_xyz_neg,  "▼ Alasan CSI Negatif — XYZ",        "#991b1b", "#b91c1c")
    reason_card(col_c3, csi_komp_pos, "▲ Alasan CSI Positif — Kompetitor", "#854d0e", "#b45309")
    reason_card(col_c4, csi_komp_neg, "▼ Alasan CSI Negatif — Kompetitor", "#64748b", "#94a3b8")

st.markdown("<br>", unsafe_allow_html=True)

# ── 6. OPPORTUNITY MATRIX ─────────────────────────────────────────────────────
st.markdown("""<div class="section-label">
    <span class="section-label-text">6 · Opportunity Matrix — Area Prioritas Perbaikan</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_opp1, col_opp2 = st.columns([2,3])

with col_opp1:
    opp_items = []
    for d in img_gap_data:
        if d["gap"] < 0:
            abs_gap  = abs(d["gap"])
            priority = "Tinggi" if abs_gap > 0.3 else ("Menengah" if abs_gap > 0.15 else "Rendah")
            pill_cls = "pill-high" if priority=="Tinggi" else ("pill-med" if priority=="Menengah" else "pill-low")
            opp_items.append({"area":d["label"],"type":"Brand Image","gap":d["gap"],"abs_gap":abs_gap,"priority":priority,"pill_cls":pill_cls})
    for d in tp_data:
        if d["gap"] < 0:
            abs_gap  = abs(d["gap"])
            priority = "Tinggi" if abs_gap > 5 else ("Menengah" if abs_gap > 2 else "Rendah")
            pill_cls = "pill-high" if priority=="Tinggi" else ("pill-med" if priority=="Menengah" else "pill-low")
            opp_items.append({"area":d["label"],"type":"Touchpoint","gap":d["gap"],"abs_gap":abs_gap,"priority":priority,"pill_cls":pill_cls})
    opp_items.sort(key=lambda x: x["abs_gap"], reverse=True)

    st.markdown('<div style="font-size:11px;color:#64748b;margin-bottom:12px;">Diurutkan berdasarkan besarnya gap vs kompetitor.</div>', unsafe_allow_html=True)
    for i, item in enumerate(opp_items[:8]):
        sign = "+" if item["gap"] >= 0 else ""
        st.markdown(f"""
        <div class="opp-item">
            <div class="opp-rank">{i+1}</div>
            <div class="opp-body">
                <div class="opp-area">{item['area']}</div>
                <div class="opp-meta">{item['type']} · Gap {sign}{item['gap']}</div>
            </div>
            <span class="opp-pill {item['pill_cls']}">{item['priority']}</span>
        </div>""", unsafe_allow_html=True)

    if not opp_items:
        st.markdown("""<div class="card"><div style="text-align:center;padding:32px 0;color:#64748b;font-size:14px;">
            ✅ Tidak ada gap negatif — XYZ unggul di semua area
        </div></div>""", unsafe_allow_html=True)

    if opp_items:
        top_prio = [item for item in opp_items if item["priority"]=="Tinggi"]
        st.markdown(f'<div class="insight-box">💡 Terdapat <b>{len(top_prio)} area prioritas tinggi</b> yang perlu ditangani segera. Fokus pada yang paling berdampak terhadap persepsi nasabah dan NPS.</div>', unsafe_allow_html=True)

with col_opp2:
    if opp_items:
        opp_labels  = [d["area"]     for d in opp_items[:10]]
        opp_gaps    = [d["gap"]      for d in opp_items[:10]]
        opp_types   = [d["type"]     for d in opp_items[:10]]
        opp_sizes   = [max(abs(d["gap"])*30,8) for d in opp_items[:10]]
        opp_prios   = [d["priority"] for d in opp_items[:10]]

        fig_opp = go.Figure()
        for prio, color in [("Tinggi","#b91c1c"),("Menengah","#b45309"),("Rendah","#15803d")]:
            idx = [i for i,d in enumerate(opp_items[:10]) if d["priority"]==prio]
            if not idx: continue
            fig_opp.add_trace(go.Scatter(
                x=[opp_gaps[i] for i in idx], y=[opp_labels[i] for i in idx],
                mode="markers+text", name=f"Prioritas {prio}",
                marker=dict(size=[opp_sizes[i] for i in idx], color=color,
                            opacity=0.85, line=dict(color="white",width=2)),
                text=[f"{opp_gaps[i]:+}" for i in idx],
                textfont=dict(color="white",size=10,family="Inter"),
                textposition="middle center",
                hovertemplate="%{y}<br>Gap: %{x}<extra></extra>"))
        fig_opp.add_vline(x=0, line_color="#e2e8f0", line_width=1.5, line_dash="dot")
        fig_opp.update_layout(**PLOT,
            xaxis=dict(color="#64748b",gridcolor="#f1f5f9",title="Gap vs Kompetitor",zeroline=False),
            yaxis=dict(color="#374151",tickfont=dict(size=11,family="Inter"),
                       categoryorder="array",categoryarray=opp_labels[::-1]),
            legend=dict(font=dict(color="#374151",size=11),bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=10,b=20,l=10,r=20), height=420)
        st.plotly_chart(fig_opp, use_container_width=True)
    else:
        st.markdown("""<div class="card" style="text-align:center;padding:60px 0;">
            <div style="font-size:36px;margin-bottom:12px;">🏆</div>
            <div style="font-family:'DM Serif Display',serif;font-size:20px;color:#1e40af;">XYZ Unggul di Semua Area</div>
            <div style="font-size:12px;color:#64748b;margin-top:6px;">Tidak ada gap negatif terhadap kompetitor</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)