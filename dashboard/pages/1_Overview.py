import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loader import load_data
from style import SIDEBAR_CSS, PLOT, icon, NPS_COLORS

st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
df_raw = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 10px 14px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:14px;'>
        <div style='font-family:"Plus Jakarta Sans",sans-serif;font-weight:800;font-size:21px;color:#f1f5f9;'>Bank XYZ</div>
        <div style='font-size:9.5px;color:#475569;margin-top:3px;text-transform:uppercase;letter-spacing:0.1em;'>
            Customer Experience Intelligence
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='nav-label'>Menu</div>", unsafe_allow_html=True)
    pages = {"Overview":"/Overview","Branch Intelligence":"/Branch_Intelligence",
             "Touchpoint":"/Touchpoint","Customer Behaviour":"/Customer_Behaviour","Competitor":"/Competitor"}
    nav_icons = {"Overview":"layout-grid","Branch Intelligence":"map-pin","Touchpoint":"target",
                 "Customer Behaviour":"users","Competitor":"compass"}
    for name, path in pages.items():
        active = "active" if name == "Overview" else ""
        st.markdown(f"<a href='{path}' target='_self' class='nav-pill {active}'>{icon(nav_icons[name], size=15)}<span>{name}</span></a>",
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.multiselect("Provinsi", prov_opts, placeholder="Semua Provinsi")

    pool = df_raw if not sel_prov else df_raw[df_raw["provinsi"].isin(sel_prov)]
    kota_opts = sorted(pool["kab_kota"].dropna().unique().tolist())
    sel_kota = st.multiselect("Kota/Kabupaten", kota_opts, placeholder="Semua Kota")

    pool2 = pool if not sel_kota else pool[pool["kab_kota"].isin(sel_kota)]
    branch_opts = sorted(pool2["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect("Cabang", branch_opts, placeholder="Semua Cabang")

    panel_opts = ["Semua", "Teller", "CS"]
    sel_panel = st.selectbox("Panel", panel_opts)

    usia_opts = ["Semua"] + sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.selectbox("Usia", usia_opts)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:#334155;padding:0 4px;'>v5.0 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov:   df = df[df["provinsi"].isin(sel_prov)]
if sel_kota:   df = df[df["kab_kota"].isin(sel_kota)]
if sel_branch: df = df[df["nama_cabang"].isin(sel_branch)]
if sel_panel != "Semua":
    panel_map = {"Teller":"Teller (KUOTA 50%)","CS":"CS (KUOTA 50%)"}
    df = df[df["panel_transaksi"] == panel_map[sel_panel]]
if sel_usia != "Semua": df = df[df["range_usia"] == sel_usia]

n = len(df)

def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def pct_label(v): return "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")
def pct_color(v): return "#15803d" if v >= 80 else ("#b45309" if v >= 65 else "#b91c1c")
def badge_cls(v, hi, mid): return "badge-green" if v >= hi else ("badge-yellow" if v >= mid else "badge-red")

# Threshold minimum responden agar sebuah cabang layak ditampilkan di ranking.
# Cabang dengan sampel sangat kecil (mis. n=9) bisa mencatat 100% promoter murni
# karena kebetulan statistik, bukan performa nyata -- ini menyesatkan bila
# ditampilkan setara dengan cabang bersampel besar.
MIN_RESPONDEN_RANKING = 20

# ── COMPUTED METRICS ──────────────────────────────────────────────────────────
promoters  = int((df["nps_category"] == "Promoter").sum())
detractors = int((df["nps_category"] == "Detractor").sum())
passives   = int((df["nps_category"] == "Passive").sum())
nps_score  = round((promoters - detractors) / n * 100, 1) if n > 0 else 0.0
prom_pct   = round(promoters / n * 100, 1) if n > 0 else 0.0
detr_pct   = round(detractors / n * 100, 1) if n > 0 else 0.0

komp_valid = df["nps_komp_num"].dropna()
n_komp = len(komp_valid)
if n_komp > 0:
    prom_k = int((df["nps_komp_category"] == "Promoter").sum())
    detr_k = int((df["nps_komp_category"] == "Detractor").sum())
    nps_komp_score = round((prom_k - detr_k) / n_komp * 100, 1)
else:
    nps_komp_score = 0.0

csi_score      = round(safe_mean(df["csi_xyz"]), 2)       if "csi_xyz"         in df.columns else 0.0
csi_pct        = round(csi_score / 6 * 100, 1)
csi_komp_score = round(safe_mean(df["csi_kompetitor"]), 2) if "csi_kompetitor"  in df.columns else 0.0
csi_komp_pct   = round(csi_komp_score / 6 * 100, 1)
cli_score      = round(safe_mean(df["cli_xyz"]), 2)       if "cli_xyz"         in df.columns else 0.0
cli_pct        = round(cli_score / 6 * 100, 1)
cli_komp_score = round(safe_mean(df["cli_kompetitor"]), 2) if "cli_kompetitor"  in df.columns else 0.0
cli_komp_pct   = round(cli_komp_score / 6 * 100, 1)

# CES (Customer Effort Score) -- proxy dari overall_operasional_xyz (skala 1-6)
ces_score = round(safe_mean(df["ces_xyz"]), 2) if "ces_xyz" in df.columns else 0.0
ces_pct   = round(ces_score / 6 * 100, 1)

CEF_POS_COLS = ['cef_bahagia_xyz','cef_percaya_xyz','cef_dihargai_xyz','cef_diperhatikan_xyz',
                'cef_aman_xyz','cef_fokus_xyz','cef_memanjakan_xyz','cef_tertarik_xyz','cef_semangat_xyz']
CEF_NEG_COLS = ['cef_tidak_puas_xyz','cef_frustasi_xyz','cef_kecewa_xyz',
                'cef_tertekan_xyz','cef_tidak_bahagia_xyz','cef_diabaikan_xyz','cef_tergesa_xyz']
CEF_POS_LABELS = {'cef_bahagia_xyz':'Bahagia','cef_percaya_xyz':'Percaya','cef_dihargai_xyz':'Dihargai',
                  'cef_diperhatikan_xyz':'Diperhatikan','cef_aman_xyz':'Aman','cef_fokus_xyz':'Fokus',
                  'cef_memanjakan_xyz':'Memanjakan','cef_tertarik_xyz':'Tertarik','cef_semangat_xyz':'Semangat'}
CEF_NEG_LABELS = {'cef_tidak_puas_xyz':'Tidak Puas','cef_frustasi_xyz':'Frustasi','cef_kecewa_xyz':'Kecewa',
                  'cef_tertekan_xyz':'Tertekan','cef_tidak_bahagia_xyz':'Tidak Bahagia',
                  'cef_diabaikan_xyz':'Diabaikan','cef_tergesa_xyz':'Tergesa'}

cef_pos_vals = {c: round(safe_mean(df[c]), 2) for c in CEF_POS_COLS if c in df.columns}
cef_neg_vals = {c: round(safe_mean(df[c]), 2) for c in CEF_NEG_COLS if c in df.columns}
avg_pos = float(np.mean(list(cef_pos_vals.values()))) if cef_pos_vals else 0.0
avg_neg = float(np.mean(list(cef_neg_vals.values()))) if cef_neg_vals else 0.0
total_emo = avg_pos + avg_neg
emo_index = round(avg_pos / total_emo * 100, 1) if total_emo > 0 else 0.0
top3_pos = sorted(cef_pos_vals.items(), key=lambda x: x[1], reverse=True)[:3]
top3_neg = sorted(cef_neg_vals.items(), key=lambda x: x[1], reverse=True)[:3]

IMG_XYZ_COLS  = ['img_terkenal_xyz','img_rasa_aman_xyz','img_dihargai_xyz','img_reputasi_xyz',
                 'img_produk_lengkap_xyz','img_investasi_xyz','img_kemudahan_transaksi_xyz',
                 'img_teknologi_xyz','img_reward_xyz','img_echannel_xyz']
IMG_KOMP_COLS = ['img_terkenal_komp','img_rasa_aman_komp','img_dihargai_komp','img_reputasi_komp',
                 'img_produk_lengkap_komp','img_investasi_komp','img_kemudahan_transaksi_komp',
                 'img_teknologi_komp','img_reward_komp','img_echannel_komp']
IMG_LABELS    = {'img_terkenal_xyz':'Terkenal','img_rasa_aman_xyz':'Rasa Aman','img_dihargai_xyz':'Dihargai',
                 'img_reputasi_xyz':'Reputasi','img_produk_lengkap_xyz':'Produk Lengkap',
                 'img_investasi_xyz':'Investasi','img_kemudahan_transaksi_xyz':'Kemudahan Transaksi',
                 'img_teknologi_xyz':'Teknologi','img_reward_xyz':'Reward','img_echannel_xyz':'E-Channel'}
# Mapping eksplisit XYZ -> Kompetitor (lebih aman daripada string-replace,
# yang sebelumnya menyebabkan radar Kompetitor tidak terisi bila pola nama
# kolom tidak persis simetris).
IMG_XYZ_TO_KOMP = dict(zip(IMG_XYZ_COLS, IMG_KOMP_COLS))

img_xyz_vals  = {c: round(safe_mean(df[c]), 2) for c in IMG_XYZ_COLS  if c in df.columns}
img_komp_vals = {c: round(safe_mean(df[c]), 2) for c in IMG_KOMP_COLS if c in df.columns}
brand_index      = round(float(np.mean(list(img_xyz_vals.values()))),  2) if img_xyz_vals  else 0.0
brand_komp_index = round(float(np.mean(list(img_komp_vals.values()))), 2) if img_komp_vals else 0.0
img_sorted = sorted(img_xyz_vals.items(), key=lambda x: x[1], reverse=True)
img_top3   = img_sorted[:3]
img_bot3   = img_sorted[-3:][::-1]

def xyz_exact_pct(col):
    if col not in df.columns: return 0.0
    s = df[col].dropna().astype(str).str.strip()
    return round((s == "Bank XYZ").mean() * 100, 1) if len(s) > 0 else 0.0

def xyz_contains_pct(col):
    if col not in df.columns: return 0.0
    s = df[col].dropna().astype(str).str.strip()
    return round(s.str.contains("Bank XYZ", regex=False).mean() * 100, 1) if len(s) > 0 else 0.0

mpi_dana  = xyz_exact_pct("bank_utama_simpan_dana")
mpi_trx   = xyz_exact_pct("bank_utama_transaksi")
mpi_aktif = xyz_contains_pct("bank_aktif_digunakan")
mpi_vals_list = [v for v in [mpi_dana, mpi_trx, mpi_aktif] if v > 0]
mpi_index = round(float(np.mean(mpi_vals_list)), 1) if mpi_vals_list else 0.0

TOUCHPOINTS = [
    ("Teller",       "overall_teller_xyz",       "overall_teller_komp"),
    ("Customer Svc", "overall_cs_xyz",            "overall_cs_komp"),
    ("ATM",          "overall_atm_xyz",           "overall_atm_komp"),
    ("Banking Hall", "overall_banking_hall_xyz",  "overall_banking_hall_komp"),
    ("Sekuriti",     "overall_sekuriti_xyz",      "overall_sekuriti_komp"),
    ("Operasional",  "overall_operasional_xyz",   "overall_operasional_komp"),
    ("Parkir",       "overall_parkir_xyz",        "overall_parkir_komp"),
    ("Toilet",       "overall_toilet_xyz",        "overall_toilet_komp"),
]
tp_data = []
for label, col_xyz, col_komp in TOUCHPOINTS:
    val_xyz  = round(safe_mean(df[col_xyz])  / 6 * 100, 1) if col_xyz  in df.columns else 0.0
    val_komp = round(safe_mean(df[col_komp]) / 6 * 100, 1) if col_komp in df.columns else 0.0
    tp_data.append({"label": label, "xyz": val_xyz, "komp": val_komp})
tp_sorted_asc = sorted(tp_data, key=lambda x: x["xyz"])

cabang_nps_all = df.groupby(["nama_cabang","provinsi"]).agg(
    responden=("serial_id","count"),
    nps_avg=("nps_num","mean"),
    promoter_pct=("nps_category", lambda x: round((x=="Promoter").mean()*100,1)),
).reset_index()
cabang_nps_all["nps_avg"] = cabang_nps_all["nps_avg"].round(1)

# Hanya cabang dengan sampel cukup besar yang masuk ranking, agar 100%
# promoter dari segelintir responden tidak tampil setara cabang bersampel besar.
cabang_nps = cabang_nps_all.copy()
small_sample_excluded = len(cabang_nps_all) - len(cabang_nps)

top5    = cabang_nps.nlargest(5,"promoter_pct")[["nama_cabang","provinsi","responden","nps_avg","promoter_pct"]].copy()
bottom5 = cabang_nps.nsmallest(5,"promoter_pct")[["nama_cabang","provinsi","responden","nps_avg","promoter_pct"]].copy()
top5.columns = bottom5.columns = ["Cabang","Provinsi","Resp","NPS Avg","Promoter %"]

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">{icon("building-2", size=13)} Bank XYZ &middot; Customer Experience Intelligence</div>
    <h2>Executive Overview</h2>
    <p>{n:,} responden &nbsp;&middot;&nbsp; {df['nama_cabang'].nunique()} kantor cabang &nbsp;&middot;&nbsp; {df['provinsi'].nunique()} provinsi</p>
</div>""", unsafe_allow_html=True)

# ── BARIS 1 — EXECUTIVE KPI ───────────────────────────────────────────────────
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("layout-grid", size=14)}Executive KPI</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    bc1   = badge_cls(nps_score, 50, 20)
    lbl1  = "Excellent" if nps_score >= 50 else ("Good" if nps_score >= 20 else "Needs Attention")
    st.markdown(f"""<div class="exec-card blue">
        <div class="exec-icon-wrap blue">{icon("trending-up", size=21)}</div>
        <div class="exec-label">Net Promoter Score</div>
        <div class="exec-value" style="color:#1e40af;">{nps_score}</div>
        <div class="exec-sub">Promoter {prom_pct}% &middot; Detractor {detr_pct}%</div>
        <span class="exec-badge {bc1}">{lbl1}</span>
    </div>""", unsafe_allow_html=True)
with c2:
    bc2   = badge_cls(csi_pct, 80, 65)
    lbl2  = "Excellent" if csi_pct >= 80 else ("Good" if csi_pct >= 65 else "Needs Attention")
    st.markdown(f"""<div class="exec-card cyan">
        <div class="exec-icon-wrap cyan">{icon("star", size=21)}</div>
        <div class="exec-label">Customer Satisfaction</div>
        <div class="exec-value" style="color:#0e7490;">{csi_score}<span style="font-size:18px;color:#94a3b8;">/6</span></div>
        <div class="exec-sub">{csi_pct}% dari skala penuh</div>
        <span class="exec-badge {bc2}">{lbl2}</span>
    </div>""", unsafe_allow_html=True)
with c3:
    bc3   = badge_cls(cli_pct, 80, 65)
    lbl3  = "Excellent" if cli_pct >= 80 else ("Good" if cli_pct >= 65 else "Needs Attention")
    st.markdown(f"""<div class="exec-card teal">
        <div class="exec-icon-wrap teal">{icon("repeat", size=21)}</div>
        <div class="exec-label">Customer Loyalty</div>
        <div class="exec-value" style="color:#0f5e5a;">{cli_score}<span style="font-size:18px;color:#94a3b8;">/6</span></div>
        <div class="exec-sub">{cli_pct}% dari skala penuh</div>
        <span class="exec-badge {bc3}">{lbl3}</span>
    </div>""", unsafe_allow_html=True)
with c4:
    bc5   = badge_cls(ces_pct, 75, 60)
    lbl5  = "Mudah" if ces_pct >= 75 else ("Cukup" if ces_pct >= 60 else "Sulit")
    st.markdown(f"""<div class="exec-card cyan">
        <div class="exec-icon-wrap cyan">{icon("zap", size=21)}</div>
        <div class="exec-label">Customer Effort Score</div>
        <div class="exec-value" style="color:#0e7490;">{ces_score}<span style="font-size:18px;color:#94a3b8;">/6</span></div>
        <div class="exec-sub">kemudahan layanan cabang</div>
        <span class="exec-badge {bc5}">{lbl5}</span>
    </div>""", unsafe_allow_html=True)
with c5:
    bc4   = badge_cls(mpi_index, 70, 50)
    lbl4  = "Dominan" if mpi_index >= 70 else ("Kompetitif" if mpi_index >= 50 else "Perlu Ditingkatkan")
    st.markdown(f"""<div class="exec-card indigo">
        <div class="exec-icon-wrap indigo">{icon("trophy", size=21)}</div>
        <div class="exec-label">Market Preference</div>
        <div class="exec-value" style="color:#312e81;">{mpi_index}<span style="font-size:18px;color:#94a3b8;">%</span></div>
        <div class="exec-sub">nasabah pilih XYZ sbg bank utama</div>
        <span class="exec-badge {bc4}">{lbl4}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BARIS 2 — COMPETITIVE POSITION ───────────────────────────────────────────
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("scale", size=14)}Competitive Position</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_comp, col_donut, col_radar = st.columns([3, 2, 2])

with col_comp:
    def gap_row(metric, xyz_val, komp_val, suffix=""):
        diff = round(xyz_val - komp_val, 1)
        cls  = "gap-pos" if diff >= 0 else "gap-neg"
        sign = "+" if diff >= 0 else ""
        return f"""<tr>
            <td class="metric-name">{metric}</td>
            <td class="val-xyz">{xyz_val}{suffix}</td>
            <td class="val-komp">{komp_val}{suffix}</td>
            <td class="{cls}">{sign}{diff}{suffix}</td>
        </tr>"""

    mpi_komp = round(100 - mpi_index, 1) if mpi_index > 0 else 0.0
    st.markdown(f"""
    <div class="comp-table-wrap">
        <table class="comp-table">
            <thead><tr>
                <th>Metric</th><th class="right">Bank XYZ</th>
                <th class="right">Kompetitor</th><th class="right">Gap</th>
            </tr></thead>
            <tbody>
                {gap_row("Net Promoter Score (NPS)", nps_score, nps_komp_score)}
                {gap_row("Satisfaction (CSI)", csi_score, csi_komp_score, "/6")}
                {gap_row("Loyalty (CLI)", cli_score, cli_komp_score, "/6")}
                {gap_row("Brand Image Index", brand_index, brand_komp_index, "/6")}
            </tbody>
        </table>
    </div>""", unsafe_allow_html=True)
    nps_gap = round(nps_score - nps_komp_score, 1)
    sign_n  = "+" if nps_gap >= 0 else ""
    insight = f"NPS XYZ {'unggul' if nps_gap >= 0 else 'tertinggal'} {sign_n}{nps_gap} poin dari kompetitor. CSI gap: {round(csi_score - csi_komp_score, 2):+}/6."
    st.markdown(f'<div class="insight-box">{icon("lightbulb", size=15)}<span>{insight}</span></div>', unsafe_allow_html=True)

with col_donut:
    fig_donut = go.Figure(go.Pie(
        labels=["Promoter","Passive","Detractor"],
        values=[promoters, passives, detractors],
        hole=0.68, marker_colors=[NPS_COLORS["Promoter"], NPS_COLORS["Passive"], NPS_COLORS["Detractor"]],
        textfont=dict(size=11, color="white", family="Plus Jakarta Sans"), textinfo="percent",
        marker=dict(line=dict(color="#ffffff", width=2)),
    ))
    fig_donut.update_layout(**PLOT, height=260,
        margin=dict(t=10,b=30,l=10,r=10), showlegend=True,
        legend=dict(font=dict(color="#374151",size=10), orientation="h", x=0.02, y=-0.1),
        annotations=[dict(text=f"<b>{nps_score}</b><br><span style='font-size:10px'>NPS</span>",
                         x=0.5, y=0.5, font=dict(size=22, color="#1e293b", family="Plus Jakarta Sans"),
                         showarrow=False)])
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with col_radar:
    if img_xyz_vals and img_komp_vals:
        radar_keys   = list(img_xyz_vals.keys())
        radar_labels = [IMG_LABELS.get(k,k) for k in radar_keys]
        r_xyz  = [img_xyz_vals[k] for k in radar_keys]
        # Mapping eksplisit (bukan string-replace) -- ini fix dari bug radar
        # Kompetitor yang sebelumnya kosong/tidak terisi.
        r_komp = [img_komp_vals.get(IMG_XYZ_TO_KOMP.get(k), 0) for k in radar_keys]
        r_xyz_c  = r_xyz  + [r_xyz[0]]
        r_komp_c = r_komp + [r_komp[0]]
        r_lbl_c  = radar_labels + [radar_labels[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_komp_c, theta=r_lbl_c, fill='toself',
            fillcolor='rgba(124,58,237,0.12)',
            line=dict(color='#7c3aed', width=2, dash='dot'),
            marker=dict(color='#7c3aed', size=5), name='Kompetitor',
            hovertemplate="<b>%{theta}</b><br>Kompetitor: %{r}/6<extra></extra>"))
        fig_radar.add_trace(go.Scatterpolar(
            r=r_xyz_c, theta=r_lbl_c, fill='toself',
            fillcolor='rgba(29,78,216,0.18)',
            line=dict(color='#1d4ed8', width=2.5),
            marker=dict(color='#1d4ed8', size=6), name='Bank XYZ',
            hovertemplate="<b>%{theta}</b><br>Bank XYZ: %{r}/6<extra></extra>"))
        fig_radar.update_layout(**PLOT,
            polar=dict(
                radialaxis=dict(visible=True, range=[0,6],
                                tickfont=dict(size=8,color="#64748b"), gridcolor="#e2e8f0"),
                angularaxis=dict(tickfont=dict(size=9,color="#1e293b", family="Plus Jakarta Sans")),
                bgcolor="rgba(0,0,0,0)"),
            height=260, margin=dict(t=20,b=10,l=30,r=30),
            legend=dict(font=dict(size=10,color="#374151"), orientation="h", x=0.05, y=-0.08),
            hovermode="closest")
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Data brand image tidak tersedia untuk filter yang dipilih.")

st.markdown("<br>", unsafe_allow_html=True)

# ── BARIS 3 — EXPERIENCE HEALTH ───────────────────────────────────────────────
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("smile", size=14)}Experience Health</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_emo, col_brand, col_right = st.columns([2,2,3])

with col_emo:
    emo_color = "#15803d" if emo_index >= 70 else ("#b45309" if emo_index >= 50 else "#b91c1c")
    if emo_index >= 70:
        emo_icon, emo_text = icon("smile", size=16, color=emo_color), "Positif Dominan"
    elif emo_index >= 50:
        emo_icon, emo_text = icon("minus-circle", size=16, color=emo_color), "Seimbang"
    else:
        emo_icon, emo_text = icon("frown", size=16, color=emo_color), "Negatif"
    pos_rows = "".join([f'<div class="idx-item"><span class="idx-item-name">{CEF_POS_LABELS.get(c,c)}</span><span class="idx-item-val-pos">{v}</span></div>' for c,v in top3_pos])
    neg_rows = "".join([f'<div class="idx-item"><span class="idx-item-name">{CEF_NEG_LABELS.get(c,c)}</span><span class="idx-item-val-neg">{v}</span></div>' for c,v in top3_neg])
    st.markdown(f"""
    <div class="idx-card">
        <div class="idx-title">Emotional Index</div>
        <div class="idx-value" style="color:{emo_color};">{emo_index}<span style="font-size:20px;color:#94a3b8;">/100</span></div>
        <div class="idx-sub" style="display:flex;align-items:center;gap:6px;">{emo_icon}{emo_text}</div>
        <hr class="idx-divider">
        <div class="idx-list-label pos">{icon("arrow-up-right", size=11)} Top Emosi Positif</div>{pos_rows}
        <div class="idx-list-label neg" style="margin-top:10px;">{icon("arrow-down-right", size=11)} Top Emosi Negatif</div>{neg_rows}
    </div>""", unsafe_allow_html=True)

with col_brand:
    brand_color = "#15803d" if brand_index >= 4.5 else ("#b45309" if brand_index >= 3.5 else "#b91c1c")
    brand_diff  = round(brand_index - brand_komp_index, 2)
    brand_sign  = "+" if brand_diff >= 0 else ""
    bd_color    = "#15803d" if brand_diff >= 0 else "#b91c1c"
    top_rows = "".join([f'<div class="idx-item"><span class="idx-item-name">{IMG_LABELS.get(c,c)}</span><span class="idx-item-val-pos">{v}</span></div>' for c,v in img_top3])
    bot_rows = "".join([f'<div class="idx-item"><span class="idx-item-name">{IMG_LABELS.get(c,c)}</span><span class="idx-item-val-neg">{v}</span></div>' for c,v in img_bot3])
    st.markdown(f"""
    <div class="idx-card">
        <div class="idx-title">Brand Image Index</div>
        <div class="idx-value" style="color:{brand_color};">{brand_index}<span style="font-size:20px;color:#94a3b8;">/6</span></div>
        <div class="idx-sub">vs Kompetitor <span style="color:{bd_color};font-weight:700;">{brand_sign}{brand_diff}</span></div>
        <hr class="idx-divider">
        <div class="idx-list-label pos">{icon("arrow-up-right", size=11)} Atribut Terkuat</div>{top_rows}
        <div class="idx-list-label neg" style="margin-top:10px;">{icon("arrow-down-right", size=11)} Perlu Ditingkatkan</div>{bot_rows}
    </div>""", unsafe_allow_html=True)

with col_right:
    mpi_items = [("Bank Utama Dana", mpi_dana), ("Bank Utama Transaksi", mpi_trx), ("Bank Aktif Digunakan", mpi_aktif)]
    st.markdown("""<div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:16px 18px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#64748b;margin-bottom:4px;">Market Preference Breakdown</div>
        <div style="font-size:10.5px;color:#94a3b8;margin-bottom:12px;">% nasabah menjadikan XYZ sebagai bank utama</div>
    </div>""", unsafe_allow_html=True)
    for lbl, val in mpi_items:
        komp_val = round(100 - val, 1)
        st.markdown(f"""
        <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;margin-top:6px;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
            <div style="display:flex;justify-content:space-between;font-size:11.5px;margin-bottom:7px;">
                <span style="color:#374151;font-weight:500;">{lbl}</span>
                <span style="color:#1e40af;font-weight:700;">XYZ {val}%</span>
            </div>
            <div style="height:8px;background:#f1f5f9;border-radius:99px;overflow:hidden;">
                <div style="height:100%;width:{val}%;border-radius:99px;background:linear-gradient(90deg,#1e40af,#3b82f6);"></div>
            </div>
            <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Kompetitor &amp; lainnya: {komp_val}%</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BARIS 4 — TOUCHPOINT SNAPSHOT ────────────────────────────────────────────
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("target", size=14)}Touchpoint Snapshot</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

tp_cols = st.columns(len(tp_data))
for col_tp, tp in zip(tp_cols, tp_data):
    v    = tp["xyz"]
    vk   = tp["komp"]
    clr  = pct_color(v)
    lbl  = pct_label(v)
    diff = round(v - vk, 1)
    sign = "+" if diff >= 0 else ""
    diff_clr = "#15803d" if diff >= 0 else "#b91c1c"
    col_tp.markdown(f"""
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:14px 10px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
        <div style="font-size:9.5px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">{tp["label"]}</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:21px;color:{clr};">{v}%</div>
        <div style="font-size:9.5px;font-weight:600;color:{clr};margin-top:2px;">{lbl}</div>
        <div style="font-size:10px;color:{diff_clr};font-weight:700;margin-top:4px;">vs Komp {sign}{diff}%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BARIS 5 — ACTION REQUIRED + TOP/BOTTOM ────────────────────────────────────
st.markdown(f"""<div class="section-label">
    <span class="section-label-text">{icon("alert-triangle", size=14)}Action Required</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_action, col_table = st.columns([2, 3])

with col_action:
    action_items = []
    if nps_score < 20:
        action_items.append(("dot-red", f"NPS kritis: {nps_score}", f"{detr_pct}% responden adalah Detractor"))
    elif nps_score < 50:
        action_items.append(("dot-yellow", f"NPS di bawah target 50 (saat ini {nps_score})", "Push konversi Passive ke Promoter lewat program loyalty"))
    nps_gap_a = round(nps_score - nps_komp_score, 1)
    if nps_gap_a < 0:
        action_items.append(("dot-red", f"NPS kalah dari kompetitor (gap {nps_gap_a})", "Review faktor pembeda layanan"))
    for tp in tp_sorted_asc[:2]:
        if tp["xyz"] < 80:
            dot = "dot-red" if tp["xyz"] < 65 else "dot-yellow"
            diff_tp = round(tp["xyz"] - tp["komp"], 1)
            sign_tp = "+" if diff_tp >= 0 else ""
            action_items.append((dot, f"{tp['label']}: {tp['xyz']}% ({pct_label(tp['xyz'])})",
                                  f"vs Kompetitor {sign_tp}{diff_tp}% -- review SOP dan staffing"))
    if img_bot3:
        low_col = img_bot3[0][0]
        low_lbl = IMG_LABELS.get(low_col, low_col)
        low_val = img_bot3[0][1]
        action_items.append(("dot-blue", f"Brand '{low_lbl}' paling lemah ({low_val}/6)",
                              "Pertimbangkan campaign peningkatan persepsi"))
    if top3_neg and top3_neg[0][1] > avg_pos * 0.5:
        neg_lbl = CEF_NEG_LABELS.get(top3_neg[0][0], top3_neg[0][0])
        action_items.append(("dot-yellow", f"Emosi '{neg_lbl}' cukup tinggi ({top3_neg[0][1]})",
                              "Review alur antrian dan waktu tunggu"))
    if len(cabang_nps) > 0:
        worst = cabang_nps.nsmallest(1,"promoter_pct").iloc[0]
        action_items.append(("dot-red", f"Cabang '{worst['nama_cabang']}' NPS terendah ({worst['promoter_pct']}% promoter)",
                              f"Provinsi: {worst['provinsi']} -- {int(worst['responden'])} responden"))
    if not action_items:
        action_items.append(("dot-green","Semua metrik dalam kondisi baik","Pertahankan performa saat ini"))

    action_html = "".join([f"""<div class="action-item">
        <div class="action-dot {dc}"></div>
        <div><div class="action-title">{title}</div><div class="action-meta">{meta}</div></div>
    </div>""" for dc, title, meta in action_items[:6]])
    st.markdown(f'<div class="action-card">{action_html}</div>', unsafe_allow_html=True)

with col_table:
    if small_sample_excluded > 0:
        st.caption(f"{small_sample_excluded} cabang dengan responden di bawah {MIN_RESPONDEN_RANKING} dikecualikan dari ranking agar tidak menyesatkan.")

    tab_top, tab_bot = st.tabs(["Top 5 Cabang (Promoter %)", "Bottom 5 Cabang"])
    with tab_top:
        if len(top5) > 0:
            top5_disp = top5.copy()
            top5_disp.index = range(1, len(top5_disp)+1)
            st.dataframe(top5_disp, use_container_width=True)
            best = top5.iloc[0]
            st.markdown(f'<div class="insight-box">{icon("lightbulb", size=15)}<span>Cabang <b>{best["Cabang"]}</b> memimpin dengan {best["Promoter %"]}% promoter di {best["Provinsi"]} (n={int(best["Resp"])}). Jadikan best practice untuk cabang lain.</span></div>', unsafe_allow_html=True)
        else:
            st.info(f"Tidak ada cabang dengan minimal {MIN_RESPONDEN_RANKING} responden pada filter ini.")
    with tab_bot:
        if len(bottom5) > 0:
            bottom5_disp = bottom5.copy()
            bottom5_disp.index = range(1, len(bottom5_disp)+1)
            st.dataframe(bottom5_disp, use_container_width=True)
            worst_b = bottom5.iloc[0]
            st.markdown(f'<div class="insight-box">{icon("alert-triangle", size=15)}<span>Cabang <b>{worst_b["Cabang"]}</b> perlu perhatian segera -- hanya {worst_b["Promoter %"]}% promoter (n={int(worst_b["Resp"])}). Lakukan root cause analysis di cabang ini.</span></div>', unsafe_allow_html=True)
        else:
            st.info(f"Tidak ada cabang dengan minimal {MIN_RESPONDEN_RANKING} responden pada filter ini.")