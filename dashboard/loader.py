import pandas as pd
import numpy as np
import streamlit as st
import os

@st.cache_data(show_spinner=False)
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "df_new.xlsx"))

    def parse_nps(v):
        if pd.isna(v) or str(v).strip() == '': return np.nan
        try: return int(str(v).strip().split()[0])
        except: return np.nan

    df['nps_num']          = df['nps_xyz'].apply(parse_nps)
    df['nps_komp_num']     = df['nps_kompetitor'].apply(parse_nps)
    df['nps_category']     = df['nps_num'].apply(
        lambda v: 'Promoter' if v >= 9 else ('Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)
    df['nps_komp_category'] = df['nps_komp_num'].apply(
        lambda v: 'Promoter' if v >= 9 else ('Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    # ── Kolom skala 1-6: validasi rentang sebelum dipakai ──
    # Nilai mentah > 6 atau <= 0 adalah error input (typo entry survey), bukan data
    # valid. Daripada cap di angka teratas (yang menyamarkan data salah dan tetap
    # bisa lolos ke rata-rata), nilai tersebut di-null-kan supaya tidak ikut
    # menghitung rata-rata dan tidak menghasilkan persentase > 100% di kartu manapun.
    SCALE_1_6_COLS = [
        'csi_xyz','cli_xyz','csi_kompetitor','cli_kompetitor',
        'overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
        'overall_banking_hall_xyz','overall_sekuriti_xyz',
        'overall_operasional_xyz','overall_parkir_xyz','overall_toilet_xyz',
        'overall_ca_xyz',
        'overall_teller_komp','overall_cs_komp','overall_atm_komp',
        'overall_banking_hall_komp','overall_sekuriti_komp',
        'overall_operasional_komp','overall_parkir_komp','overall_toilet_komp',
        'smart_table_xyz',
    ]

    num_cols = SCALE_1_6_COLS + [
        'waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi',
        'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi',
        'waktu_ideal_tambah_teller','waktu_ideal_tambah_cs',
        'cef_bahagia_xyz','cef_percaya_xyz','cef_dihargai_xyz','cef_diperhatikan_xyz',
        'cef_aman_xyz','cef_fokus_xyz','cef_memanjakan_xyz','cef_tertarik_xyz','cef_semangat_xyz',
        'cef_tidak_puas_xyz','cef_frustasi_xyz','cef_kecewa_xyz',
        'cef_tertekan_xyz','cef_tidak_bahagia_xyz','cef_diabaikan_xyz','cef_tergesa_xyz',
        'img_terkenal_xyz','img_rasa_aman_xyz','img_dihargai_xyz','img_reputasi_xyz',
        'img_produk_lengkap_xyz','img_investasi_xyz','img_kemudahan_transaksi_xyz',
        'img_teknologi_xyz','img_reward_xyz','img_echannel_xyz',
        'img_terkenal_komp','img_rasa_aman_komp','img_dihargai_komp','img_reputasi_komp',
        'img_produk_lengkap_komp','img_investasi_komp','img_kemudahan_transaksi_komp',
        'img_teknologi_komp','img_reward_komp','img_echannel_komp',
        'imp_terkenal','imp_rasa_aman','imp_dihargai','imp_reputasi',
        'imp_produk_lengkap','imp_investasi','imp_kemudahan_transaksi',
        'imp_teknologi','imp_reward','imp_echannel',
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Validasi rentang skala 1-6: nilai di luar rentang dianggap data invalid
    for c in SCALE_1_6_COLS:
        if c in df.columns:
            df.loc[(df[c] > 6) | (df[c] <= 0), c] = np.nan

    pct_src = [
        'csi_xyz','cli_xyz','csi_kompetitor','cli_kompetitor',
        'overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
        'overall_banking_hall_xyz','overall_sekuriti_xyz',
        'overall_operasional_xyz','overall_parkir_xyz','overall_toilet_xyz',
        'overall_ca_xyz',
        'overall_teller_komp','overall_cs_komp','overall_atm_komp',
        'overall_banking_hall_komp','overall_sekuriti_komp',
        'overall_operasional_komp','overall_parkir_komp','overall_toilet_komp',
        'smart_table_xyz',
    ]
    for c in pct_src:
        if c in df.columns:
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    # ── CES (Customer Effort Score) ──
    # Proxy dari overall_operasional_xyz: skor kemudahan proses/layanan cabang
    # (skala 1-6). Konsisten dengan pendekatan di versi dashboard sebelumnya.
    if 'overall_operasional_xyz' in df.columns:
        df['ces_xyz']     = df['overall_operasional_xyz']
        df['ces_xyz_pct'] = df['overall_operasional_xyz_pct']

    # Tp attrs pct
    for prefix in ['tp_teller_','tp_cs_','tp_atm_','tp_bh_','tp_satpam_','tp_ca_']:
        cols = [c for c in df.columns if c.startswith(prefix) and c.endswith('_xyz')]
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors='coerce')
            df.loc[(df[c] > 6) | (df[c] <= 0), c] = np.nan
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    return df