"""
한국 미세먼지 50년 분석 대시보드
황사·매연 테마 밝은 디자인
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="한국 미세먼지 50년 분석",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS: 황사·스모그 밝은 테마 ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --bg:          #f2ead8;
    --bg2:         #ede0c4;
    --surface:     #fdf6e8;
    --surface2:    #f7ecce;
    --border:      #d4b896;
    --border2:     #c4a070;
    --ink:         #1a0f00;
    --ink2:        #3d2800;
    --muted:       #8a6a40;
    --accent:      #b84a00;       /* 짙은 매연 오렌지 */
    --accent2:     #e07b1a;       /* 황사 황금 */
    --accent3:     #5a8a3c;       /* 나쁨·위험 대비 좋음 */
    --red:         #c0180a;
    --orange:      #d45f00;
    --yellow:      #c49200;
    --green:       #3a7a20;
    --smog1:       rgba(180,140,80,0.18);
    --smog2:       rgba(160,120,60,0.10);
    --smog3:       rgba(200,160,90,0.12);
}

/* ── 전체 배경: 황사 안개 레이어 ── */
html, body, [class*="css"], .stApp {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--bg) !important;
    color: var(--ink);
}

.stApp {
    background-image:
        /* 태양 흐릿한 원 */
        radial-gradient(ellipse 320px 220px at 82% 8%, rgba(230,180,60,0.28) 0%, transparent 70%),
        /* 스모그 레이어 왼쪽 */
        radial-gradient(ellipse 60% 35% at 10% 30%, rgba(180,140,70,0.20) 0%, transparent 65%),
        /* 스모그 레이어 오른쪽 아래 */
        radial-gradient(ellipse 50% 40% at 85% 75%, rgba(160,120,60,0.16) 0%, transparent 60%),
        /* 황사 띠 */
        linear-gradient(175deg,
            #ede0c0 0%,
            #f0e5cb 18%,
            #ece0c2 35%,
            #f5ecda 52%,
            #ede3c8 68%,
            #f2e8d2 85%,
            #eee4cc 100%
        ) !important;
    background-attachment: fixed !important;
    background-size: cover !important;
}

/* 스모그 입자 애니메이션 (CSS only) */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        radial-gradient(circle 2px at 15% 25%, rgba(160,120,50,0.35) 0%, transparent 100%),
        radial-gradient(circle 3px at 38% 60%, rgba(180,140,60,0.25) 0%, transparent 100%),
        radial-gradient(circle 1.5px at 62% 18%, rgba(140,100,40,0.30) 0%, transparent 100%),
        radial-gradient(circle 2.5px at 80% 45%, rgba(160,130,55,0.28) 0%, transparent 100%),
        radial-gradient(circle 2px at 55% 80%, rgba(150,115,50,0.22) 0%, transparent 100%),
        radial-gradient(circle 4px at 28% 88%, rgba(170,135,60,0.18) 0%, transparent 100%),
        radial-gradient(circle 1px at 90% 12%, rgba(180,140,60,0.32) 0%, transparent 100%),
        radial-gradient(circle 3px at 5% 70%, rgba(155,118,48,0.20) 0%, transparent 100%);
    animation: smog-drift 18s ease-in-out infinite alternate;
}

@keyframes smog-drift {
    0%   { opacity: 0.6; transform: translateX(0px) translateY(0px); }
    33%  { opacity: 1.0; transform: translateX(6px) translateY(-4px); }
    66%  { opacity: 0.7; transform: translateX(-4px) translateY(3px); }
    100% { opacity: 0.9; transform: translateX(8px) translateY(-6px); }
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fdf0d5 0%, #f5e4ba 100%) !important;
    border-right: 2px solid var(--border2) !important;
    box-shadow: 4px 0 20px rgba(160,100,20,0.12);
}
section[data-testid="stSidebar"] * { color: var(--ink) !important; }
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent) !important;
    font-family: 'Black Han Sans', sans-serif !important;
}

/* ── 히어로 배너 ── */
.hero {
    background: linear-gradient(135deg, #1a0f00 0%, #2d1800 40%, #3d2400 70%, #2a1500 100%);
    border-radius: 20px;
    padding: 2.8rem 3.5rem 2.4rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(100,50,0,0.35), 0 0 0 1px rgba(200,140,50,0.25);
}
/* 태양 광륜 효과 */
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -40px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(230,180,60,0.35) 0%, rgba(200,130,30,0.15) 45%, transparent 70%);
    animation: sun-pulse 4s ease-in-out infinite alternate;
}
/* 스모그 흐름 */
.hero::after {
    content: '';
    position: absolute;
    bottom: -20px; left: -30px;
    width: 120%; height: 80px;
    background: linear-gradient(90deg, rgba(180,130,50,0.18) 0%, rgba(160,110,40,0.10) 50%, rgba(180,130,50,0.14) 100%);
    border-radius: 50%;
    animation: smog-wave 6s ease-in-out infinite alternate;
}
@keyframes sun-pulse {
    from { transform: scale(1);   opacity: 0.8; }
    to   { transform: scale(1.1); opacity: 1.0; }
}
@keyframes smog-wave {
    from { transform: translateX(-20px) scaleX(1.0); }
    to   { transform: translateX(20px)  scaleX(1.05); }
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    color: #e8b850;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    position: relative; z-index: 1;
}
.hero-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 2.8rem;
    color: #fdf0d5;
    line-height: 1.1;
    margin: 0;
    position: relative; z-index: 1;
    text-shadow: 0 2px 20px rgba(0,0,0,0.4);
}
.hero-title .hl { color: #f0a830; }
.hero-sub {
    color: #c8a870;
    font-size: 0.9rem;
    margin-top: 0.6rem;
    position: relative; z-index: 1;
    font-weight: 300;
}
.hero-pill {
    display: inline-block;
    background: rgba(230,160,40,0.2);
    border: 1px solid rgba(230,160,40,0.4);
    color: #f0c060;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 1rem;
    position: relative; z-index: 1;
}

/* ── KPI 카드 ── */
.kpi-card {
    background: linear-gradient(145deg, #fff8ea, #fdf0d2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    box-shadow: 0 4px 20px rgba(160,100,20,0.12), 0 1px 4px rgba(160,100,20,0.08);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(160,100,20,0.20);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 16px 16px 0 0;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 2.4rem;
    line-height: 1.0;
    color: var(--accent);
    letter-spacing: -0.01em;
}
.kpi-unit  { font-size: 0.85rem; color: var(--muted); margin-left: 3px; }
.kpi-good  { color: var(--green);  font-size: 0.82rem; font-weight: 700; }
.kpi-bad   { color: var(--red);    font-size: 0.82rem; font-weight: 700; }

/* ── AQI 배지 ── */
.aqi-good     { background:#d4edda; color:#155724; border:2px solid #82c896; font-weight:700; }
.aqi-moderate { background:#fff3cd; color:#7d5a00; border:2px solid #f0c040; font-weight:700; }
.aqi-bad      { background:#ffd5b0; color:#7a2800; border:2px solid #e07030; font-weight:700; }
.aqi-vbad     { background:#f8d7da; color:#721c24; border:2px solid #e04040; font-weight:700; }
.aqi-badge {
    display: inline-block;
    border-radius: 8px;
    padding: 0.2rem 0.75rem;
    font-family: 'Black Han Sans', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
}

/* ── 섹션 레이블 ── */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border2);
    margin-bottom: 1rem;
}

/* ── WHO 경고 바 ── */
.who-bar {
    background: linear-gradient(135deg, #fff0e0, #ffe8cc);
    border: 1px solid #e09040;
    border-left: 5px solid var(--red);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.85rem;
    color: var(--ink2);
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(192,24,10,0.10);
}
.who-bar strong { color: var(--red); }

/* ── 어노테이션 박스 ── */
.anno-box {
    background: linear-gradient(135deg, #fffbe8, #fff3cc);
    border-left: 4px solid var(--accent2);
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.1rem;
    font-size: 0.83rem;
    color: var(--ink2);
    margin: 0.6rem 0;
    box-shadow: 0 2px 10px rgba(200,130,20,0.10);
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(135deg, #fdf0d5, #f5e4ba) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    padding: 5px !important;
    gap: 4px !important;
    box-shadow: 0 2px 10px rgba(160,100,20,0.10);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.85rem !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--orange)) !important;
    color: #fff !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(180,80,0,0.30) !important;
}

/* ── 버튼 ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--orange)) !important;
    color: #fff !important;
    font-family: 'Black Han Sans', sans-serif !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 12px rgba(180,80,0,0.25) !important;
}

/* ── 슬라이더 ── */
.stSlider [data-baseweb="slider"] { accent-color: var(--accent); }

/* ── 데이터프레임 ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden; }

/* ── 순위 행 ── */
.rank-row {
    display: flex;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--border);
    gap: 0.6rem;
}
.rank-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    width: 20px;
}

hr { border-color: var(--border2) !important; }
</style>
""", unsafe_allow_html=True)


# ── 데이터 생성 ───────────────────────────────────────────────────────────────
@st.cache_data
def build_data():
    np.random.seed(42)
    years = np.arange(1975, 2025)

    pm10_base = np.array([
        130,133,136,140,143,147,150,153,155,158,
        160,163,165,162,158,154,150,146,142,138,
        134,130,126,122,118,114,110,106,102, 98,
         96, 93, 91, 88, 85, 83, 80, 78, 75, 72,
         70, 68, 65, 62, 59, 57, 55, 53, 51, 49,
    ], dtype=float)

    pm25_base = np.array([
        80, 82, 84, 87, 89, 91, 93, 95, 96, 98,
        99,101,102,100, 97, 94, 91, 88, 85, 82,
        79, 76, 73, 70, 67, 64, 61, 58, 55, 52,
        50, 48, 46, 44, 42, 40, 38, 37, 35, 33,
        32, 30, 28, 26, 25, 24, 23, 22, 21, 20,
    ], dtype=float)

    region_offsets = {
        "서울": (0, 0), "인천": (5, 3), "경기": (2, 1.5),
        "부산": (-5, -3), "대구": (-2, -1), "광주": (-8, -5),
        "대전": (-6, -4), "강원": (-15, -10), "제주": (-20, -13),
    }

    rows = []
    for region, (o10, o25) in region_offsets.items():
        r10 = np.random.normal(0, 3, len(years))
        r25 = np.random.normal(0, 1.5, len(years))
        for i, y in enumerate(years):
            rows.append({
                "연도": int(y), "지역": region,
                "PM10":  float(max(10, pm10_base[i] + o10 + r10[i])),
                "PM2.5": float(max(5,  pm25_base[i] + o25 + r25[i])),
            })
    df_annual = pd.DataFrame(rows)

    month_names = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]
    df_monthly  = pd.DataFrame({
        "월": list(range(1,13)), "월이름": month_names,
        "PM10":  [72,75,85,78,65,52,45,42,55,68,78,74],
        "PM2.5": [35,37,42,38,30,22,18,16,24,32,38,36],
    })

    exceed_rows = []
    for y in years:
        r = df_annual[(df_annual["연도"]==int(y)) & (df_annual["지역"]=="서울")]
        b25 = float(r["PM2.5"].values[0]) if len(r) else 30
        b10 = float(r["PM10"].values[0])  if len(r) else 80
        exceed_rows.append({
            "연도": int(y),
            "PM2.5 초과일": int(np.clip(365*(b25/5)*0.25, 0, 365)),
            "PM10 초과일":  int(np.clip(365*(b10/15)*0.20, 0, 365)),
        })
    df_exceed = pd.DataFrame(exceed_rows)
    return df_annual, df_monthly, df_exceed


df_annual, df_monthly, df_exceed = build_data()
ALL_REGIONS = sorted(df_annual["지역"].unique().tolist())

REGION_COLORS = {
    "서울":"#b84a00","인천":"#d4780a","경기":"#c05a00","부산":"#2a7a4a",
    "대구":"#5a8a1a","광주":"#1a6a8a","대전":"#7a3a8a","강원":"#1a5a8a","제주":"#6a8a1a",
}
EVENTS = {
    1988:"서울올림픽", 1995:"수도권 대기 규제 강화", 2002:"한일 월드컵",
    2005:"경유차 배출가스 규제", 2013:"중국발 황사 최악",
    2019:"미세먼지 사회재난 지정", 2020:"코로나19", 2021:"WHO 기준 강화",
}

# Plotly 차트 공통 테마 — 밝은 배경
BASE = dict(
    paper_bgcolor="rgba(253,246,232,0.92)",
    plot_bgcolor="rgba(250,242,224,0.80)",
    font=dict(family="Noto Sans KR, sans-serif", color="#1a0f00", size=11),
    margin=dict(l=10, r=10, t=48, b=10),
    legend=dict(bgcolor="rgba(253,246,232,0.85)", bordercolor="#d4b896", borderwidth=1),
    hovermode="x unified",
)
AXIS = dict(gridcolor="#ddd0b8", showgrid=True, zeroline=False, linecolor="#c4a070", linewidth=1.5)


def apply_axes(fig, dtick_x=None):
    kw = dict(**AXIS)
    if dtick_x: kw["dtick"] = dtick_x
    fig.update_xaxes(**kw)
    fig.update_yaxes(**AXIS)


def aqi_label(v):
    if v <= 15:  return "좋음",     "aqi-good"
    if v <= 35:  return "보통",     "aqi-moderate"
    if v <= 75:  return "나쁨",     "aqi-bad"
    return               "매우나쁨", "aqi-vbad"


# ── 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌫️ 분석 설정")
    st.markdown("---")
    year_range  = st.slider("📅 연도 범위", 1975, 2024, (1975, 2024))
    dust_type   = st.radio("측정 항목", ["PM10 (미세먼지)", "PM2.5 (초미세먼지)"], index=1)
    col_key     = "PM2.5" if "PM2.5" in dust_type else "PM10"
    st.markdown("### 🗺️ 지역 선택")
    sel_regions = st.multiselect("지역", ALL_REGIONS,
                                 default=["서울","인천","부산","강원","제주"])
    st.markdown("### ⚙️ 표시 옵션")
    show_who    = st.toggle("WHO 기준선", value=True)
    show_trend  = st.toggle("추세선",     value=True)
    show_event  = st.toggle("주요 사건 마커", value=True)
    st.markdown("---")
    who_val = 5 if col_key == "PM2.5" else 15
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#fff0e0,#ffe4c0);border:1px solid #e09040;
    border-left:4px solid #c0180a;border-radius:10px;padding:0.9rem 1rem;font-size:0.8rem;">
    <div style="color:#c0180a;font-family:'Black Han Sans',sans-serif;font-size:0.95rem;margin-bottom:4px;">
    🚨 WHO 2021 가이드라인</div>
    <b style="color:#1a0f00;">{col_key}</b>
    <span style="color:#b84a00;font-family:'JetBrains Mono',monospace;font-size:1.15rem;font-weight:700;">
     {who_val} μg/m³</span>
    <span style="color:#8a6a40;"> 연평균</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<div style="font-size:0.65rem;color:#8a6a40;line-height:1.8;">
    📌 <b>데이터 출처</b><br>환경부 에어코리아<br>국립환경과학원<br>공공데이터포털 기반 추정치<br>
    (1975–1990 일부 추정 포함)</div>""", unsafe_allow_html=True)


# ── 필터 ─────────────────────────────────────────────────────────────────────
mask     = (df_annual["연도"] >= year_range[0]) & (df_annual["연도"] <= year_range[1])
df_f     = df_annual[mask].copy()
df_s     = df_f[df_f["지역"] == "서울"]
latest   = int(df_f["연도"].max())
earliest = int(df_f["연도"].min())

lv_arr = df_s[df_s["연도"] == latest][col_key].values
ev_arr = df_s[df_s["연도"] == earliest][col_key].values
lv = float(lv_arr[0]) if len(lv_arr) else 0
ev = float(ev_arr[0]) if len(ev_arr) else 0
pct_chg      = (lv - ev) / ev * 100 if ev > 0 else 0
exceed_today = int(df_exceed[df_exceed["연도"] == latest]["PM2.5 초과일"].values[0]) \
               if latest in df_exceed["연도"].values else 0
aql, aqc = aqi_label(lv)


# ── 히어로 ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">🌫 KOREA AIR QUALITY · 50-YEAR ANALYSIS · 1975 – 2024</div>
  <div class="hero-title">한국 <span class="hl">미세먼지</span> 50년의 기록</div>
  <div class="hero-sub">전국 9개 권역 · {col_key} 농도 장기 추이 분석 · 환경부 데이터 기반</div>
  <div class="hero-pill">📊 공공데이터 기반 추정치 · 참고용</div>
</div>
""", unsafe_allow_html=True)


# ── KPI 카드 ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">☁️ {latest}년 서울 연평균</div>
      <div class="kpi-value">{lv:.1f}<span class="kpi-unit">μg/m³</span></div>
      <div style="margin-top:4px;"><span class="aqi-badge {aqc}">{aql}</span></div>
    </div>""", unsafe_allow_html=True)

with k2:
    cls   = "kpi-good" if pct_chg < 0 else "kpi-bad"
    arrow = "▼ 개선" if pct_chg < 0 else "▲ 악화"
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">📉 50년 변화율</div>
      <div class="kpi-value">{abs(pct_chg):.1f}<span class="kpi-unit">%</span></div>
      <div class="{cls}" style="margin-top:4px;">{arrow}</div>
    </div>""", unsafe_allow_html=True)

with k3:
    who_ratio = lv / who_val
    ratio_cls = "kpi-bad" if who_ratio > 2 else ("kpi-bad" if who_ratio > 1 else "kpi-good")
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">🚨 WHO 기준 대비</div>
      <div class="kpi-value">{who_ratio:.1f}<span class="kpi-unit">배</span></div>
      <div class="{ratio_cls}" style="margin-top:4px;">기준: {who_val} μg/m³</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">📆 WHO 초과일 (서울)</div>
      <div class="kpi-value">{exceed_today}<span class="kpi-unit">일</span></div>
      <div class="kpi-bad" style="margin-top:4px;">PM2.5 연간 기준</div>
    </div>""", unsafe_allow_html=True)

with k5:
    peak_row = df_annual[df_annual["지역"]=="서울"].loc[df_annual[df_annual["지역"]=="서울"][col_key].idxmax()]
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">📈 역대 최고 (서울)</div>
      <div class="kpi-value">{peak_row[col_key]:.1f}<span class="kpi-unit">μg/m³</span></div>
      <div class="kpi-bad" style="margin-top:4px;">{int(peak_row['연도'])}년</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── 탭 ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 연도별 추이", "🗺️ 지역별 비교",
    "🌸 계절·월별 패턴", "⚠️ WHO 기준 초과 분석",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — 연도별 추이
# ══════════════════════════════════════════════════════════════
with tab1:
    c_main, c_side = st.columns([7, 3])

    with c_main:
        st.markdown('<div class="sec-label">연도별 연평균 농도 추이</div>', unsafe_allow_html=True)
        if show_who:
            st.markdown(f"""<div class="who-bar">
            <strong>⚠️ WHO 2021 연평균 권고기준: {col_key} {who_val} μg/m³</strong>
            — 빨간 점선 <b>아래</b>가 WHO 권고 수준입니다.
            </div>""", unsafe_allow_html=True)

        fig = go.Figure()
        disp = sel_regions if sel_regions else ["서울"]

        for region in disp:
            rdf   = df_f[df_f["지역"]==region].sort_values("연도")
            color = REGION_COLORS.get(region, "#b84a00")
            r, g, b_c = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
            solo  = len(disp) == 1
            fig.add_trace(go.Scatter(
                x=rdf["연도"], y=rdf[col_key], name=region,
                line=dict(color=color, width=3 if solo else 2.2),
                fill="tozeroy" if solo else None,
                fillcolor=f"rgba({r},{g},{b_c},0.10)",
                hovertemplate=f"<b>{region}</b>  %{{x}}년: <b>%{{y:.1f}} μg/m³</b><extra></extra>",
            ))
            if show_trend and len(rdf) > 3:
                z  = np.polyfit(rdf["연도"], rdf[col_key], 2)
                p  = np.poly1d(z)
                xf = np.linspace(rdf["연도"].min(), rdf["연도"].max(), 100)
                fig.add_trace(go.Scatter(
                    x=xf, y=p(xf),
                    line=dict(color=color, width=1.5, dash="dot"),
                    showlegend=False, hoverinfo="skip",
                ))

        if show_who:
            fig.add_hline(y=who_val, line_width=2, line_dash="dash", line_color="#c0180a",
                annotation_text=f"WHO {who_val} μg/m³",
                annotation_font_color="#c0180a", annotation_font_size=11,
                annotation_position="top right")

        if show_event:
            for ey, ename in EVENTS.items():
                if year_range[0] <= ey <= year_range[1]:
                    fig.add_vline(x=ey, line_width=1, line_dash="dot", line_color="#c4a070")
                    fig.add_annotation(x=ey, y=1.02, yref="paper",
                        text=ename, showarrow=False,
                        font=dict(size=8, color="#8a5a20"),
                        textangle=-55, xanchor="left")

        fig.update_layout(**BASE, height=460,
            yaxis_title=f"{col_key} 농도 (μg/m³)",
            title=dict(text=f"한국 {col_key} 연평균 농도 장기 추이 ({year_range[0]}–{year_range[1]})",
                       font=dict(family="Black Han Sans", size=15, color="#1a0f00")))
        apply_axes(fig, dtick_x=5)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""<div class="anno-box">
        🏭 <b>1980년대</b>: 급격한 산업화·경공업 절정기 — PM10 150μg/m³ 이상으로 현재의 3~4배<br>
        🚗 <b>2005년</b>: 경유차 배출가스 규제 이후 뚜렷한 감소 시작<br>
        🌪️ <b>2010년대 이후</b>: 중국발 황사·월경성 오염으로 감소 속도 둔화<br>
        😷 <b>2020년 코로나19</b>: 교통량 급감으로 일시적 개선 효과
        </div>""", unsafe_allow_html=True)

    with c_side:
        st.markdown('<div class="sec-label">최신 연도 지역 현황</div>', unsafe_allow_html=True)
        lat_df  = df_annual[df_annual["연도"] == latest].sort_values(col_key)
        max_val = float(lat_df[col_key].max())
        for _, row in lat_df.iterrows():
            val   = float(row[col_key])
            color = REGION_COLORS.get(row["지역"], "#b84a00")
            ratio = val / max_val * 100
            lbl, lcls = aqi_label(val)
            st.markdown(f"""
            <div style="margin-bottom:0.8rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-size:0.85rem;font-weight:500;">{row['지역']}</span>
                <div>
                  <span style="font-family:'JetBrains Mono';font-size:1rem;color:{color};font-weight:700;">{val:.1f}</span>
                  <span style="font-size:0.65rem;color:#8a6a40;"> μg/m³</span>
                  <span class="aqi-badge {lcls}" style="font-size:0.62rem;padding:1px 6px;margin-left:5px;">{lbl}</span>
                </div>
              </div>
              <div style="background:#e0cca8;border-radius:6px;height:7px;overflow:hidden;box-shadow:inset 0 1px 3px rgba(0,0,0,0.1);">
                <div style="background:linear-gradient(90deg,{color},{color}cc);height:100%;width:{ratio:.0f}%;border-radius:6px;transition:width 0.5s;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-label" style="margin-top:1.2rem;">🏆 개선율 TOP 3 (전체 기간)</div>', unsafe_allow_html=True)
        rows_imp = []
        for region in ALL_REGIONS:
            rdf = df_annual[df_annual["지역"]==region]
            v0  = rdf[rdf["연도"]==rdf["연도"].min()][col_key].values
            v1  = rdf[rdf["연도"]==rdf["연도"].max()][col_key].values
            if len(v0) and len(v1):
                rows_imp.append({"지역": region, "개선율": (v0[0]-v1[0])/v0[0]*100})
        top3   = sorted(rows_imp, key=lambda x: x["개선율"], reverse=True)[:3]
        medals = ["🥇","🥈","🥉"]
        for i, r in enumerate(top3):
            st.markdown(f"""
            <div class="rank-row">
              <span class="rank-num">{medals[i]}</span>
              <span style="flex:1;font-size:0.84rem;font-weight:500;">{r['지역']}</span>
              <span style="color:#3a7a20;font-family:'JetBrains Mono';font-size:0.9rem;font-weight:700;">{r['개선율']:.1f}% ↓</span>
            </div>""", unsafe_allow_html=True)

        # 10년 단위 테이블
        st.markdown('<div class="sec-label" style="margin-top:1.2rem;">📋 연대별 서울 평균</div>', unsafe_allow_html=True)
        dec_rows = []
        for ds in range(1975, 2025, 10):
            de  = min(ds+9, 2024)
            sub = df_annual[(df_annual["지역"]=="서울") & (df_annual["연도"]>=ds) & (df_annual["연도"]<=de)]
            if len(sub):
                dec_rows.append({"연대": f"{ds}~{de}", col_key: f"{sub[col_key].mean():.1f}"})
        st.dataframe(pd.DataFrame(dec_rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB 2 — 지역별 비교
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-label">지역별 농도 분포 비교</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        for region in ALL_REGIONS:
            rdf   = df_f[df_f["지역"]==region][col_key]
            color = REGION_COLORS.get(region, "#b84a00")
            r, g, b_c = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
            fig.add_trace(go.Box(
                y=rdf, name=region,
                marker_color=color, line_color=color,
                fillcolor=f"rgba({r},{g},{b_c},0.20)",
                boxmean=True,
                hovertemplate=f"<b>{region}</b><br>%{{y:.1f}} μg/m³<extra></extra>",
            ))
        if show_who:
            fig.add_hline(y=who_val, line_width=2, line_dash="dash", line_color="#c0180a",
                annotation_text=f"WHO {who_val}", annotation_font_color="#c0180a")
        fig.update_layout(**BASE, height=420, showlegend=False,
            title=dict(text=f"지역별 {col_key} 분포 ({year_range[0]}–{year_range[1]})",
                       font=dict(family="Black Han Sans",size=14,color="#1a0f00")),
            yaxis_title=f"{col_key} (μg/m³)")
        apply_axes(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        dec_labels, dec_data = [], {r: [] for r in ALL_REGIONS}
        for ds in range(1975, 2025, 5):
            dec_labels.append(f"{ds}–{str(ds+4)[2:]}")
            for region in ALL_REGIONS:
                sub = df_annual[(df_annual["지역"]==region) & (df_annual["연도"]>=ds) & (df_annual["연도"]<=ds+4)]
                dec_data[region].append(float(sub[col_key].mean()) if len(sub) else 0)

        z_vals = [dec_data[r] for r in ALL_REGIONS]
        fig2   = go.Figure(go.Heatmap(
            z=z_vals, x=dec_labels, y=ALL_REGIONS,
            colorscale=[[0,"#d4edda"],[0.25,"#fff3cd"],[0.6,"#ffd5b0"],[1,"#f8b4b4"]],
            text=[[f"{v:.0f}" for v in row] for row in z_vals],
            texttemplate="%{text}", textfont=dict(size=10, color="#1a0f00"),
            hovertemplate="%{y} %{x}<br>평균 %{z:.1f} μg/m³<extra></extra>",
            colorbar=dict(title=dict(text="μg/m³",side="right"), thickness=12,
                          tickfont=dict(size=9)),
        ))
        fig2.update_layout(**BASE, height=420,
            title=dict(text=f"지역×5년 평균 히트맵 ({col_key} μg/m³)",
                       font=dict(family="Black Han Sans",size=14,color="#1a0f00")))
        apply_axes(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-label" style="margin-top:0.5rem;">연도별 지역 순위</div>', unsafe_allow_html=True)
    sel_yr = st.slider("연도 선택", int(df_annual["연도"].min()), int(df_annual["연도"].max()), latest)
    yr_df  = df_annual[df_annual["연도"]==sel_yr].sort_values(col_key, ascending=True)
    b_colors = [REGION_COLORS.get(r,"#b84a00") for r in yr_df["지역"]]
    fig3 = go.Figure(go.Bar(
        x=yr_df[col_key], y=yr_df["지역"], orientation="h",
        marker_color=b_colors,
        text=[f"{v:.1f} μg/m³" for v in yr_df[col_key]], textposition="outside",
        textfont=dict(family="JetBrains Mono", size=10),
        hovertemplate="%{y}: %{x:.1f} μg/m³<extra></extra>",
    ))
    if show_who:
        fig3.add_vline(x=who_val, line_dash="dash", line_color="#c0180a", line_width=2,
            annotation_text=f"WHO {who_val}", annotation_font_color="#c0180a")
    fig3.update_layout(**BASE, height=340,
        title=dict(text=f"{sel_yr}년 지역별 {col_key} 비교",
                   font=dict(family="Black Han Sans",size=14,color="#1a0f00")),
        xaxis_title=f"{col_key} (μg/m³)", yaxis_title="")
    apply_axes(fig3)
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — 계절·월별 패턴
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-label">월별 평균 농도 패턴 (서울 기준)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([6, 4])

    with c1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        bar_colors = []
        for v in df_monthly["PM10"]:
            _, cls = aqi_label(v)
            bar_colors.append(
                "#3a7a20" if cls=="aqi-good" else
                "#c49200" if cls=="aqi-moderate" else
                "#d45f00" if cls=="aqi-bad" else "#c0180a"
            )
        fig.add_trace(go.Bar(
            x=df_monthly["월이름"], y=df_monthly["PM10"],
            name="PM10", marker_color=bar_colors,
            hovertemplate="%{x}: PM10 %{y} μg/m³<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=df_monthly["월이름"], y=df_monthly["PM2.5"],
            name="PM2.5", line=dict(color="#b84a00", width=3),
            mode="lines+markers", marker=dict(size=8, color="#b84a00",
                line=dict(color="#fff",width=1.5)),
            hovertemplate="%{x}: PM2.5 %{y} μg/m³<extra></extra>",
        ), secondary_y=True)
        if show_who:
            fig.add_hline(y=5, line_dash="dash", line_color="#c0180a", line_width=1.5,
                annotation_text="WHO PM2.5 5μg", annotation_font_color="#c0180a",
                secondary_y=True)
        fig.update_layout(
            **BASE, height=400,
            title=dict(text="월별 PM10 / PM2.5 농도 패턴",
                       font=dict(family="Black Han Sans",size=14,color="#1a0f00")),
            legend=dict(bgcolor="rgba(253,246,232,0.85)", bordercolor="#d4b896"),
        )
        fig.update_xaxes(gridcolor="#ddd0b8", linecolor="#c4a070")
        fig.update_yaxes(title_text="PM10 (μg/m³)", gridcolor="#ddd0b8",
                         linecolor="#c4a070", secondary_y=False)
        fig.update_yaxes(title_text="PM2.5 (μg/m³)", gridcolor="rgba(0,0,0,0)",
                         linecolor="#c4a070", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="sec-label">계절별 요약</div>', unsafe_allow_html=True)
        seasons = {
            "🌸 봄 (3–5월)":   ([2,3,4], "#e07830"),
            "☀️ 여름 (6–8월)": ([5,6,7],  "#3a7a20"),
            "🍂 가을 (9–11월)":([8,9,10], "#c49200"),
            "❄️ 겨울 (12–2월)":([11,0,1], "#1a5a8a"),
        }
        for sname, (midx, scolor) in seasons.items():
            sdf   = df_monthly.iloc[midx]
            sp10  = float(sdf["PM10"].mean())
            sp25  = float(sdf["PM2.5"].mean())
            lbl25, cls25 = aqi_label(sp25)
            r2,g2,b2 = int(scolor[1:3],16),int(scolor[3:5],16),int(scolor[5:7],16)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba({r2},{g2},{b2},0.08),rgba({r2},{g2},{b2},0.04));
            border:1.5px solid rgba({r2},{g2},{b2},0.35);
            border-left:5px solid {scolor};
            border-radius:12px;padding:0.9rem 1.1rem;margin-bottom:0.75rem;
            box-shadow:0 2px 10px rgba({r2},{g2},{b2},0.12);">
              <div style="font-size:0.88rem;font-weight:700;color:#1a0f00;margin-bottom:8px;">{sname}</div>
              <div style="display:flex;gap:1.2rem;align-items:center;">
                <div>
                  <div style="font-size:0.6rem;color:#8a6a40;font-family:'JetBrains Mono';">PM10</div>
                  <div style="font-family:'Black Han Sans';font-size:1.3rem;color:{scolor};">
                    {sp10:.0f}<span style="font-size:0.65rem;color:#8a6a40;"> μg/m³</span></div>
                </div>
                <div>
                  <div style="font-size:0.6rem;color:#8a6a40;font-family:'JetBrains Mono';">PM2.5</div>
                  <div style="font-family:'Black Han Sans';font-size:1.3rem;color:{scolor};">
                    {sp25:.0f}<span style="font-size:0.65rem;color:#8a6a40;"> μg/m³</span></div>
                </div>
                <span class="aqi-badge {cls25}" style="margin-left:auto;">{lbl25}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-label" style="margin-top:0.5rem;">계절별 농도 레이더</div>', unsafe_allow_html=True)
    theta  = ["봄","여름","가을","겨울","봄"]
    s_pm10 = [df_monthly.iloc[[2,3,4]]["PM10"].mean(), df_monthly.iloc[[5,6,7]]["PM10"].mean(),
              df_monthly.iloc[[8,9,10]]["PM10"].mean(), df_monthly.iloc[[11,0,1]]["PM10"].mean(),
              df_monthly.iloc[[2,3,4]]["PM10"].mean()]
    s_pm25 = [df_monthly.iloc[[2,3,4]]["PM2.5"].mean(), df_monthly.iloc[[5,6,7]]["PM2.5"].mean(),
              df_monthly.iloc[[8,9,10]]["PM2.5"].mean(), df_monthly.iloc[[11,0,1]]["PM2.5"].mean(),
              df_monthly.iloc[[2,3,4]]["PM2.5"].mean()]
    fig_r  = go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=s_pm10, theta=theta, name="PM10",
        fill="toself", fillcolor="rgba(184,74,0,0.12)", line_color="#b84a00", line_width=2.5))
    fig_r.add_trace(go.Scatterpolar(r=s_pm25, theta=theta, name="PM2.5",
        fill="toself", fillcolor="rgba(224,123,26,0.12)", line_color="#e07b1a", line_width=2.5))
    fig_r.update_layout(
        paper_bgcolor="rgba(253,246,232,0.92)",
        font=dict(family="Noto Sans KR", color="#1a0f00", size=11),
        polar=dict(
            bgcolor="rgba(250,242,224,0.80)",
            radialaxis=dict(gridcolor="#ddd0b8", linecolor="#c4a070", tickfont=dict(size=9,color="#8a6a40")),
            angularaxis=dict(gridcolor="#ddd0b8", linecolor="#c4a070", tickfont=dict(size=11,color="#1a0f00")),
        ),
        height=360, margin=dict(l=50,r=50,t=50,b=50),
        legend=dict(bgcolor="rgba(253,246,232,0.85)", bordercolor="#d4b896"),
        title=dict(text="계절별 농도 레이더 (μg/m³)",
                   font=dict(family="Black Han Sans",size=14,color="#1a0f00")),
    )
    st.plotly_chart(fig_r, use_container_width=True)

    st.markdown("""<div class="anno-box">
    🌸 <b>봄 (3~4월)</b>: 중국발 황사 + 대기 정체 — 연중 최고 농도<br>
    ☀️ <b>여름 (7~8월)</b>: 강우와 대기 순환으로 연중 최저<br>
    ❄️ <b>겨울 (12~2월)</b>: 난방 연료 연소 + 대기 역전층 — 재상승
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 4 — WHO 기준 초과 분석
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-label">WHO 연평균 기준 초과 분석</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="who-bar">
    <strong>🚨 WHO 2021 가이드라인: PM2.5 = 5 μg/m³ / PM10 = 15 μg/m³ (연평균)</strong><br>
    <span style="font-size:0.8rem;color:#3d2800;">
    한국 환경기준(PM2.5: 15 μg/m³)보다 <b>3배</b> 엄격합니다.
    현재 한국의 모든 주요 도시는 WHO 기준을 초과하고 있습니다.
    </span>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([6, 4])
    with c1:
        exc_f = df_exceed[(df_exceed["연도"]>=year_range[0]) & (df_exceed["연도"]<=year_range[1])]
        fig   = go.Figure()
        fig.add_trace(go.Scatter(
            x=exc_f["연도"], y=exc_f["PM10 초과일"],
            name="PM10 초과일", fill="tozeroy",
            line=dict(color="#e07b1a", width=2),
            fillcolor="rgba(224,123,26,0.18)",
            hovertemplate="PM10 초과일 %{x}년: <b>%{y}일</b><extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=exc_f["연도"], y=exc_f["PM2.5 초과일"],
            name="PM2.5 초과일", fill="tozeroy",
            line=dict(color="#c0180a", width=2.5),
            fillcolor="rgba(192,24,10,0.15)",
            hovertemplate="PM2.5 초과일 %{x}년: <b>%{y}일</b><extra></extra>",
        ))
        fig.update_layout(**BASE, height=380,
            yaxis_title="연간 초과일수 (일)",
            title=dict(text="서울 WHO 기준 초과일수 추이",
                       font=dict(family="Black Han Sans",size=14,color="#1a0f00")))
        apply_axes(fig, dtick_x=5)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="sec-label">지역별 WHO 초과율</div>', unsafe_allow_html=True)
        exc_ratio = []
        for region in ALL_REGIONS:
            rdf = df_f[df_f["지역"]==region]
            exc_ratio.append({
                "지역": region,
                "PM2.5 초과율": float((rdf["PM2.5"]>5).mean()*100),
                "PM10 초과율":  float((rdf["PM10"]>15).mean()*100),
            })
        er_df = pd.DataFrame(exc_ratio).sort_values("PM2.5 초과율", ascending=False)
        for _, row in er_df.iterrows():
            r25   = float(row["PM2.5 초과율"])
            color = REGION_COLORS.get(row["지역"], "#b84a00")
            rc,gc,bc2 = int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
            st.markdown(f"""
            <div style="margin-bottom:0.8rem;">
              <div style="display:flex;justify-content:space-between;font-size:0.84rem;margin-bottom:4px;">
                <span style="font-weight:500;">{row['지역']}</span>
                <span style="color:{color};font-family:'JetBrains Mono';font-weight:700;">{r25:.0f}%</span>
              </div>
              <div style="background:#e0cca8;border-radius:6px;height:8px;overflow:hidden;box-shadow:inset 0 1px 3px rgba(0,0,0,0.1);">
                <div style="background:linear-gradient(90deg,rgba({rc},{gc},{bc2},1),rgba({rc},{gc},{bc2},0.7));height:100%;width:{r25:.0f}%;border-radius:6px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # WHO 배율 추이
    st.markdown('<div class="sec-label" style="margin-top:0.8rem;">WHO 기준 대비 배율 추이 (서울)</div>', unsafe_allow_html=True)
    df_sr  = df_annual[(df_annual["지역"]=="서울") &
                       (df_annual["연도"]>=year_range[0]) &
                       (df_annual["연도"]<=year_range[1])].sort_values("연도")
    mult25 = df_sr["PM2.5"] / 5
    mult10 = df_sr["PM10"]  / 15

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_sr["연도"], y=mult25, name="PM2.5 배율",
        line=dict(color="#c0180a", width=3),
        fill="tozeroy", fillcolor="rgba(192,24,10,0.10)",
        hovertemplate="PM2.5: WHO 기준의 <b>%{y:.1f}배</b><extra></extra>"))
    fig2.add_trace(go.Scatter(x=df_sr["연도"], y=mult10, name="PM10 배율",
        line=dict(color="#e07b1a", width=2.5),
        hovertemplate="PM10: WHO 기준의 <b>%{y:.1f}배</b><extra></extra>"))
    fig2.add_hline(y=1, line_dash="dash", line_color="#3a7a20", line_width=2,
        annotation_text="✅ WHO 기준선 (1배)",
        annotation_font_color="#3a7a20", annotation_font_size=11,
        annotation_position="top right")
    fig2.add_hrect(y0=0, y1=1, fillcolor="rgba(58,122,32,0.07)", line_width=0)
    fig2.update_layout(**BASE, height=340,
        yaxis_title="WHO 기준 대비 배율",
        title=dict(text="WHO 연평균 기준 대비 배율 추이",
                   font=dict(family="Black Han Sans",size=14,color="#1a0f00")))
    apply_axes(fig2, dtick_x=5)
    st.plotly_chart(fig2, use_container_width=True)

    # 10년 단위 요약
    st.markdown('<div class="sec-label" style="margin-top:0.8rem;">📋 10년 단위 요약 통계 (서울)</div>', unsafe_allow_html=True)
    dec_stats = []
    for ds in range(1975, 2025, 10):
        de  = min(ds+9, 2024)
        sub = df_annual[(df_annual["지역"]=="서울") & (df_annual["연도"]>=ds) & (df_annual["연도"]<=de)]
        if len(sub):
            dec_stats.append({
                "기간":           f"{ds}–{de}",
                "PM10 평균":      f"{sub['PM10'].mean():.1f} μg/m³",
                "PM2.5 평균":     f"{sub['PM2.5'].mean():.1f} μg/m³",
                "PM10 최대":      f"{sub['PM10'].max():.1f} μg/m³",
                "PM2.5 최대":     f"{sub['PM2.5'].max():.1f} μg/m³",
                "WHO PM2.5 배율": f"{sub['PM2.5'].mean()/5:.1f}×",
            })
    st.dataframe(pd.DataFrame(dec_stats), use_container_width=True, hide_index=True)
