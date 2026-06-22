import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loader import load_data
from style import SIDEBAR_CSS, PLOT

st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
df_raw = load_data()

DETAIL_GROUPS = {
    "Banking Hall": ['tp_bh_jumlah_cabang_xyz','tp_bh_weekend_banking_xyz','tp_bh_penampilan_gedung_xyz',
        'tp_bh_area_parkir_xyz','tp_bh_kebersihan_parkir_xyz','tp_bh_kebersihan_masuk_xyz',
        'tp_bh_kebersihan_hall_xyz','tp_bh_tempat_duduk_xyz','tp_bh_ac_sejuk_xyz',
        'tp_bh_ruang_tunggu_nyaman_xyz','tp_bh_wifi_xyz','tp_bh_tv_xyz','tp_bh_wangi_xyz',
        'tp_bh_bersih_xyz','tp_bh_signage_pelayanan_xyz','tp_bh_kerapian_xyz','tp_bh_tata_letak_xyz',
        'tp_bh_ada_toilet_xyz','tp_bh_toilet_bersih_xyz','tp_bh_toilet_harum_xyz'],
    "Security": ['tp_satpam_penampilan_rapi_xyz','tp_satpam_seragam_lengkap_xyz','tp_satpam_sambut_ramah_xyz',
        'tp_satpam_sopan_xyz','tp_satpam_ucap_salam_xyz','tp_satpam_tawar_bantuan_xyz',
        'tp_satpam_arahkan_nasabah_xyz','tp_satpam_beri_nomor_antrian_xyz','tp_satpam_atur_antrian_xyz',
        'tp_satpam_jumlah_memadai_xyz','tp_satpam_dalam_siaga_xyz'],
    "Teller": ['tp_teller_antrian_cepat_xyz','tp_teller_sistem_antrian_xyz','tp_teller_layanan_cepat_xyz',
        'tp_teller_jumlah_mencukupi_xyz','tp_teller_penampilan_rapi_xyz','tp_teller_akurasi_transaksi_xyz',
        'tp_teller_sistem_komputer_xyz','tp_teller_pengetahuan_xyz','tp_teller_keramahan_xyz',
        'tp_teller_ucap_salam_xyz','tp_teller_keinginan_bantu_xyz','tp_teller_personal_approach_xyz'],
    "Customer Service": ['tp_cs_keramahan_xyz','tp_cs_jumlah_mencukupi_xyz','tp_cs_pengetahuan_produk_xyz',
        'tp_cs_ketepatan_solusi_xyz','tp_cs_kecepatan_layanan_xyz','tp_cs_ketelitian_xyz',
        'tp_cs_antrian_cepat_xyz','tp_cs_pemahaman_nasabah_xyz','tp_cs_info_lengkap_akurat_xyz',
        'tp_cs_penampilan_rapi_xyz','tp_cs_keinginan_bantu_xyz','tp_cs_personal_approach_xyz','tp_cs_ucap_salam_xyz'],
    "Customer Assistant": ['tp_ca_keramahan_xyz','tp_ca_standby_xyz','tp_ca_pengetahuan_produk_xyz',
        'tp_ca_kecepatan_layanan_xyz','tp_ca_ketelitian_xyz','tp_ca_tangani_masalah_xyz',
        'tp_ca_pemahaman_nasabah_xyz','tp_ca_info_lengkap_akurat_xyz','tp_ca_penampilan_rapi_xyz',
        'tp_ca_keinginan_bantu_xyz','tp_ca_ucap_salam_xyz','tp_ca_personal_approach_xyz'],
    "ATM": ['tp_atm_kemudahan_akses_xyz','tp_atm_ketersediaan_jenis_xyz','tp_atm_kelengkapan_fitur_xyz',
        'tp_atm_antrian_xyz','tp_atm_keamanan_xyz','tp_atm_kehandalan_xyz','tp_atm_lokasi_aman_xyz',
        'tp_atm_kenyamanan_xyz','tp_atm_pilihan_pecahan_xyz','tp_atm_stok_uang_xyz'],
}

PROV_COORDS = {
    "dki jakarta":(-6.2088,106.8456),"jakarta":(-6.2088,106.8456),
    "jawa barat":(-6.9175,107.6191),"jawa tengah":(-6.9667,110.4167),
    "jawa timur":(-7.2575,112.7521),"banten":(-6.1200,106.1500),
    "yogyakarta":(-7.7956,110.3695),"di yogyakarta":(-7.7956,110.3695),
    "bali":(-8.4095,115.1889),"sumatera utara":(3.5952,98.6722),
    "sumatera barat":(-0.9471,100.4172),"sumatera selatan":(-2.9761,104.7754),
    "riau":(0.5071,101.4478),"kepulauan riau":(0.9167,104.4500),
    "jambi":(-1.6101,103.6131),"bengkulu":(-3.8004,102.2655),
    "lampung":(-5.4500,105.2667),"kalimantan barat":(-0.0263,109.3425),
    "kalimantan tengah":(-2.2096,113.9213),"kalimantan selatan":(-3.3194,114.5908),
    "kalimantan timur":(-0.5022,117.1536),"kalimantan utara":(3.0731,117.1000),
    "sulawesi utara":(1.4748,124.8421),"sulawesi tengah":(-0.8917,119.8707),
    "sulawesi selatan":(-5.1477,119.4327),"sulawesi tenggara":(-3.9778,122.5150),
    "gorontalo":(0.5435,123.0568),"sulawesi barat":(-2.8441,119.2321),
    "maluku":(-3.6954,128.1814),"maluku utara":(0.7833,127.3667),
    "papua":(-2.5337,140.7181),"papua barat":(-0.8615,134.0620),
    "nusa tenggara timur":(-10.1772,123.6070),"nusa tenggara barat":(-8.5833,116.1167),
    "aceh":(5.5483,95.3238),
    "kepulauan bangka belitung":(-2.7411,106.4406),"bangka belitung":(-2.7411,106.4406),
}

# Mapping eksplisit nama provinsi (format survei, lowercase) -> NAME_1 pada
# indonesia_provinces.json (GADM). Eksplisit dictionary -- bukan string-replace
# otomatis -- supaya provinsi yang gagal cocok tidak diam-diam hilang dari peta.
PROV_TO_GADM = {
    "dki jakarta":"JakartaRaya","jakarta":"JakartaRaya",
    "jawa barat":"JawaBarat","jawa tengah":"JawaTengah","jawa timur":"JawaTimur",
    "banten":"Banten","yogyakarta":"Yogyakarta","di yogyakarta":"Yogyakarta",
    "bali":"Bali","sumatera utara":"SumateraUtara","sumatera barat":"SumateraBarat",
    "sumatera selatan":"SumateraSelatan","riau":"Riau","kepulauan riau":"KepulauanRiau",
    "jambi":"Jambi","bengkulu":"Bengkulu","lampung":"Lampung",
    "kalimantan barat":"KalimantanBarat","kalimantan tengah":"KalimantanTengah",
    "kalimantan selatan":"KalimantanSelatan","kalimantan timur":"KalimantanTimur",
    "kalimantan utara":"KalimantanUtara","sulawesi utara":"SulawesiUtara",
    "sulawesi tengah":"SulawesiTengah","sulawesi selatan":"SulawesiSelatan",
    "sulawesi tenggara":"SulawesiTenggara","gorontalo":"Gorontalo",
    "sulawesi barat":"SulawesiBarat","maluku":"Maluku","maluku utara":"MalukuUtara",
    "papua":"Papua","papua barat":"PapuaBarat",
    "nusa tenggara timur":"NusaTenggaraTimur","nusa tenggara barat":"NusaTenggaraBarat",
    "aceh":"Aceh","kepulauan bangka belitung":"BangkaBelitung","bangka belitung":"BangkaBelitung",
}

@st.cache_data(show_spinner=False)
def load_geojson():
    geo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "indonesia_provinces.json")
    geo_path = os.path.normpath(geo_path)
    with open(geo_path, encoding="utf-8") as f:
        return json.load(f)

def get_coord(prov_name):
    if pd.isna(prov_name): return None
    key = str(prov_name).strip().lower()
    for pre in ["provinsi ","prov. ","prov "]:
        if key.startswith(pre): key = key[len(pre):]
    return PROV_COORDS.get(key)

def get_gadm_name(prov_name):
    if pd.isna(prov_name): return None
    key = str(prov_name).strip().lower()
    for pre in ["provinsi ","prov. ","prov "]:
        if key.startswith(pre): key = key[len(pre):]
    return PROV_TO_GADM.get(key)

def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def tier_color(metric, val):
    if val is None or (isinstance(val, float) and np.isnan(val)): return "#9ca3af"
    if metric == "NPS": return "#15803d" if val >= 50 else ("#b45309" if val >= 20 else "#b91c1c")
    return "#15803d" if val >= 80 else ("#b45309" if val >= 65 else "#b91c1c")

def pct_color(v): return "#15803d" if v >= 80 else ("#b45309" if v >= 65 else "#b91c1c")
def pct_label(v): return "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")

def pretty_label(col):
    name = col
    for pre in ['tp_bh_','tp_satpam_','tp_teller_','tp_cs_','tp_ca_','tp_atm_']:
        if name.startswith(pre): name = name[len(pre):]; break
    return name.replace('_xyz','').replace('_',' ').title()

def section_label(text):
    return f"""<div class="section-label">
        <span class="section-label-text">{text}</span>
        <div class="section-label-line"></div>
    </div>"""

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
        active = "active" if name == "Branch Intelligence" else ""
        st.markdown(f"<a href='{path}' target='_self' class='nav-pill {active}'><span>{icons[name]}</span><span>{name}</span></a>",
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

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:#334155;padding:0 4px;'>v4.0 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov:   df = df[df["provinsi"].isin(sel_prov)]
if sel_kota:   df = df[df["kab_kota"].isin(sel_kota)]
if sel_branch: df = df[df["nama_cabang"].isin(sel_branch)]
n = len(df)

METRIC_COL = {"CSI":"csi_pct","NPS":"nps_score","CLI":"cli_pct"}

def branch_nps_score(s):
    s2 = s.dropna()
    if len(s2) == 0: return np.nan
    return round((s2 >= 9).mean()*100 - (s2 < 7).mean()*100, 1)

if n > 0:
    branch_stats = df.groupby(["nama_cabang","provinsi","kab_kota"]).agg(
        responden=("serial_id","count"),
        csi_pct=("csi_xyz_pct","mean"),
        cli_pct=("cli_xyz_pct","mean"),
        wait_teller=("waktu_tunggu_teller_aktual","mean"),
        tol_teller=("waktu_tunggu_teller_toleransi","mean"),
        wait_cs=("waktu_tunggu_cs_aktual","mean"),
        tol_cs=("waktu_tunggu_cs_toleransi","mean"),
        add_teller=("waktu_ideal_tambah_teller","mean"),
        add_cs=("waktu_ideal_tambah_cs","mean"),
    ).reset_index()
    nps_branch = df.groupby("nama_cabang")["nps_num"].apply(branch_nps_score).rename("nps_score").reset_index()
    branch_stats = branch_stats.merge(nps_branch, on="nama_cabang", how="left")
    branch_stats["csi_pct"] = branch_stats["csi_pct"].round(1)
    branch_stats["cli_pct"] = branch_stats["cli_pct"].round(1)
    branch_stats["gap_teller"] = (branch_stats["wait_teller"] - branch_stats["tol_teller"]).round(1)
    branch_stats["gap_cs"]     = (branch_stats["wait_cs"]     - branch_stats["tol_cs"]).round(1)
else:
    branch_stats = pd.DataFrame(columns=["nama_cabang","provinsi","kab_kota","responden","csi_pct","cli_pct",
                                          "wait_teller","tol_teller","wait_cs","tol_cs","add_teller","add_cs",
                                          "nps_score","gap_teller","gap_cs"])

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">▣ Bank XYZ · Customer Experience Intelligence</div>
    <h2>Branch Intelligence</h2>
    <p>{n:,} responden &nbsp;·&nbsp; {df['nama_cabang'].nunique()} cabang aktif &nbsp;·&nbsp; {df['provinsi'].nunique()} provinsi</p>
</div>""", unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────────────────────────────
st.markdown(section_label("Ringkasan Cabang"), unsafe_allow_html=True)

avg_nps    = round(safe_mean(branch_stats["nps_score"]), 1) if len(branch_stats) > 0 else 0.0
avg_csi    = round(safe_mean(branch_stats["csi_pct"]),   1) if len(branch_stats) > 0 else 0.0
n_critical = int(((branch_stats["csi_pct"] < 65) | (branch_stats["nps_score"] < 20)).sum()) if len(branch_stats) > 0 else 0

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="exec-card blue">
        <span class="exec-icon">▣</span>
        <div class="exec-label">Total Cabang Aktif</div>
        <div class="exec-value" style="color:#1e40af;">{df['nama_cabang'].nunique()}</div>
        <div class="exec-sub">Tersebar di {df['provinsi'].nunique()} provinsi</div>
    </div>""", unsafe_allow_html=True)
with c2:
    bc = "badge-green" if avg_nps >= 50 else ("badge-yellow" if avg_nps >= 20 else "badge-red")
    lbl = "Excellent" if avg_nps >= 50 else ("Good" if avg_nps >= 20 else "Needs Attention")
    st.markdown(f"""<div class="exec-card cyan">
        <span class="exec-icon">📊</span>
        <div class="exec-label">Rata-rata NPS Cabang</div>
        <div class="exec-value" style="color:#0e7490;">{avg_nps}</div>
        <div class="exec-sub">Rata-rata seluruh cabang aktif</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)
with c3:
    bc3 = "badge-green" if avg_csi >= 80 else ("badge-yellow" if avg_csi >= 65 else "badge-red")
    lbl3 = "Excellent" if avg_csi >= 80 else ("Good" if avg_csi >= 65 else "Needs Attention")
    st.markdown(f"""<div class="exec-card teal">
        <span class="exec-icon">⭐</span>
        <div class="exec-label">Rata-rata CSI Cabang</div>
        <div class="exec-value" style="color:#0f5e5a;">{avg_csi}<span style="font-size:16px;color:#94a3b8;">%</span></div>
        <div class="exec-sub">Dari skala penuh</div>
        <span class="exec-badge {bc3}">{lbl3}</span>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="exec-card red">
        <span class="exec-icon">⚠</span>
        <div class="exec-label">Cabang Perlu Perhatian</div>
        <div class="exec-value" style="color:#b91c1c;">{n_critical}</div>
        <div class="exec-sub">CSI &lt; 65% atau NPS &lt; 20</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 1. GEOGRAPHIC MAP ─────────────────────────────────────────────────────────
st.markdown(section_label("Geographic Performance Map"), unsafe_allow_html=True)

with st.container(border=True):
    top_row = st.columns([1,3])
    with top_row[0]:
        map_metric = st.selectbox("Metric", ["CSI","NPS","CLI"], key="map_metric")

    if len(branch_stats) > 0:
        metric_col_map = METRIC_COL[map_metric]
        prov_geo = branch_stats.groupby("provinsi").agg(
            responden=("responden","sum"), value=(metric_col_map,"mean")).reset_index()
        prov_geo["value"]     = prov_geo["value"].round(1)
        prov_geo["coord"]     = prov_geo["provinsi"].apply(get_coord)
        prov_geo["gadm_name"] = prov_geo["provinsi"].apply(get_gadm_name)
        prov_geo_plot = prov_geo[prov_geo["coord"].notna() & prov_geo["gadm_name"].notna()].copy()
        prov_geo_plot["lat"] = prov_geo_plot["coord"].apply(lambda c: c[0])
        prov_geo_plot["lon"] = prov_geo_plot["coord"].apply(lambda c: c[1])

        # Status & kritis konsisten dengan threshold tier_color (NPS beda skala dari CSI/CLI)
        if map_metric == "NPS":
            status_fn  = lambda v: "Baik" if v >= 50 else ("Perlu Perhatian" if v >= 20 else "Kritis")
            critical_fn = lambda v: v < 20
            zmin_map, zmax_map = -100, 100
        else:
            status_fn  = lambda v: "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")
            critical_fn = lambda v: v < 65
            zmin_map, zmax_map = 0, 100
        prov_geo_plot["status"]   = prov_geo_plot["value"].apply(status_fn)
        prov_geo_plot["critical"] = prov_geo_plot["value"].apply(critical_fn)

        unmatched_provs = prov_geo[prov_geo["gadm_name"].isna()]["provinsi"].tolist()

        if len(prov_geo_plot) > 0:
            geo_data = load_geojson()
            suffix_map = "" if map_metric == "NPS" else "%"

            fig_map = go.Figure()

            fig_map.add_trace(go.Choropleth(
                geojson=geo_data,
                locations=prov_geo_plot["gadm_name"],
                z=prov_geo_plot["value"],
                featureidkey="properties.NAME_1",
                colorscale="RdYlGn", zmin=zmin_map, zmax=zmax_map,
                marker_line_color="white", marker_line_width=0.8,
                colorbar=dict(title=dict(text=map_metric, font=dict(size=10, color="#374151")),
                              tickfont=dict(size=9, color="#64748b"), thickness=14, len=0.7),
                customdata=np.stack([prov_geo_plot["provinsi"], prov_geo_plot["value"],
                                     prov_geo_plot["responden"], prov_geo_plot["status"]], axis=-1),
                hovertemplate=("<b>%{customdata[0]}</b><br>" + map_metric +
                                ": %{customdata[1]}" + suffix_map +
                                "<br>%{customdata[2]} responden<br>Status: %{customdata[3]}<extra></extra>"),
            ))

            # Label angka di titik tengah tiap provinsi
            fig_map.add_trace(go.Scattergeo(
                lat=prov_geo_plot["lat"], lon=prov_geo_plot["lon"],
                mode="text",
                text=[f"{v:.0f}{suffix_map}" for v in prov_geo_plot["value"]],
                textfont=dict(size=10, color="#1e293b", family="Plus Jakarta Sans"),
                showlegend=False, hoverinfo="skip",
            ))

            # Tanda peringatan untuk provinsi kritis, sedikit di atas label angka
            crit_rows = prov_geo_plot[prov_geo_plot["critical"]]
            if len(crit_rows) > 0:
                fig_map.add_trace(go.Scattergeo(
                    lat=crit_rows["lat"] + 0.75, lon=crit_rows["lon"],
                    mode="text", text=["⚠️"] * len(crit_rows),
                    textfont=dict(size=15),
                    showlegend=False, hoverinfo="skip",
                ))

            fig_map.update_geos(scope="asia", projection_type="mercator",
                lataxis_range=[-11,7], lonaxis_range=[94,142],
                showland=True, landcolor="#f1f5f9", showocean=True, oceancolor="#dbeafe",
                showcountries=True, countrycolor="#cbd5e1", showframe=False,
                bgcolor="rgba(0,0,0,0)", coastlinecolor="#cbd5e1")
            fig_map.update_layout(**PLOT, height=420, margin=dict(t=10,b=10,l=0,r=0))
            st.plotly_chart(fig_map, use_container_width=True)

            n_crit_map = int(prov_geo_plot["critical"].sum())
            warn_note = f" ⚠️ menandai {n_crit_map} provinsi kritis." if n_crit_map > 0 else " Tidak ada provinsi dalam status kritis."
            st.markdown(f'<div class="insight-box">💡 Peta menampilkan {len(prov_geo_plot)} provinsi, diwarnai berdasarkan {map_metric}. Angka di tengah wilayah adalah nilai {map_metric} rata-rata.{warn_note}</div>', unsafe_allow_html=True)

            if unmatched_provs:
                st.caption(f"Provinsi tidak tergambar di peta (nama tidak dikenali): {', '.join(unmatched_provs)}")

# ── 2. BRANCH RANKING ─────────────────────────────────────────────────────────
st.markdown(section_label("Branch Ranking"), unsafe_allow_html=True)

rank_top = st.columns([1,3])
with rank_top[0]:
    rank_metric = st.selectbox("Ranking berdasarkan", ["CSI","NPS","CLI"], key="rank_metric")
metric_col_rank = METRIC_COL[rank_metric]
suffix_rank = "" if rank_metric == "NPS" else "%"

valid_rank = branch_stats.dropna(subset=[metric_col_rank]) if len(branch_stats) > 0 else branch_stats
col_top, col_bot = st.columns(2)

with col_top:
    with st.container(border=True):
        st.markdown(f'<div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">▲ Top 10 Cabang — {rank_metric}</div>', unsafe_allow_html=True)
        if len(valid_rank) > 0:
            top10 = valid_rank.nlargest(10, metric_col_rank).sort_values(metric_col_rank)
            fig_top = go.Figure(go.Bar(
                x=top10[metric_col_rank], y=top10["nama_cabang"], orientation="h",
                marker_color="#15803d",
                text=[f"{v:.1f}{suffix_rank}" for v in top10[metric_col_rank]],
                textposition="outside", textfont=dict(color="#374151",size=10)))
            fig_top.update_layout(**PLOT,
                xaxis=dict(color="#64748b",gridcolor="#e2e8f0"),
                yaxis=dict(color="#374151",tickfont=dict(size=9)),
                margin=dict(t=10,b=10,l=10,r=50), height=320)
            st.plotly_chart(fig_top, use_container_width=True)

with col_bot:
    with st.container(border=True):
        st.markdown(f'<div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">▼ Bottom 10 Cabang — {rank_metric}</div>', unsafe_allow_html=True)
        if len(valid_rank) > 0:
            bot10 = valid_rank.nsmallest(10, metric_col_rank).sort_values(metric_col_rank, ascending=False)
            fig_bot = go.Figure(go.Bar(
                x=bot10[metric_col_rank], y=bot10["nama_cabang"], orientation="h",
                marker_color="#b91c1c",
                text=[f"{v:.1f}{suffix_rank}" for v in bot10[metric_col_rank]],
                textposition="outside", textfont=dict(color="#374151",size=10)))
            fig_bot.update_layout(**PLOT,
                xaxis=dict(color="#64748b",gridcolor="#e2e8f0"),
                yaxis=dict(color="#374151",tickfont=dict(size=9)),
                margin=dict(t=10,b=10,l=10,r=50), height=320)
            st.plotly_chart(fig_bot, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 3. BRANCH DRIVER ANALYSIS ─────────────────────────────────────────────────
st.markdown(section_label("Branch Driver Analysis"), unsafe_allow_html=True)

DRIVER_TP = [(lbl,c) for lbl,c in [
    ("Teller","overall_teller_xyz_pct"),("CS","overall_cs_xyz_pct"),
    ("ATM","overall_atm_xyz_pct"),("Security","overall_sekuriti_xyz_pct"),
    ("Banking Hall","overall_banking_hall_xyz_pct"),("CA","overall_ca_xyz_pct"),
    ("Operasional","overall_operasional_xyz_pct")] if c in df.columns]

with st.container(border=True):
    if len(branch_stats) > 0:
        branch_list_sorted = branch_stats.sort_values("csi_pct")["nama_cabang"].tolist()
        sel_driver_branch = st.selectbox("Pilih Cabang untuk Dianalisis", branch_list_sorted, key="driver_branch")

        branch_df_sel = df[df["nama_cabang"] == sel_driver_branch]
        network_avg = {lbl: round(safe_mean(df[col]), 1) for lbl,col in DRIVER_TP}
        branch_val  = {lbl: round(safe_mean(branch_df_sel[col]), 1) for lbl,col in DRIVER_TP}

        labels_d = list(branch_val.keys())
        vals_d   = [branch_val[l] for l in labels_d]
        avg_d    = [network_avg[l] for l in labels_d]
        colors_d = [tier_color("CSI", v) for v in vals_d]

        fig_drv = go.Figure()
        fig_drv.add_trace(go.Bar(
            x=labels_d, y=vals_d, name=sel_driver_branch, marker_color=colors_d,
            text=[f"{v}%" for v in vals_d], textposition="outside",
            textfont=dict(color="#374151",size=10)))
        fig_drv.add_trace(go.Scatter(
            x=labels_d, y=avg_d, name="Rata-rata Network", mode="lines+markers",
            line=dict(color="#1e40af",dash="dash",width=1.5),
            marker=dict(color="#1e40af",size=6)))
        fig_drv.update_layout(**PLOT,
            yaxis=dict(range=[0,115], color="#64748b", gridcolor="#e2e8f0", title="%"),
            xaxis=dict(color="#374151"),
            legend=dict(font=dict(size=10,color="#374151"),orientation="h",x=0,y=1.14),
            margin=dict(t=46,b=10,l=10,r=10), height=340)
        st.plotly_chart(fig_drv, use_container_width=True)

        if vals_d:
            weakest_lbl, weakest_val = min(branch_val.items(), key=lambda x: x[1])
            st.markdown(f"""<div class="insight-box">
                💡 Touchpoint paling lemah di <b>{sel_driver_branch}</b> adalah
                <b style="color:#b91c1c;">{weakest_lbl}</b> ({weakest_val}%) —
                akar masalah cabang ini kemungkinan besar berasal dari area tersebut.
                Garis biru putus-putus menunjukkan rata-rata jaringan untuk perbandingan.
            </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 4. SERVICE BOTTLENECK — GAP CHART ─────────────────────────────────────────
st.markdown(section_label("Service Bottleneck — Waiting Time Gap"), unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)
with col_g1:
    with st.container(border=True):
        st.markdown('<div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">⏱ Gap Waktu Tunggu Teller (Aktual − Toleransi)</div>', unsafe_allow_html=True)
        gt = branch_stats.dropna(subset=["gap_teller"]) if len(branch_stats) > 0 else branch_stats
        if len(gt) > 0:
            worst_teller = gt.nlargest(10,"gap_teller").sort_values("gap_teller")
            fig_gt = go.Figure(go.Bar(
                x=worst_teller["gap_teller"], y=worst_teller["nama_cabang"], orientation="h",
                marker_color=["#b91c1c" if v > 0 else "#15803d" for v in worst_teller["gap_teller"]],
                text=[f"{'+' if v>=0 else ''}{v:.1f} mnt" for v in worst_teller["gap_teller"]],
                textposition="outside", textfont=dict(size=9,color="#374151")))
            fig_gt.update_layout(**PLOT, height=320,
                margin=dict(t=10,b=10,l=10,r=60),
                xaxis=dict(title="Gap (menit)", color="#64748b",gridcolor="#e2e8f0"),
                yaxis=dict(tickfont=dict(size=9),color="#374151"))
            st.plotly_chart(fig_gt, use_container_width=True)
            st.markdown('<div class="insight-box">💡 Merah = waktu tunggu melebihi toleransi nasabah. Hijau = masih dalam batas toleransi. Fokus perbaikan pada cabang dengan gap positif terbesar.</div>', unsafe_allow_html=True)

with col_g2:
    with st.container(border=True):
        st.markdown('<div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">⏱ Gap Waktu Tunggu CS (Aktual − Toleransi)</div>', unsafe_allow_html=True)
        gc = branch_stats.dropna(subset=["gap_cs"]) if len(branch_stats) > 0 else branch_stats
        if len(gc) > 0:
            worst_cs = gc.nlargest(10,"gap_cs").sort_values("gap_cs")
            fig_gc = go.Figure(go.Bar(
                x=worst_cs["gap_cs"], y=worst_cs["nama_cabang"], orientation="h",
                marker_color=["#b91c1c" if v > 0 else "#15803d" for v in worst_cs["gap_cs"]],
                text=[f"{'+' if v>=0 else ''}{v:.1f} mnt" for v in worst_cs["gap_cs"]],
                textposition="outside", textfont=dict(size=9,color="#374151")))
            fig_gc.update_layout(**PLOT, height=320,
                margin=dict(t=10,b=10,l=10,r=60),
                xaxis=dict(title="Gap (menit)", color="#64748b",gridcolor="#e2e8f0"),
                yaxis=dict(tickfont=dict(size=9),color="#374151"))
            st.plotly_chart(fig_gc, use_container_width=True)
            st.markdown('<div class="insight-box">💡 Cabang dengan gap CS tinggi perlu evaluasi jumlah staf CS dan sistem antrian. Bandingkan dengan data capacity indicator di bawah.</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">👥 Capacity Indicator — Kebutuhan Tambahan Staf</div>', unsafe_allow_html=True)
    if len(branch_stats) > 0:
        cap = branch_stats.dropna(subset=["add_teller","add_cs"], how="all").copy()
        cap["add_teller_r"] = cap["add_teller"].fillna(0).round(0)
        cap["add_cs_r"]     = cap["add_cs"].fillna(0).round(0)
        cap["total_need"]   = cap["add_teller_r"] + cap["add_cs_r"]
        cap_top = cap[cap["total_need"] > 0].nlargest(8,"total_need")
        if len(cap_top) > 0:
            n_col    = min(4, len(cap_top))
            cap_cols = st.columns(n_col)
            for i, (_, row) in enumerate(cap_top.iterrows()):
                with cap_cols[i % n_col]:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;
                                padding:12px 10px;text-align:center;margin-bottom:8px;">
                        <div style="font-size:11px;font-weight:700;color:#1e40af;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{row['nama_cabang'][:18]}</div>
                        <div style="font-size:17px;font-family:'DM Serif Display',serif;color:#b91c1c;margin-top:4px;">+{int(row['add_teller_r'])} Teller</div>
                        <div style="font-size:13px;color:#b45309;">+{int(row['add_cs_r'])} CS</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#64748b;font-size:12px;'>Tidak ada cabang yang membutuhkan tambahan staf signifikan.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 5. BRANCH PAIN POINT ──────────────────────────────────────────────────────
st.markdown(section_label("Branch Pain Point"), unsafe_allow_html=True)

with st.container(border=True):
    branch_list_all = sorted(df["nama_cabang"].dropna().unique().tolist())
    if branch_list_all:
        pain_branch = st.selectbox("Pilih Cabang", branch_list_all, key="pain_branch")
        bdf = df[df["nama_cabang"] == pain_branch]
        pain_scores = []
        for grp, cols in DETAIL_GROUPS.items():
            for c in cols:
                if c in df.columns:
                    v = safe_mean(bdf[c])
                    if v > 0: pain_scores.append((grp, pretty_label(c), round(v,2)))
        pain_scores_sorted = sorted(pain_scores, key=lambda x: x[2])[:5]

        if pain_scores_sorted:
            rows = "".join([f'<div class="idx-item"><span class="idx-item-name">[{grp}] {lbl}</span><span class="idx-item-val-neg">{val}/6</span></div>'
                            for grp,lbl,val in pain_scores_sorted])
            st.markdown(rows, unsafe_allow_html=True)
            st.markdown(f"""<div class="insight-box">
                💡 Fokuskan perbaikan pada {len(pain_scores_sorted)} atribut dengan skor terendah di atas
                untuk meningkatkan pengalaman nasabah di cabang <b>{pain_branch}</b>.
                Atribut terlemah: <b style="color:#b91c1c;">{pain_scores_sorted[0][1]}</b> ({pain_scores_sorted[0][2]}/6).
            </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 6. REGIONAL COMPARISON ────────────────────────────────────────────────────
st.markdown(section_label("Regional Comparison"), unsafe_allow_html=True)

reg_top = st.columns([1,3])
with reg_top[0]:
    reg_metric = st.selectbox("Metric", ["CSI","NPS","CLI"], key="reg_metric")
metric_col_reg = METRIC_COL[reg_metric]

col_pr, col_kr = st.columns(2)
with col_pr:
    with st.container(border=True):
        if len(branch_stats) > 0:
            prov_rank = branch_stats.groupby("provinsi").agg(
                value=(metric_col_reg,"mean"), responden=("responden","sum")).reset_index()
            prov_rank = prov_rank.dropna(subset=["value"]).sort_values("value",ascending=False)
            if len(prov_rank) > 0:
                fig_pr = go.Figure(go.Bar(
                    x=prov_rank["value"], y=prov_rank["provinsi"], orientation="h",
                    marker_color=[tier_color(reg_metric,v) for v in prov_rank["value"]],
                    text=[f"{v:.1f}" for v in prov_rank["value"]], textposition="outside",
                    textfont=dict(size=9,color="#374151")))
                fig_pr.update_layout(**PLOT, height=max(280,26*len(prov_rank)),
                    margin=dict(t=10,b=10,l=10,r=50),
                    xaxis=dict(color="#64748b",gridcolor="#e2e8f0"),
                    yaxis=dict(tickfont=dict(size=9),color="#374151",autorange="reversed"))
                st.plotly_chart(fig_pr, use_container_width=True)

with col_kr:
    with st.container(border=True):
        if len(branch_stats) > 0:
            kota_rank = branch_stats.groupby("kab_kota").agg(
                value=(metric_col_reg,"mean"), responden=("responden","sum")).reset_index()
            kota_rank = kota_rank.dropna(subset=["value"]).sort_values("value",ascending=False).head(15)
            if len(kota_rank) > 0:
                fig_kr = go.Figure(go.Bar(
                    x=kota_rank["value"], y=kota_rank["kab_kota"], orientation="h",
                    marker_color=[tier_color(reg_metric,v) for v in kota_rank["value"]],
                    text=[f"{v:.1f}" for v in kota_rank["value"]], textposition="outside",
                    textfont=dict(size=9,color="#374151")))
                fig_kr.update_layout(**PLOT, height=max(280,26*len(kota_rank)),
                    margin=dict(t=10,b=10,l=10,r=50),
                    xaxis=dict(color="#64748b",gridcolor="#e2e8f0"),
                    yaxis=dict(tickfont=dict(size=9),color="#374151",autorange="reversed"))
                st.plotly_chart(fig_kr, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 7. BRANCH DATA TABLE ──────────────────────────────────────────────────────
st.markdown(section_label("Appendix — Branch Data Table"), unsafe_allow_html=True)

with st.container(border=True):
    if len(branch_stats) > 0:
        tbl = branch_stats[["nama_cabang","provinsi","kab_kota","responden","nps_score","csi_pct","cli_pct","wait_teller","wait_cs"]].copy()
        tbl.columns = ["Cabang","Provinsi","Kota/Kab","Responden","NPS","CSI (%)","CLI (%)","Wait Teller (mnt)","Wait CS (mnt)"]
        for c in ["NPS","CSI (%)","CLI (%)","Wait Teller (mnt)","Wait CS (mnt)"]:
            tbl[c] = tbl[c].round(1)
        tbl = tbl.sort_values("CSI (%)",ascending=False).reset_index(drop=True)
        tbl.index += 1
        st.dataframe(tbl, use_container_width=True, height=380)