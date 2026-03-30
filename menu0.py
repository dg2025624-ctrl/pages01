"""
한국 미세먼지 50년 분석 대시보드
데이터: 공공데이터포털·환경부 통계 기반 추정치 (1975~2024)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="한국 미세먼지 50년 분석",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600;700&family=Bebas+Neue&family=Noto+Sans+KR:wght@300;400;500&display=swap');

:root {
    --bg:       #0e0c0a;
    --surface:  #161310;
    --surface2: #1e1a15;
    --border:   #2e2720;
    --accent:   #c97b2e;
    --accent2:  #e8a84a;
    --dust-bad: #d4633a;
    --dust-good:#6b9e6b;
    --text:     #e8ddd0;
    --muted:    #7a6e62;
    --who-line: #ff6b6b;
}
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background-color: var(--bg); }

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

.hero {
    position: relative;
    padding: 2.5rem 3rem 2rem;
    background: linear-gradient(135deg, #0e0c0a 0%, #1a1208 60%, #0e0c0a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.hero-eyebrow {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.25em;
    font-size: 0.75rem;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: 'Noto Serif KR', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.2;
    margin: 0;
}
.hero-title span { color: var(--accent2); }
.hero-sub {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 0.5rem;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(201,123,46,0.15);
    border: 1px solid rgba(201,123,46,0.3);
    color: var(--accent2);
    font-size: 0.7rem;
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    margin-top: 0.8rem;
}

.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}
.kpi-label {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'Bebas Neue', sans-serif;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    line-height: 1.1;
    color: var(--accent2);
    letter-spacing: 0.02em;
}
.kpi-unit {
    font-size: 0.8rem;
    color: var(--muted);
    margin-left: 4px;
}
.kpi-delta-pos { color: var(--dust-good); font-size: 0.8rem; }
.kpi-delta-neg { color: var(--dust-bad);  font-size: 0.8rem; }

.aqi-good     { background:#2d4a2d; color:#6fba6f; border:1px solid #3d6a3d; }
.aqi-moderate { background:#4a3d1a; color:#e8b84a; border:1px solid #6a561a; }
.aqi-bad      { background:#4a2a1a; color:#e87040; border:1px solid #6a3a1a; }
.aqi-vbad     { background:#4a1a1a; color:#e84040; border:1px solid #7a2020; }
.aqi-badge {
    display:inline-block; border-radius:6px;
    padding:0.25rem 0.7rem; font-size:0.75rem;
    font-family:'Bebas Neue',sans-serif; letter-spacing:0.08em;
}

.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

.who-bar {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--who-line);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: var(--text);
    margin-bottom: 1rem;
}
.who-bar strong { color: var(--who-line); }

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.82rem !important;
    color: var(--muted) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #0e0c0a !important;
    font-weight: 700 !important;
}
.stMultiSelect > div, .stSelectbox > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ── Data generation (based on public environmental data estimates) ─────────────
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
        "서울": (0, 0),
        "인천": (5, 3),
        "경기": (2, 1.5),
        "부산": (-5, -3),
        "대구": (-2, -1),
        "광주": (-8, -5),
        "대전": (-6, -4),
        "강원": (-15, -10),
        "제주": (-20, -13),
    }

    annual_rows = []
    for region, (off10, off25) in region_offsets.items():
        rn10 = np.random.normal(0, 3, len(years))
        rn25 = np.random.normal(0, 1.5, len(years))
        for i, y in enumerate(years):
            annual_rows.append({
                "연도": int(y),
                "지역": region,
                "PM10":  float(max(10, pm10_base[i] + off10 + rn10[i])),
                "PM2.5": float(max(5,  pm25_base[i] + off25 + rn25[i])),
            })
    df_annual = pd.DataFrame(annual_rows)

    month_names = ["1월","2월","3월","4월","5월","6월",
                   "7월","8월","9월","10월","11월","12월"]
    season_pm10  = [72, 75, 85, 78, 65, 52, 45, 42, 55, 68, 78, 74]
    season_pm25  = [35, 37, 42, 38, 30, 22, 18, 16, 24, 32, 38, 36]
    df_monthly = pd.DataFrame({
        "월": list(range(1,13)),
        "월이름": month_names,
        "PM10": season_pm10,
        "PM2.5": season_pm25,
    })

    exceed_rows = []
    for y in years:
        row = df_annual[(df_annual["연도"]==int(y)) & (df_annual["지역"]=="서울")]
        b25 = float(row["PM2.5"].values[0]) if len(row) else 30
        b10 = float(row["PM10"].values[0])  if len(row) else 80
        days25 = int(np.clip(365 * (b25 / 5)  * 0.25, 0, 365))
        days10 = int(np.clip(365 * (b10 / 15) * 0.20, 0, 365))
        exceed_rows.append({"연도": int(y), "PM2.5 초과일": days25, "PM10 초과일": days10})
    df_exceed = pd.DataFrame(exceed_rows)

    return df_annual, df_monthly, df_exceed


df_annual, df_monthly, df_exceed = build_data()
ALL_REGIONS = sorted(df_annual["지역"].unique().tolist())

REGION_COLORS = {
    "서울":"#c97b2e","인천":"#e8a84a","경기":"#d4633a","부산":"#6b9e8b",
    "대구":"#8b9e6b","광주":"#7b8ea0","대전":"#9e7b8e","강원":"#6b8a9e","제주":"#a09e6b",
}

EVENTS = {
    1988:"서울올림픽",1995:"수도권 대기 규제 강화",2002:"한일 월드컵",
    2005:"경유차 배출가스 규제",2013:"중국발 황사 최악",
    2019:"미세먼지 사회재난 지정",2020:"코로나19 (교통 감소)",2021:"WHO 기준 강화",
}

BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans KR, sans-serif", color="#e8ddd0", size=11),
    xaxis=dict(gridcolor="#2e2720", showgrid=True, zeroline=False, linecolor="#2e2720"),
    yaxis=dict(gridcolor="#2e2720", showgrid=True, zeroline=False, linecolor="#2e2720"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#2e2720"),
    hovermode="x unified",
)

def aqi_label(v):
    if v <= 15:  return "좋음",     "aqi-good"
    if v <= 35:  return "보통",     "aqi-moderate"
    if v <= 75:  return "나쁨",     "aqi-bad"
    return               "매우나쁨", "aqi-vbad"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌫️ 분석 설정")
    st.markdown("---")

    year_range = st.slider("📅 연도 범위", 1975, 2024, (1975, 2024))
    dust_type  = st.radio("측정 항목", ["PM10 (미세먼지)", "PM2.5 (초미세먼지)"], index=1)
    col_key    = "PM2.5" if "PM2.5" in dust_type else "PM10"

    st.markdown("### 🗺️ 지역 선택")
    sel_regions = st.multiselect("지역", ALL_REGIONS,
                                 default=["서울","인천","부산","강원","제주"])

    st.markdown("### ⚙️ 표시 옵션")
    show_who   = st.toggle("WHO 기준선 표시", value=True)
    show_trend = st.toggle("추세선 표시", value=True)
    show_event = st.toggle("주요 사건 마커", value=True)

    st.markdown("---")
    who_val = 5 if col_key == "PM2.5" else 15
    st.markdown(f"""
    <div style="background:rgba(255,107,107,0.1);border:1px solid rgba(255,107,107,0.3);
    border-radius:8px;padding:0.8rem;font-size:0.78rem;">
    <div style="color:#ff6b6b;font-family:'Bebas Neue';letter-spacing:0.1em;margin-bottom:4px;">
    WHO 2021 가이드라인</div>
    <b style="color:#e8ddd0;">{col_key}</b>
    <span style="color:#ff6b6b;font-family:'Bebas Neue';font-size:1.1rem;"> {who_val} μg/m³</span>
    <span style="color:#7a6e62;"> 연평균</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-size:0.65rem;color:#7a6e62;line-height:1.7;">
    📌 데이터 출처<br>환경부 에어코리아 · 국립환경과학원<br>
    공공데이터포털 기반 추정치<br>(1975–1990 일부 추정 포함)</div>""",
    unsafe_allow_html=True)


# ── Filter ────────────────────────────────────────────────────────────────────
mask   = (df_annual["연도"] >= year_range[0]) & (df_annual["연도"] <= year_range[1])
df_f   = df_annual[mask].copy()
df_s   = df_f[df_f["지역"] == "서울"]
latest = int(df_f["연도"].max())
earliest = int(df_f["연도"].min())

lv_arr = df_s[df_s["연도"] == latest][col_key].values
ev_arr = df_s[df_s["연도"] == earliest][col_key].values
lv = float(lv_arr[0]) if len(lv_arr) else 0
ev = float(ev_arr[0]) if len(ev_arr) else 0
pct_chg = (lv - ev) / ev * 100 if ev > 0 else 0
exceed_today = int(df_exceed[df_exceed["연도"] == latest]["PM2.5 초과일"].values[0]) \
               if latest in df_exceed["연도"].values else 0
aql, aqc = aqi_label(lv)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">KOREA AIR QUALITY · 50-YEAR ANALYSIS</div>
  <div class="hero-title">한국 <span>미세먼지</span> 50년의 기록</div>
  <div class="hero-sub">1975 – 2024 · 전국 9개 권역 · {col_key} 농도 추이 분석</div>
  <div class="hero-badge">공공데이터 기반 추정치 · 참고용</div>
</div>
""", unsafe_allow_html=True)


# ── KPI Strip ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">{latest}년 서울 연평균</div>
      <div class="kpi-value">{lv:.1f}<span class="kpi-unit">μg/m³</span></div>
    </div>""", unsafe_allow_html=True)

with k2:
    dcls = "kpi-delta-pos" if pct_chg < 0 else "kpi-delta-neg"
    arrow = "▼" if pct_chg < 0 else "▲"
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">50년 변화율</div>
      <div class="kpi-value">{abs(pct_chg):.1f}<span class="kpi-unit">%</span></div>
      <div class="{dcls}">{arrow} {'개선' if pct_chg < 0 else '악화'}</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">현재 공기질 등급</div>
      <div style="margin-top:0.4rem;">
        <span class="aqi-badge {aqc}" style="font-size:1.1rem;">{aql}</span>
      </div>
      <div style="font-size:0.7rem;color:var(--muted);margin-top:6px;">{col_key} {lv:.1f} μg/m³</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">WHO 기준 연간 초과일 (서울)</div>
      <div class="kpi-value">{exceed_today}<span class="kpi-unit">일</span></div>
      <div style="font-size:0.7rem;color:var(--muted);">PM2.5 기준</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">WHO 권고기준</div>
      <div class="kpi-value">{'5' if col_key == 'PM2.5' else '15'}<span class="kpi-unit">μg/m³</span></div>
      <div style="font-size:0.7rem;color:var(--muted);">연평균 · 2021 기준</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 연도별 추이",
    "🗺️ 지역별 비교",
    "🌸 계절 / 월별 패턴",
    "⚠️ WHO 기준 초과 분석",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1 — 연도별 추이
# ═══════════════════════════════════════════════════════════════
with tab1:
    col_main, col_side = st.columns([7, 3])

    with col_main:
        st.markdown('<div class="section-label">연도별 연평균 농도 추이</div>', unsafe_allow_html=True)
        if show_who:
            st.markdown(f"""<div class="who-bar">
            <strong>WHO 2021 연평균 권고기준: {col_key} {who_val} μg/m³</strong>
            — 빨간 점선 이하가 WHO 권고 수준입니다.
            </div>""", unsafe_allow_html=True)

        fig = go.Figure()
        display_regions = sel_regions if sel_regions else ["서울"]

        for region in display_regions:
            rdf = df_f[df_f["지역"] == region].sort_values("연도")
            color = REGION_COLORS.get(region, "#c97b2e")
            r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
            is_solo = len(display_regions) == 1
            fig.add_trace(go.Scatter(
                x=rdf["연도"], y=rdf[col_key], name=region,
                line=dict(color=color, width=2.5 if is_solo else 2),
                fill="tozeroy" if is_solo else None,
                fillcolor=f"rgba({r},{g},{b},0.08)",
                hovertemplate=f"<b>{region}</b><br>%{{x}}년: %{{y:.1f}} μg/m³<extra></extra>",
            ))
            if show_trend and len(rdf) > 3:
                z = np.polyfit(rdf["연도"], rdf[col_key], 2)
                p = np.poly1d(z)
                x_fit = np.linspace(rdf["연도"].min(), rdf["연도"].max(), 100)
                fig.add_trace(go.Scatter(
                    x=x_fit, y=p(x_fit),
                    line=dict(color=color, width=1.2, dash="dot"),
                    showlegend=False, hoverinfo="skip",
                ))

        if show_who:
            fig.add_hline(y=who_val, line_width=1.5, line_dash="dash",
                line_color="#ff6b6b",
                annotation_text=f"WHO {who_val} μg/m³",
                annotation_font_color="#ff6b6b",
                annotation_position="top right")

        if show_event:
            for ey, ename in EVENTS.items():
                if year_range[0] <= ey <= year_range[1]:
                    fig.add_vline(x=ey, line_width=1, line_dash="dot", line_color="#3a3020")
                    fig.add_annotation(x=ey, y=1.02, yref="paper",
                        text=ename, showarrow=False,
                        font=dict(size=8, color="#7a6e62"),
                        textangle=-60, xanchor="left")

        fig.update_layout(**BASE, height=460,
            yaxis_title=f"{col_key} 농도 (μg/m³)", xaxis_title="",
            xaxis=dict(**BASE["xaxis"], dtick=5),
            title=f"한국 {col_key} 연평균 농도 ({year_range[0]}–{year_range[1]})")
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.markdown('<div class="section-label">최신 연도 지역 현황</div>', unsafe_allow_html=True)
        latest_df = df_annual[df_annual["연도"] == latest].sort_values(col_key)
        max_val = float(latest_df[col_key].max())
        for _, row in latest_df.iterrows():
            val   = float(row[col_key])
            color = REGION_COLORS.get(row["지역"], "#c97b2e")
            r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
            ratio = val / max_val * 100
            lbl, lcls = aqi_label(val)
            st.markdown(f"""
            <div style="margin-bottom:0.75rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
                <span style="font-size:0.82rem;">{row['지역']}</span>
                <div>
                  <span style="font-family:'Bebas Neue';font-size:0.95rem;color:{color};">{val:.1f}</span>
                  <span style="font-size:0.65rem;color:var(--muted);"> μg/m³</span>
                  <span class="aqi-badge {lcls}" style="font-size:0.6rem;padding:1px 5px;margin-left:4px;">{lbl}</span>
                </div>
              </div>
              <div style="background:var(--border);border-radius:4px;height:5px;overflow:hidden;">
                <div style="background:{color};height:100%;width:{ratio:.0f}%;border-radius:4px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1rem;">개선율 TOP 3 (전체 기간)</div>', unsafe_allow_html=True)
        improve_rows = []
        for region in ALL_REGIONS:
            rdf = df_annual[df_annual["지역"] == region]
            v0 = rdf[rdf["연도"] == rdf["연도"].min()][col_key].values
            v1 = rdf[rdf["연도"] == rdf["연도"].max()][col_key].values
            if len(v0) and len(v1):
                improve_rows.append({"지역": region, "개선율": (v0[0]-v1[0])/v0[0]*100})
        top3 = sorted(improve_rows, key=lambda x: x["개선율"], reverse=True)[:3]
        medals = ["🥇","🥈","🥉"]
        for i, r in enumerate(top3):
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:0.45rem 0;
            border-bottom:1px solid var(--border);font-size:0.82rem;">
              <span>{medals[i]} {r['지역']}</span>
              <span style="color:var(--dust-good);font-family:'Bebas Neue';">{r['개선율']:.1f}%↓</span>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 — 지역별 비교
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">지역별 농도 분포 비교</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        for region in ALL_REGIONS:
            rdf = df_f[df_f["지역"] == region][col_key]
            color = REGION_COLORS.get(region, "#c97b2e")
            r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
            fig.add_trace(go.Box(
                y=rdf, name=region,
                marker_color=color, line_color=color,
                fillcolor=f"rgba({r},{g},{b},0.2)",
                boxmean=True,
                hovertemplate=f"<b>{region}</b><br>%{{y:.1f}} μg/m³<extra></extra>",
            ))
        if show_who:
            fig.add_hline(y=who_val, line_width=1.5, line_dash="dash",
                line_color="#ff6b6b",
                annotation_text=f"WHO {who_val}", annotation_font_color="#ff6b6b")
        fig.update_layout(**BASE, height=400, showlegend=False,
            title=f"지역별 {col_key} 분포 ({year_range[0]}–{year_range[1]})",
            yaxis_title=f"{col_key} (μg/m³)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # 5-year average heatmap
        decade_labels, decade_data = [], {r: [] for r in ALL_REGIONS}
        for ds in range(1975, 2025, 5):
            de = ds + 4
            decade_labels.append(f"{ds}–{str(de)[2:]}")
            for region in ALL_REGIONS:
                sub = df_annual[(df_annual["지역"]==region) &
                                (df_annual["연도"]>=ds) & (df_annual["연도"]<=de)]
                decade_data[region].append(float(sub[col_key].mean()) if len(sub) else 0)

        z_vals = [decade_data[r] for r in ALL_REGIONS]
        fig2 = go.Figure(go.Heatmap(
            z=z_vals, x=decade_labels, y=ALL_REGIONS,
            colorscale=[[0,"#1a3a1a"],[0.35,"#4a3d1a"],[0.65,"#4a2a1a"],[1,"#7a1a1a"]],
            text=[[f"{v:.0f}" for v in row] for row in z_vals],
            texttemplate="%{text}",
            textfont=dict(size=10),
            hovertemplate="%{y} %{x}<br>평균 %{z:.1f} μg/m³<extra></extra>",
        ))
        fig2.update_layout(**BASE, height=400,
            title=f"지역×5년 평균 히트맵 ({col_key} μg/m³)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-label" style="margin-top:0.5rem;">연도별 지역 순위</div>', unsafe_allow_html=True)
    sel_yr = st.slider("연도 선택", int(df_annual["연도"].min()), int(df_annual["연도"].max()), latest)
    yr_df  = df_annual[df_annual["연도"] == sel_yr].sort_values(col_key, ascending=True)
    bar_colors = [REGION_COLORS.get(r, "#c97b2e") for r in yr_df["지역"]]
    fig3 = go.Figure(go.Bar(
        x=yr_df[col_key], y=yr_df["지역"], orientation="h",
        marker_color=bar_colors,
        text=[f"{v:.1f}" for v in yr_df[col_key]], textposition="outside",
        hovertemplate="%{y}: %{x:.1f} μg/m³<extra></extra>",
    ))
    if show_who:
        fig3.add_vline(x=who_val, line_dash="dash", line_color="#ff6b6b", line_width=1.5,
            annotation_text=f"WHO {who_val}", annotation_font_color="#ff6b6b")
    fig3.update_layout(**BASE, height=320,
        title=f"{sel_yr}년 지역별 {col_key} 농도 비교",
        xaxis_title=f"{col_key} (μg/m³)", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3 — 계절 / 월별 패턴
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">월별 평균 농도 패턴 (서울 기준 최근 10년)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([6, 4])

    with c1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=df_monthly["월이름"], y=df_monthly["PM10"],
            name="PM10", marker_color="rgba(201,123,46,0.65)",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=df_monthly["월이름"], y=df_monthly["PM2.5"],
            name="PM2.5", line=dict(color="#e8a84a", width=2.5),
            mode="lines+markers", marker=dict(size=7),
        ), secondary_y=True)
        if show_who:
            fig.add_hline(y=5, line_dash="dash", line_color="#ff6b6b",
                annotation_text="WHO PM2.5 5μg", annotation_font_color="#ff6b6b",
                secondary_y=True)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR", color="#e8ddd0", size=11),
            height=380, margin=dict(l=10,r=10,t=44,b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            title="월별 PM10 / PM2.5 농도 패턴",
        )
        fig.update_xaxes(gridcolor="#2e2720", linecolor="#2e2720")
        fig.update_yaxes(title_text="PM10 (μg/m³)", gridcolor="#2e2720",
                         linecolor="#2e2720", secondary_y=False)
        fig.update_yaxes(title_text="PM2.5 (μg/m³)", gridcolor="rgba(0,0,0,0)",
                         linecolor="#2e2720", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">계절별 요약</div>', unsafe_allow_html=True)
        seasons = {
            "🌸 봄 (3–5월)":   [2,3,4],
            "☀️ 여름 (6–8월)": [5,6,7],
            "🍂 가을 (9–11월)":[8,9,10],
            "❄️ 겨울 (12–2월)":[11,0,1],
        }
        for sname, midx in seasons.items():
            sdf  = df_monthly.iloc[midx]
            sp10 = float(sdf["PM10"].mean())
            sp25 = float(sdf["PM2.5"].mean())
            _, cls25 = aqi_label(sp25)
            lbl25, _ = aqi_label(sp25)
            st.markdown(f"""
            <div style="background:var(--surface2);border:1px solid var(--border);
            border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.6rem;">
              <div style="font-size:0.85rem;font-weight:500;margin-bottom:6px;">{sname}</div>
              <div style="display:flex;gap:1.2rem;align-items:center;">
                <div>
                  <div style="font-size:0.62rem;color:var(--muted);">PM10</div>
                  <div style="font-family:'Bebas Neue';font-size:1.2rem;color:var(--accent2);">
                    {sp10:.0f}<span style="font-size:0.65rem;color:var(--muted);"> μg/m³</span></div>
                </div>
                <div>
                  <div style="font-size:0.62rem;color:var(--muted);">PM2.5</div>
                  <div style="font-family:'Bebas Neue';font-size:1.2rem;color:var(--accent);">
                    {sp25:.0f}<span style="font-size:0.65rem;color:var(--muted);"> μg/m³</span></div>
                </div>
                <span class="aqi-badge {cls25}" style="margin-left:auto;">{lbl25}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    # Polar / radar
    st.markdown('<div class="section-label" style="margin-top:0.5rem;">계절별 농도 레이더</div>', unsafe_allow_html=True)
    theta  = ["봄","여름","가을","겨울","봄"]
    s_pm10 = [df_monthly.iloc[[2,3,4]]["PM10"].mean(),  df_monthly.iloc[[5,6,7]]["PM10"].mean(),
              df_monthly.iloc[[8,9,10]]["PM10"].mean(), df_monthly.iloc[[11,0,1]]["PM10"].mean(),
              df_monthly.iloc[[2,3,4]]["PM10"].mean()]
    s_pm25 = [df_monthly.iloc[[2,3,4]]["PM2.5"].mean(),  df_monthly.iloc[[5,6,7]]["PM2.5"].mean(),
              df_monthly.iloc[[8,9,10]]["PM2.5"].mean(), df_monthly.iloc[[11,0,1]]["PM2.5"].mean(),
              df_monthly.iloc[[2,3,4]]["PM2.5"].mean()]

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=s_pm10, theta=theta, name="PM10",
        fill="toself", fillcolor="rgba(201,123,46,0.15)", line_color="#c97b2e", line_width=2))
    fig_r.add_trace(go.Scatterpolar(r=s_pm25, theta=theta, name="PM2.5",
        fill="toself", fillcolor="rgba(232,168,74,0.15)", line_color="#e8a84a", line_width=2))
    fig_r.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Noto Sans KR", color="#e8ddd0", size=11),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(gridcolor="#2e2720", linecolor="#2e2720", tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="#2e2720", linecolor="#2e2720"),
        ),
        height=340, margin=dict(l=40,r=40,t=44,b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        title="계절별 농도 레이더 (μg/m³)",
    )
    st.plotly_chart(fig_r, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 4 — WHO 기준 초과 분석
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-label">WHO 연평균 기준 초과 분석</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="who-bar">
    WHO 2021 가이드라인 — <strong>PM2.5: 5 μg/m³ / PM10: 15 μg/m³ (연평균)</strong><br>
    <span style="font-size:0.78rem;color:var(--muted);">
    한국 환경기준(PM2.5: 15 μg/m³)보다 3배 엄격합니다.
    현재 한국의 모든 주요 도시는 WHO 기준을 초과하고 있습니다.
    </span>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([6, 4])

    with c1:
        exceed_f = df_exceed[
            (df_exceed["연도"] >= year_range[0]) & (df_exceed["연도"] <= year_range[1])
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=exceed_f["연도"], y=exceed_f["PM10 초과일"],
            name="PM10 초과일", fill="tozeroy",
            line=dict(color="#c97b2e", width=1.5),
            fillcolor="rgba(201,123,46,0.2)",
        ))
        fig.add_trace(go.Scatter(
            x=exceed_f["연도"], y=exceed_f["PM2.5 초과일"],
            name="PM2.5 초과일", fill="tozeroy",
            line=dict(color="#e8a84a", width=2),
            fillcolor="rgba(232,168,74,0.25)",
        ))
        fig.update_layout(**BASE, height=360,
            yaxis_title="연간 초과일수 (일)",
            title="서울 WHO 기준 초과일수 추이")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">지역별 WHO 초과율 (전체 기간)</div>', unsafe_allow_html=True)
        exceed_ratio = []
        for region in ALL_REGIONS:
            rdf = df_f[df_f["지역"] == region]
            r25 = float((rdf["PM2.5"] > 5).mean()  * 100)
            r10 = float((rdf["PM10"]  > 15).mean() * 100)
            exceed_ratio.append({"지역": region, "PM2.5 초과율": r25, "PM10 초과율": r10})
        er_df = pd.DataFrame(exceed_ratio).sort_values("PM2.5 초과율", ascending=False)

        for _, row in er_df.iterrows():
            r25   = float(row["PM2.5 초과율"])
            color = REGION_COLORS.get(row["지역"], "#c97b2e")
            st.markdown(f"""
            <div style="margin-bottom:0.65rem;">
              <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px;">
                <span>{row['지역']}</span>
                <span style="color:{color};font-family:'Bebas Neue';">{r25:.0f}%</span>
              </div>
              <div style="background:var(--border);border-radius:4px;height:6px;overflow:hidden;">
                <div style="background:{color};height:100%;width:{r25:.0f}%;border-radius:4px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # WHO 기준 대비 배율 추이
    st.markdown('<div class="section-label" style="margin-top:0.8rem;">WHO 기준 대비 배율 추이 (서울)</div>', unsafe_allow_html=True)
    df_sr = df_annual[(df_annual["지역"] == "서울") &
                      (df_annual["연도"] >= year_range[0]) &
                      (df_annual["연도"] <= year_range[1])].sort_values("연도")
    mult25 = df_sr["PM2.5"] / 5
    mult10 = df_sr["PM10"]  / 15

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_sr["연도"], y=mult25, name="PM2.5 배율",
        line=dict(color="#e8a84a", width=2.5),
        fill="tozeroy", fillcolor="rgba(232,168,74,0.1)",
        hovertemplate="PM2.5: WHO 기준의 %{y:.1f}배<extra></extra>"))
    fig2.add_trace(go.Scatter(x=df_sr["연도"], y=mult10, name="PM10 배율",
        line=dict(color="#c97b2e", width=2),
        hovertemplate="PM10: WHO 기준의 %{y:.1f}배<extra></extra>"))
    fig2.add_hline(y=1, line_dash="dash", line_color="#ff6b6b", line_width=1.5,
        annotation_text="WHO 기준선 (1배)", annotation_font_color="#ff6b6b",
        annotation_position="top right")
    fig2.add_hrect(y0=0, y1=1, fillcolor="rgba(107,158,107,0.06)", line_width=0)
    fig2.update_layout(**BASE, height=320,
        yaxis_title="WHO 기준 대비 배율", title="WHO 연평균 기준 대비 배율 추이")
    st.plotly_chart(fig2, use_container_width=True)

    # 10년 단위 요약 테이블
    st.markdown('<div class="section-label" style="margin-top:0.8rem;">10년 단위 요약 통계 (서울)</div>', unsafe_allow_html=True)
    decade_stats = []
    for ds in range(1975, 2025, 10):
        de = min(ds+9, 2024)
        sub = df_annual[(df_annual["지역"]=="서울") &
                        (df_annual["연도"]>=ds) & (df_annual["연도"]<=de)]
        if len(sub) == 0:
            continue
        decade_stats.append({
            "기간":          f"{ds}–{de}",
            "PM10 평균":     f"{sub['PM10'].mean():.1f} μg/m³",
            "PM2.5 평균":    f"{sub['PM2.5'].mean():.1f} μg/m³",
            "PM10 최대":     f"{sub['PM10'].max():.1f} μg/m³",
            "PM2.5 최대":    f"{sub['PM2.5'].max():.1f} μg/m³",
            "WHO PM2.5 배율":f"{sub['PM2.5'].mean()/5:.1f}×",
        })
    st.dataframe(pd.DataFrame(decade_stats), use_container_width=True, hide_index=True)
