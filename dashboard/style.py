# ── SHARED STYLE ─────────────────────────────────────────────────────────────
# Tema: dark sidebar #0f172a + light content #F8F4F0
# Font: Plus Jakarta Sans (UI & angka) -- modern, profesional, satu keluarga font
# Icon: Lucide-style inline SVG -- tanpa emoji, tanpa dependency JS runtime

SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.main { background-color: #F8F4F0 !important; }
.block-container { padding: 1.5rem 2rem 3rem; background: #F8F4F0; max-width: 1400px; }

[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
[data-testid="stSidebar"] * { color: #f1f5f9 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #f1f5f9 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #f1f5f9 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }
[data-testid="stSidebarNav"] { display: none !important; }

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

.nav-label {
    color: #475569;
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 0 0 5px 0; margin-top: 10px;
}
.nav-pill {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; border-radius: 8px;
    color: #94a3b8; font-size: 13px; font-weight: 500;
    text-decoration: none; margin-bottom: 3px;
    transition: all 0.15s; cursor: pointer;
    border-left: 3px solid transparent;
}
.nav-pill svg { width: 15px; height: 15px; flex-shrink: 0; }
.nav-pill:hover { background: rgba(255,255,255,0.06); color: #f1f5f9; }
.nav-pill.active {
    background: rgba(59,130,246,0.15);
    color: #93c5fd !important; font-weight: 600;
    border-left: 3px solid #3b82f6;
}

/* PAGE HEADER */
.page-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #1e40af 100%);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    position: relative; overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.page-header-tag {
    display: flex; align-items: center; gap: 6px;
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.14em; color: #60a5fa; margin-bottom: 8px;
}
.page-header-tag svg { width: 13px; height: 13px; }
.page-header h2 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f1f5f9; font-size: 27px; font-weight: 700; margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}
.page-header p { color: rgba(241,245,249,0.55); font-size: 12px; margin: 0; }

/* SECTION LABEL */
.section-label {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px; margin-top: 4px;
}
.section-label-text {
    display: flex; align-items: center; gap: 7px;
    color: #1e293b; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; white-space: nowrap;
}
.section-label-text svg { width: 14px; height: 14px; color: #3b82f6; }
.section-label-line {
    flex: 1; height: 1px; background: linear-gradient(90deg, #94a3b8, transparent);
}

/* EXEC CARD (KPI) -- centered layout */
.exec-card {
    background: white;
    border-radius: 14px; padding: 22px 18px 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    position: relative; overflow: hidden;
    transition: transform 0.18s, box-shadow 0.18s;
    height: 100%;
    display: flex; flex-direction: column; align-items: center;
    text-align: center;
}
.exec-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.exec-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; }
.exec-card.blue::before   { background: linear-gradient(90deg, #1e40af, #3b82f6); }
.exec-card.cyan::before   { background: linear-gradient(90deg, #0e7490, #06b6d4); }
.exec-card.teal::before   { background: linear-gradient(90deg, #0f5e5a, #2d9b96); }
.exec-card.indigo::before { background: linear-gradient(90deg, #312e81, #6366f1); }
.exec-card.red::before    { background: linear-gradient(90deg, #991b1b, #ef4444); }

.exec-icon-wrap {
    width: 42px; height: 42px; border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 12px;
}
.exec-icon-wrap svg { width: 21px; height: 21px; }
.exec-icon-wrap.blue   { background: #eff6ff; }
.exec-icon-wrap.blue   svg { color: #1e40af; }
.exec-icon-wrap.cyan   { background: #ecfeff; }
.exec-icon-wrap.cyan   svg { color: #0e7490; }
.exec-icon-wrap.teal   { background: #ecfdf5; }
.exec-icon-wrap.teal   svg { color: #0f5e5a; }
.exec-icon-wrap.indigo { background: #eef2ff; }
.exec-icon-wrap.indigo svg { color: #4338ca; }
.exec-icon-wrap.red    { background: #fef2f2; }
.exec-icon-wrap.red    svg { color: #991b1b; }

.exec-label { color: #64748b; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 8px; }
.exec-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 34px; font-weight: 800; line-height: 1; margin-bottom: 7px;
    color: #1e293b; letter-spacing: -0.02em;
}
.exec-sub   { font-size: 11.5px; color: #94a3b8; font-weight: 500; }
.exec-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; margin-top: 10px; letter-spacing: 0.02em; }
.badge-green  { background: #dcfce7; color: #166534; }
.badge-yellow { background: #fef9c3; color: #854d0e; }
.badge-red    { background: #fee2e2; color: #991b1b; }

/* INSIGHT BOX */
.insight-box {
    display: flex; align-items: flex-start; gap: 10px;
    font-size: 11.5px; color: #1e3a5f; margin-top: 8px; padding: 12px 14px;
    background: #eff6ff; border-radius: 8px; border-left: 3px solid #3b82f6;
    line-height: 1.6;
}
.insight-box svg { width: 15px; height: 15px; flex-shrink: 0; margin-top: 1px; color: #3b82f6; }

/* CHART CARD */
.chart-card {
    background: white;
    border-radius: 14px; padding: 20px 20px 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 0; height: 100%;
}
.chart-card-title {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.09em; color: #64748b; margin-bottom: 4px;
}
.chart-card-sub {
    font-size: 11px; color: #94a3b8; margin-bottom: 14px; line-height: 1.5;
}

/* BUBBLE CONTAINER */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    position: relative; overflow: hidden;
    padding: 6px 4px 2px;
}
div[data-testid="stVerticalBlockBorderWrapper"]::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #1e40af, #3b82f6);
}

/* IDX CARD */
.idx-card {
    background: white; border-radius: 14px; padding: 20px 18px;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.idx-title  { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin-bottom: 4px; }
.idx-value  { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 40px; color: #1e293b; line-height: 1.1; margin-bottom: 4px; letter-spacing: -0.02em; }
.idx-sub    { font-size: 11px; color: #64748b; margin-bottom: 12px; }
.idx-divider { border: none; border-top: 1px solid #f1f5f9; margin: 12px 0; }
.idx-list-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.idx-list-label.pos { color: #15803d; }
.idx-list-label.neg { color: #b91c1c; }
.idx-item { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; border-bottom: 1px solid #f8fafc; font-size: 12px; }
.idx-item:last-child { border-bottom: none; }
.idx-item-name { color: #374151; font-weight: 500; }
.idx-item-val-pos { font-weight: 700; color: #15803d; font-size: 12px; }
.idx-item-val-neg { font-weight: 700; color: #b91c1c; font-size: 12px; }
.idx-item-val-neu { font-weight: 700; color: #1e40af; font-size: 12px; }

/* COMP TABLE */
.comp-table-wrap {
    background: white; border-radius: 14px; padding: 20px 22px;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.comp-table { width: 100%; border-collapse: collapse; }
.comp-table th {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #64748b; padding: 8px 12px;
    border-bottom: 2px solid #e2e8f0; text-align: left;
}
.comp-table th.right { text-align: right; }
.comp-table td { padding: 10px 12px; border-bottom: 1px solid #f8fafc; font-size: 13px; }
.comp-table tr:last-child td { border-bottom: none; }
.comp-table td.metric-name { font-weight: 600; color: #1e293b; }
.comp-table td.val-xyz  { text-align: right; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 19px; color: #1e40af; }
.comp-table td.val-komp { text-align: right; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 19px; color: #6b7280; }
.comp-table td.gap-pos  { text-align: right; color: #15803d; font-weight: 700; }
.comp-table td.gap-neg  { text-align: right; color: #b91c1c; font-weight: 700; }
.comp-table td.val-r    { text-align: right; font-weight: 700; color: #1e40af; }
.comp-table-scroll { max-height: 320px; overflow-y: auto; }

/* RISK PILL */
.risk-pill {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 10.5px; font-weight: 700; color: white;
}

/* ACTION CARD */
.action-card { background: white; border-radius: 14px; padding: 18px 20px; border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.action-item { display: flex; align-items: flex-start; gap: 12px; padding: 9px 10px; border-radius: 8px; margin-bottom: 6px; }
.action-item:hover { background: #f8fafc; }
.action-item:last-child { margin-bottom: 0; }
.action-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 5px; }
.dot-red    { background: #ef4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.15); }
.dot-yellow { background: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,0.15); }
.dot-blue   { background: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.15); }
.dot-green  { background: #22c55e; box-shadow: 0 0 0 3px rgba(34,197,94,0.15); }
.action-title { font-size: 12.5px; font-weight: 600; color: #1e293b; line-height: 1.4; }
.action-meta  { font-size: 10.5px; color: #94a3b8; margin-top: 2px; }

/* RANK TABLE */
.rank-table { width: 100%; border-collapse: collapse; }
.rank-table th {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #64748b; padding: 8px 10px;
    border-bottom: 2px solid #e2e8f0; text-align: left;
}
.rank-table th.right { text-align: right; }
.rank-table td { padding: 10px 10px; border-bottom: 1px solid #f8fafc; font-size: 13px; color: #374151; }
.rank-table tr:last-child td { border-bottom: none; }
.rank-table tr:hover td { background: #f8fafc; }
.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 50%;
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 800;
    background: #f1f5f9; color: #1e40af;
}
.rank-badge.top1 { background: #1e40af; color: #bfdbfe; }
.rank-badge.top2 { background: #1e3a5f; color: #dbeafe; }
.rank-badge.top3 { background: #3b82f6; color: white; }

/* DATAFRAME / TABS */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: white; border-radius: 10px; padding: 5px; gap: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 7px !important; padding: 9px 18px !important;
    font-weight: 600 !important; font-size: 12px !important;
    color: #64748b !important; border: none !important;
    background: transparent !important; transition: all 0.2s !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #1e40af !important; color: #dbeafe !important;
    box-shadow: 0 2px 8px rgba(30,64,175,0.3) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* MISC */
.opp-item {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 14px; border-radius: 10px; margin-bottom: 8px;
    border: 1px solid #e2e8f0; background: white;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.opp-item:hover { background: #f8fafc; }
.opp-rank { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 22px; color: #3b82f6; min-width: 28px; text-align: center; }
.opp-body { flex: 1; }
.opp-area { font-size: 13px; font-weight: 600; color: #1e293b; }
.opp-meta { font-size: 11px; color: #94a3b8; margin-top: 2px; }
.opp-pill { padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
.pill-high { background: #fee2e2; color: #991b1b; }
.pill-med  { background: #fef9c3; color: #854d0e; }
.pill-low  { background: #dcfce7; color: #166534; }

.gap-item { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid #f8fafc; }
.gap-item:last-child { border-bottom: none; }
.gap-label { font-size: 12.5px; color: #374151; font-weight: 500; }
.gap-val-pos { font-size: 12px; font-weight: 700; color: #15803d; min-width: 46px; text-align: right; }
.gap-val-neg { font-size: 12px; font-weight: 700; color: #b91c1c; min-width: 46px; text-align: right; }

.wt-summary { display: flex; gap: 10px; margin-bottom: 14px; }
.wt-box { flex: 1; background: #f8fafc; border-radius: 10px; padding: 10px 14px; border: 1px solid #e2e8f0; }
.wt-box-label { font-size: 9.5px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.wt-box-val { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 21px; line-height: 1; }
.wt-box-unit { font-size: 10px; color: #94a3b8; margin-top: 2px; }
.wt-gap-positive { color: #b91c1c; }
.wt-gap-negative { color: #15803d; }

.reason-card { background: white; border-radius: 14px; padding: 16px 18px; border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 12px; }
.reason-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 10px; }
.reason-pos-title { color: #166534; }
.reason-neg-title { color: #991b1b; }
.reason-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #f8fafc; font-size: 12px; color: #374151; }
.reason-item:last-child { border-bottom: none; }
.reason-count { font-weight: 700; color: #1e40af; }

.card { background: white; border-radius: 14px; padding: 20px 20px 16px; border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.06); position: relative; overflow: hidden; height: 100%; }
.card-accent-blue::before   { content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#1e40af,#3b82f6); }
.card-accent-teal::before   { content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#0f5e5a,#2d9b96); }
.card-accent-red::before    { content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#991b1b,#ef4444); }
.card-accent-cyan::before   { content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#0e7490,#06b6d4); }
</style>
"""

# ── ICON LIBRARY (gaya Lucide, inline SVG) ────────────────────────────────────
# Pengganti emoji. Setiap pemanggilan mengembalikan string SVG siap pakai,
# tanpa dependency JS runtime sehingga selalu konsisten tampil di semua browser.
_ICON_PATHS = {
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "repeat": '<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "map-pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "building-2": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z"/><path d="m9 12 2 2 4-4"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
    "frown": '<circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
    "layout-grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "bar-chart-3": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "user-check": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "filter": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "check-circle": '<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>',
    "x-circle": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "minus-circle": '<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/>',
    "arrow-up-right": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "arrow-down-right": '<path d="m7 7 10 10"/><path d="M17 7v10H7"/>',
}

def icon(name, size=20, color="currentColor", stroke_width=2):
    """Render inline SVG icon (gaya Lucide) sebagai pengganti emoji.
    Contoh: icon("trending-up", size=22)"""
    p = _ICON_PATHS.get(name, _ICON_PATHS["info"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{p}</svg>')


PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Plus Jakarta Sans", color="#374151", size=12),
)

# Palet vivid untuk chart -- lebih jenuh & kontras dibanding versi sebelumnya,
# tetap dalam keluarga warna korporat biru/ungu.
BLUE_COLORS = ["#1d4ed8","#0891b2","#7c3aed","#0d9488","#2563eb","#0ea5e9","#6366f1","#06b6d4"]
ACCENT   = "#2563eb"
ACCENT2  = "#7c3aed"
SUCCESS  = "#16a34a"
WARNING  = "#d97706"
DANGER   = "#dc2626"

# Warna kategori NPS -- lebih jenuh, kontras tinggi di atas putih
NPS_COLORS = {"Promoter": "#16a34a", "Passive": "#d97706", "Detractor": "#dc2626"}