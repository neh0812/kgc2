"""
KGC 인삼공사 · 주간 마케팅 통찰 보고서
구글 스프레드시트 연동 버전
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ────────────────────────────────────────────
# 페이지 설정
# ────────────────────────────────────────────
st.set_page_config(
    page_title="KGC 주간 마케팅 통찰 보고서 · 2026 W13",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ────────────────────────────────────────────
# 구글 스프레드시트 데이터 로드
# ────────────────────────────────────────────
# ★ 여기에 본인의 스프레드시트 ID 입력 ★
SHEET_ID = "여기에_스프레드시트_ID_입력"

@st.cache_data(ttl=300)  # 5분마다 자동 갱신
def load_sheet(sheet_name):
    from urllib.parse import quote
    encoded_name = quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    try:
        import io, requests
response = requests.get(url)
response.encoding = "utf-8"
df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}\n스프레드시트 ID와 공유 설정을 확인하세요.")
        return None

# 데이터 불러오기
df_kpi     = load_sheet("KPI")
df_channel = load_sheet("channel")
df_age     = load_sheet("연령")

# 데이터 파싱
if df_kpi is not None:
    kpi_values = dict(zip(df_kpi["항목"], df_kpi["값"].astype(float)))
    kpi_desc   = dict(zip(df_kpi["항목"], df_kpi["설명"]))
    weekly_summary = kpi_desc.get("주간요약", "이번 주 주요 지표를 확인하세요.")
else:
    # 데이터 로드 실패 시 기본값
    kpi_values = {"수도권판매증감":15, "지방판매증감":-2, "주력연령층비중":45, "액티브키워드증가":30}
    kpi_desc   = {"수도권판매증감":"편의점 채널 강세", "지방판매증감":"대형마트 채널 정체",
                  "주력연령층비중":"2030 사회초년생", "액티브키워드증가":"등산·테니스 언급"}
    weekly_summary = "이번 주 수도권 편의점 채널 강세, 액티브 키워드 확산 포착."

# ────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif !important; }
.stApp { background-color: #f7f6f2; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }
.brand-tag { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: #9a6f20; margin-bottom: 8px; }
.report-title { font-size: 36px; font-weight: 700; color: #1a1a1a; line-height: 1.2; margin: 0; padding: 0; }
.report-title em { color: #b8860b; font-style: italic; }
.report-sub { font-size: 13px; color: #9090a8; margin-top: 4px; font-weight: 300; }
.report-meta { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #9090a8; line-height: 2; text-align: right; }
.report-meta b { color: #4a4a5a; }
.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #9090a8; border-bottom: 1px solid rgba(0,0,0,0.07); padding-bottom: 8px; margin-bottom: 16px; margin-top: 8px; }
.kpi-card { background: #ffffff; border: 1px solid rgba(0,0,0,0.07); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 14px 14px 0 0; }
.kpi-up::before   { background: linear-gradient(90deg, #1e7a50, transparent); }
.kpi-down::before { background: linear-gradient(90deg, #c0392b, transparent); }
.kpi-gold::before { background: linear-gradient(90deg, #9a6f20, transparent); }
.kpi-blue::before { background: linear-gradient(90deg, #2563c8, transparent); }
.kpi-label { font-size: 11px; color: #9090a8; margin-bottom: 8px; letter-spacing: 0.04em; }
.kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 32px; font-weight: 600; line-height: 1; margin-bottom: 6px; }
.kpi-sub   { font-size: 12px; color: #9090a8; line-height: 1.5; font-weight: 300; }
.kpi-badge { position: absolute; top: 16px; right: 16px; font-size: 20px; opacity: 0.45; }
.color-up   { color: #1e7a50; }
.color-down { color: #c0392b; }
.color-gold { color: #b8860b; }
.color-blue { color: #2563c8; }
.panel { background: #ffffff; border: 1px solid rgba(0,0,0,0.07); border-radius: 14px; padding: 22px; }
.panel-title { font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #4a4a5a; margin-bottom: 16px; }
.review-card { border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; display: flex; gap: 12px; border: 1px solid transparent; }
.review-pos  { background: rgba(30,122,80,0.07); }
.review-neg  { background: rgba(192,57,43,0.07); }
.review-tag  { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 4px; }
.tag-pos { background: rgba(30,122,80,0.15); color: #1e7a50; }
.tag-neg { background: rgba(192,57,43,0.15); color: #c0392b; }
.review-text { font-size: 13px; color: #4a4a5a; line-height: 1.6; font-weight: 300; }
.kw-cloud { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.kw-tag   { padding: 5px 13px; border-radius: 100px; font-size: 12px; font-weight: 500; border: 1px solid; display: inline-block; }
.kw-gold  { background: rgba(184,134,11,0.1);  border-color: rgba(184,134,11,0.3);  color: #9a6f20; }
.kw-green { background: rgba(30,122,80,0.09);  border-color: rgba(30,122,80,0.3);   color: #1e7a50; }
.kw-blue  { background: rgba(37,99,200,0.08);  border-color: rgba(37,99,200,0.25);  color: #2563c8; }
.kw-amber { background: rgba(196,122,32,0.09); border-color: rgba(196,122,32,0.3);  color: #c47a20; }
.insight-card    { background: #ffffff; border: 1px solid rgba(0,0,0,0.07); border-radius: 14px; padding: 20px; margin-bottom: 12px; }
.insight-heading { font-size: 14px; font-weight: 700; color: #1a1a1a; margin: 6px 0; }
.insight-body    { font-size: 13px; color: #4a4a5a; line-height: 1.7; font-weight: 300; }
.priority-badge  { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 10px; border-radius: 100px; margin-top: 10px; }
.p-high { background: rgba(192,57,43,0.12); color: #c0392b; }
.p-mid  { background: rgba(196,122,32,0.1);  color: #c47a20; }
.p-low  { background: rgba(30,122,80,0.09);  color: #1e7a50; }
.matrix-cell  { border-radius: 10px; padding: 14px; border: 1px solid rgba(0,0,0,0.07); height: 100%; }
.mc-star { background: rgba(184,134,11,0.08); }
.mc-cash { background: rgba(30,122,80,0.07);  }
.mc-risk { background: rgba(192,57,43,0.07);  }
.mc-ques { background: rgba(37,99,200,0.07);  }
.mc-label { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
.mc-gold  { color: #9a6f20; }
.mc-green { color: #1e7a50; }
.mc-red   { color: #c0392b; }
.mc-blue  { color: #2563c8; }
.mc-body  { font-size: 12px; color: #4a4a5a; line-height: 1.6; font-weight: 300; }
.action-item  { background: #ffffff; border: 1px solid rgba(0,0,0,0.07); border-radius: 12px; padding: 16px; margin-bottom: 10px; display: flex; gap: 14px; align-items: flex-start; }
.action-num   { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 600; color: rgba(0,0,0,0.07); min-width: 28px; line-height: 1; }
.action-title { font-size: 14px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
.action-desc  { font-size: 12px; color: #4a4a5a; line-height: 1.65; font-weight: 300; }
.action-tag   { font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; display: inline-block; margin: 2px; }
.at-red   { background: rgba(192,57,43,0.1);  color: #c0392b; }
.at-blue  { background: rgba(37,99,200,0.1);  color: #2563c8; }
.at-amber { background: rgba(196,122,32,0.1); color: #c47a20; }
.at-green { background: rgba(30,122,80,0.09); color: #1e7a50; }
.at-gray  { background: rgba(0,0,0,0.05);     color: #4a4a5a; }
.ch-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.ch-table th { padding: 10px 12px; font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #9090a8; text-align: left; border-bottom: 1px solid rgba(0,0,0,0.07); white-space: nowrap; background: #f7f6f2; }
.ch-table td { padding: 12px 12px; border-bottom: 1px solid rgba(0,0,0,0.06); color: #4a4a5a; vertical-align: top; line-height: 1.6; font-weight: 300; }
.ch-table tr:last-child td { border-bottom: none; }
.ch-badge { display: inline-block; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.comment-panel { background: #ffffff; border: 1px solid rgba(184,134,11,0.2); border-radius: 14px; padding: 22px; margin-bottom: 28px; }
.comment-label { font-size: 10px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #9a6f20; margin-bottom: 8px; }
.comment-text  { font-size: 14px; color: #4a4a5a; line-height: 1.85; font-weight: 300; }
.page-footer { border-top: 1px solid rgba(0,0,0,0.07); padding-top: 20px; margin-top: 32px; display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #9090a8; }
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid rgba(0,0,0,0.07); gap: 0; }
.stTabs [data-baseweb="tab"] { font-family: 'Noto Sans KR', sans-serif; font-size: 13px; font-weight: 500; color: #9090a8; padding: 10px 20px; border: none; background: transparent; }
.stTabs [aria-selected="true"] { color: #b8860b !important; border-bottom: 2px solid #b8860b !important; background: transparent !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px; }
.sync-badge { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; color: #1e7a50; background: rgba(30,122,80,0.09); border: 1px solid rgba(30,122,80,0.2); padding: 4px 12px; border-radius: 100px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 헤더
# ════════════════════════════════════════════
col_left, col_right = st.columns([2, 1])
with col_left:
    st.markdown(f"""
    <div style="border-bottom:1px solid rgba(0,0,0,0.08);padding-bottom:24px;margin-bottom:28px;">
      <div class="brand-tag">— KGC 인삼공사 · 브랜드전략실</div>
      <div class="report-title">주간 마케팅 <em>통찰 보고서</em></div>
      <div class="report-sub">정관장 에브리타임 밸런스 (리뉴얼) · 2026년 3월 4주차</div>
      <div style="margin-top:12px; padding:12px 16px; background:rgba(184,134,11,0.08); border-left:3px solid #b8860b; border-radius:6px; font-size:13px; color:#4a4a5a; font-weight:300; line-height:1.7;">
        📋 {weekly_summary}
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="report-meta" style="margin-top:12px;">
      <div><b>작성</b>&nbsp;&nbsp;브랜드전략실 마케팅팀</div>
      <div><b>기간</b>&nbsp;&nbsp;2026.03.24 – 03.30</div>
      <div><b>분석건수</b>&nbsp;&nbsp;고객리뷰 500건</div>
      <div><b>배포대상</b>&nbsp;&nbsp;브랜드 매니저</div>
    </div>
    """, unsafe_allow_html=True)

# 데이터 동기화 상태 + 새로고침 버튼
sync_col, btn_col = st.columns([3, 1])
with sync_col:
    st.markdown('<div class="sync-badge">🟢 구글 스프레드시트 연동 중 · 5분마다 자동 갱신</div>', unsafe_allow_html=True)
with btn_col:
    if st.button("🔄 지금 새로고침"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 01 · KPI 카드 (스프레드시트 데이터 반영)
# ════════════════════════════════════════════
st.markdown('<div class="sec-label">01 · 핵심 지표 요약</div>', unsafe_allow_html=True)

v1 = kpi_values.get("수도권판매증감", 0)
v2 = kpi_values.get("지방판매증감", 0)
v3 = kpi_values.get("주력연령층비중", 0)
v4 = kpi_values.get("액티브키워드증가", 0)

d1 = kpi_desc.get("수도권판매증감", "")
d2 = kpi_desc.get("지방판매증감", "")
d3 = kpi_desc.get("주력연령층비중", "")
d4 = kpi_desc.get("액티브키워드증가", "")

k1, k2, k3, k4 = st.columns(4)

with k1:
    cls = "kpi-up" if v1 >= 0 else "kpi-down"
    vcls = "color-up" if v1 >= 0 else "color-down"
    badge = "📈" if v1 >= 0 else "📉"
    val_str = f"+{v1:.0f}%" if v1 >= 0 else f"{v1:.0f}%"
    st.markdown(f"""
    <div class="kpi-card {cls}">
      <div class="kpi-badge">{badge}</div>
      <div class="kpi-label">수도권 판매량 증감 (전주比)</div>
      <div class="kpi-value {vcls}">{val_str}</div>
      <div class="kpi-sub">{d1}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    cls = "kpi-up" if v2 >= 0 else "kpi-down"
    vcls = "color-up" if v2 >= 0 else "color-down"
    badge = "📈" if v2 >= 0 else "📉"
    val_str = f"+{v2:.0f}%" if v2 >= 0 else f"{v2:.0f}%"
    st.markdown(f"""
    <div class="kpi-card {cls}">
      <div class="kpi-badge">{badge}</div>
      <div class="kpi-label">지방 판매량 증감 (전주比)</div>
      <div class="kpi-value {vcls}">{val_str}</div>
      <div class="kpi-sub">{d2}</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card kpi-gold">
      <div class="kpi-badge">🎯</div>
      <div class="kpi-label">주력 구매 연령층</div>
      <div class="kpi-value color-gold">{v3:.0f}%</div>
      <div class="kpi-sub">{d3}</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card kpi-blue">
      <div class="kpi-badge">🏃</div>
      <div class="kpi-label">액티브 키워드 언급 증가</div>
      <div class="kpi-value color-blue">+{v4:.0f}%</div>
      <div class="kpi-sub">{d4}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 02 · 채널 분석 + 연령 분포 (스프레드시트 데이터)
# ════════════════════════════════════════════
st.markdown('<div class="sec-label">02 · 판매 채널 및 구매자 분석</div>', unsafe_allow_html=True)

ch_col, age_col = st.columns(2, gap="medium")

with ch_col:
    st.markdown('<div class="panel"><div class="panel-title">📊 채널별 판매 비중 추정</div>', unsafe_allow_html=True)

    if df_channel is not None:
        ch_names  = df_channel["채널명"].tolist()
        ch_scores = df_channel["점수"].astype(float).tolist()
        ch_status = df_channel["상태"].tolist()
        ch_colors_map = {"강세 ▲":"#1e7a50","성장 →":"#2563c8","정체 ▼":"#c0392b","기회 ◆":"#c47a20"}
        ch_colors = [ch_colors_map.get(s, "#9090a8") for s in ch_status]
    else:
        ch_names  = ["편의점 (수도권)","온라인 (추정)","대형마트 (지방)","약국·헬스숍"]
        ch_scores = [72, 55, 38, 28]
        ch_status = ["강세 ▲","성장 →","정체 ▼","기회 ◆"]
        ch_colors = ["#1e7a50","#2563c8","#c0392b","#c47a20"]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=ch_scores, y=ch_names,
        orientation="h",
        marker=dict(color=ch_colors, opacity=0.85, line=dict(width=0)),
        text=ch_status,
        textposition="outside",
        textfont=dict(size=11, color=ch_colors),
        hovertemplate="%{y}: %{x}%<extra></extra>",
        width=0.55,
    ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=60, t=4, b=0),
        font=dict(family="Noto Sans KR, sans-serif", color="#4a4a5a"),
        showlegend=False, height=220,
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 100]),
        yaxis=dict(tickfont=dict(size=12, color="#4a4a5a"), showgrid=False),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with age_col:
    st.markdown('<div class="panel"><div class="panel-title">👥 구매 연령 분포</div>', unsafe_allow_html=True)

    if df_age is not None:
        age_labels = df_age["연령대"].tolist()
        age_values = df_age["비중"].astype(float).tolist()
    else:
        age_labels = ["2030 사회초년생","4050 직장인","60대 이상","기타"]
        age_values = [45, 32, 14, 9]

    fig_pie = go.Figure(go.Pie(
        labels=age_labels, values=age_values,
        hole=0.52,
        marker=dict(colors=["#9a6f20","#1e7a50","#2563c8","#9090a8"], line=dict(color="#f7f6f2", width=2)),
        textinfo="percent",
        textfont=dict(size=11, color="#ffffff"),
        hovertemplate="%{label}: %{value}%<extra></extra>",
        rotation=90,
    ))
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=4, b=0),
        font=dict(family="Noto Sans KR, sans-serif", color="#4a4a5a"),
        showlegend=True, height=200,
        legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=11, color="#4a4a5a")),
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 03 · 고객 리뷰
# ════════════════════════════════════════════
st.markdown('<div class="sec-label">03 · 고객 리뷰 분석 (500건)</div>', unsafe_allow_html=True)

pos_col, neg_col = st.columns(2, gap="medium")
with pos_col:
    st.markdown("""
    <div class="panel">
      <div class="panel-title">💬 긍정 리뷰 핵심</div>
      <div class="review-card review-pos">
        <div style="font-size:18px;">🎁</div>
        <div><span class="review-tag tag-pos">패키지</span>
        <div class="review-text">"포장이 세련되어 선물용으로 좋다" — 리뉴얼 패키지가 선물 수요를 직접 자극. 기념일·명절 시즌 선물 기획전 연동 가능.</div></div>
      </div>
      <div class="review-card review-pos">
        <div style="font-size:18px;">😋</div>
        <div><span class="review-tag tag-pos">맛/편의성</span>
        <div class="review-text">"기존보다 쓴맛이 덜해 먹기 편하다" — 홍삼 복용 장벽 해소. 거부감 보유 소비자 재유입 포인트로 메시지화 필요.</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

with neg_col:
    st.markdown("""
    <div class="panel">
      <div class="panel-title">⚠️ 개선 요구 리뷰 핵심</div>
      <div class="review-card review-neg">
        <div style="font-size:18px;">💰</div>
        <div><span class="review-tag tag-neg">가격 민감도</span>
        <div class="review-text">"가격이 작년보다 오른 느낌이다" — 원가 인상 체감이 구매 이탈로 이어질 수 있음. 용량 대비 가치 소구 또는 구독형 구매 혜택 강조 필요.</div></div>
      </div>
      <div class="review-card review-neg">
        <div style="font-size:18px;">📦</div>
        <div><span class="review-tag tag-neg">패키지 불편</span>
        <div class="review-text">"박스 개봉이 가끔 뻑뻑하다" — 반복 구매 UX에 직접적 마찰. 품질팀과 협업하여 개봉 구조 개선 또는 박스 재질 검토 권고.</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="panel">
  <div class="panel-title">🔍 신규 라이프스타일 키워드 포착 — 전주 대비 +30% 증가</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
    <div>
      <div style="font-size:11px;color:#9090a8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">상승 키워드</div>
      <div class="kw-cloud">
        <span class="kw-tag kw-gold">🏔️ 등산</span>
        <span class="kw-tag kw-gold">🎾 테니스</span>
        <span class="kw-tag kw-green">🏃 러닝</span>
        <span class="kw-tag kw-green">💪 건강관리</span>
        <span class="kw-tag kw-blue">🌅 아침루틴</span>
        <span class="kw-tag kw-blue">🎒 출근전</span>
        <span class="kw-tag kw-amber">⚡ 에너지부스터</span>
      </div>
    </div>
    <div>
      <div style="font-size:11px;color:#9090a8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">마케팅 시사점</div>
      <p style="font-size:13px;color:#4a4a5a;line-height:1.75;font-weight:300;">
        '건강기능식품'에서 <span style="color:#b8860b;font-weight:500">'액티브 라이프스타일 파트너'</span>로 포지셔닝 확장 가능성 포착.
        등산·테니스 커뮤니티 타겟 콘텐츠 마케팅을 통해 2030 브랜드 친화도 제고 기회.
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 04 · 전략 탭
# ════════════════════════════════════════════
st.markdown('<div class="sec-label">04 · 전략적 통찰 및 권고</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["핵심 인사이트", "기회·위험 매트릭스", "채널별 전략", "즉시 실행 Action"])

with tab1:
    insights = [
        ("🏙️","수도권·편의점 채널의 폭발적 성장","수도권 +15%는 MZ층의 편의점 채널 구매 행동 변화가 반영된 신호. 편의점 진열 위치 및 POS 마케팅 집중 투자로 모멘텀 유지 필요.","최우선","p-high"),
        ("🌿","지방 대형마트 채널 정체 대응","지방 -2%는 대형마트 의존도 과다의 결과. 지방 편의점망 확대 및 지역 헬스숍·약국 채널로의 분산을 통해 유통 리스크 완화가 시급.","중요","p-mid"),
        ("🎾","액티브 라이프 포지셔닝 전환 시점","등산·테니스 키워드 +30% 급증은 소비자가 스스로 브랜드를 재정의하고 있다는 신호. 이 흐름을 마케팅이 따라가거나 선도해야 할 결정적 시점.","최우선","p-high"),
        ("💸","가격 저항 선제 대응","가격 민감도 언급은 향후 대량 이탈 예고 신호일 수 있음. '가성비 소구'보다 '가치 소구' 전환 — 구독 혜택·멤버십 할인 등 락인 장치 필요.","중요","p-mid"),
        ("📦","패키지 완성도 보강","선물용 호평과 박스 개봉 불편이 공존. 겉 디자인은 성공했으나 기능적 UX는 미완성. 품질팀·패키지 디자인팀 공동 개선 TF 구성 권고.","검토","p-low"),
        ("🍵","맛 개선 자산화",'"쓴맛 감소"는 잠재 고객층을 실질적으로 넓힐 수 있는 산물. 광고 크리에이티브에서 전면 메시지화하여 홍삼 비경험자 유입 캠페인에 활용.',"검토","p-low"),
    ]
    rows = [insights[i:i+3] for i in range(0, len(insights), 3)]
    for row in rows:
        cols = st.columns(len(row), gap="small")
        for col, (icon, heading, body, priority, pcls) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="insight-card">
                  <div style="font-size:22px;margin-bottom:8px;">{icon}</div>
                  <div class="insight-heading">{heading}</div>
                  <div class="insight-body">{body}</div>
                  <div class="priority-badge {pcls}">● {priority}</div>
                </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown('<div style="font-size:10px;color:#9090a8;text-transform:uppercase;letter-spacing:0.1em;text-align:right;margin-bottom:6px;">← 영향 낮음 &nbsp;|&nbsp; 영향 높음 →</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2, gap="small")
    with m1:
        st.markdown('<div class="matrix-cell mc-star"><div class="mc-label mc-gold">⭐ 집중 공략 (고영향·고가능성)</div><div class="mc-body">편의점 채널 MZ 확대 · 액티브 라이프 포지셔닝 · 선물 수요 시즌 연동 · 쓴맛 개선 메시지 캠페인</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="matrix-cell mc-ques"><div class="mc-label mc-blue">🔵 면밀 검토 (고영향·저가능성)</div><div class="mc-body">지방 편의점 신규 진입 · 약국 채널 파트너십 · 가격 락인 구독 모델 도입 · 해외 MZ 타겟 수출 확대</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2, gap="small")
    with m3:
        st.markdown('<div class="matrix-cell mc-cash"><div class="mc-label mc-green">💚 즉시 실행 (저영향·고가능성)</div><div class="mc-body">박스 개봉부 구조 개선 · SNS 라이프스타일 콘텐츠 강화 · 리뷰 응답 고객 CS 피드백 루프 구축</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="matrix-cell mc-risk"><div class="mc-label mc-red">🔴 모니터링 (저영향·저가능성)</div><div class="mc-body">경쟁사 유사 리뉴얼 선점 · 대형마트 판촉비 증가 요구 · 원재료 가격 상승에 따른 추가 인상 압력</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#9090a8;text-transform:uppercase;letter-spacing:0.1em;text-align:center;margin-top:8px;">↑ 실행 용이 &nbsp;|&nbsp; 실행 어려움 ↓</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <table class="ch-table">
      <thead><tr><th>채널</th><th>현황</th><th>기회 포인트</th><th>단기 액션 (4주 내)</th><th>우선순위</th></tr></thead>
      <tbody>
        <tr><td><span class="ch-badge" style="background:rgba(30,122,80,0.09);color:#1e7a50;border:1px solid rgba(30,122,80,0.3)">편의점</span></td><td>수도권 +15% <span style="color:#1e7a50">강세</span></td><td>2030 출근 전 루틴 수요, 충동 구매 유발 가능성</td><td>계산대 옆 특화 진열 요청 · 스틱 번들 POP 소재 제작</td><td><span class="ch-badge" style="background:rgba(192,57,43,0.09);color:#c0392b">최우선</span></td></tr>
        <tr><td><span class="ch-badge" style="background:rgba(37,99,200,0.08);color:#2563c8;border:1px solid rgba(37,99,200,0.25)">온라인</span></td><td>성장세 유지 추정</td><td>정기구독 전환율 제고, 리뷰 마케팅 연동</td><td>네이버 스마트스토어 정기구독 패키지 출시 검토</td><td><span class="ch-badge" style="background:rgba(196,122,32,0.09);color:#c47a20">우선</span></td></tr>
        <tr><td><span class="ch-badge" style="background:rgba(192,57,43,0.08);color:#c0392b;border:1px solid rgba(192,57,43,0.25)">대형마트</span></td><td>지방 -2% <span style="color:#c0392b">정체</span></td><td>선물세트 기획전 연동, 대용량 번들 프로모션</td><td>점포별 담당MD와 4월 가정의 달 기획전 협의 착수</td><td><span class="ch-badge" style="background:rgba(196,122,32,0.09);color:#c47a20">우선</span></td></tr>
        <tr><td><span class="ch-badge" style="background:rgba(184,134,11,0.09);color:#9a6f20;border:1px solid rgba(184,134,11,0.3)">약국·헬스숍</span></td><td>미개발 채널</td><td>액티브 라이프스타일 소비자 접점, 전문가 신뢰도</td><td>약사·트레이너 대상 샘플 제공 파일럿 기획</td><td><span class="ch-badge" style="background:rgba(30,122,80,0.08);color:#1e7a50">검토</span></td></tr>
        <tr><td><span class="ch-badge" style="background:rgba(0,0,0,0.05);color:#4a4a5a;border:1px solid rgba(0,0,0,0.07)">스포츠 채널</span></td><td>신규 기회 감지</td><td>등산·테니스 동호회 협찬, 스포츠 앱 제휴</td><td>커뮤니티 매체(산악회 카페, 테니스 앱) 광고 단가 조사</td><td><span class="ch-badge" style="background:rgba(30,122,80,0.08);color:#1e7a50">검토</span></td></tr>
      </tbody>
    </table>""", unsafe_allow_html=True)

with tab4:
    actions = [
        ("01","편의점 채널 판촉 소재 즉시 제작",'수도권 +15% 모멘텀을 유지하기 위해 2주 내 편의점용 POP 소재 및 계산대 옆 진열 협의 완료.',[("D-14","at-red"),("마케팅팀","at-blue"),("영업팀 협업","at-gray")]),
        ("02","액티브 라이프 SNS 콘텐츠 캠페인 기획",'등산·테니스 키워드 +30% 급증 대응. 유튜브 쇼츠용 "운동 후 에브리타임" 브이로그형 콘텐츠 4월 중 런칭 목표.',[("D-21","at-red"),("디지털팀","at-blue"),("인플루언서 섭외","at-gray")]),
        ("03","박스 개봉 UX 품질팀 이슈 공유","리뷰 500건 중 반복 언급된 박스 개봉 불편 이슈를 품질팀에 공식 전달. 다음 생산 로트 전 개선 가능 여부 확인.",[("D-7","at-amber"),("품질팀 협업","at-blue"),("VOC 공식 이슈화","at-gray")]),
        ("04","가정의 달 선물 기획전 대형마트 MD 협의",'"선물용으로 좋다" 긍정 리뷰를 활용. 5월 가정의 달 전 대형마트 선물세트 기획전 입점 협의를 이달 내 완료.',[("D-30","at-amber"),("영업팀","at-blue"),("대형마트 MD","at-gray")]),
        ("05",'"쓴맛 감소" 크리에이티브 소구 적용','홍삼 비경험자 유입을 위한 "이제는 부담 없이" 컨셉 온라인 광고 소재 개발. A/B 테스트 진행.',[("D-45","at-green"),("광고팀","at-blue"),("A/B 테스트","at-gray")]),
    ]
    for num, title, desc, tags in actions:
        tag_html = "".join(f'<span class="action-tag {cls}">{label}</span>' for label, cls in tags)
        st.markdown(f"""
        <div class="action-item">
          <div class="action-num">{num}</div>
          <div>
            <div class="action-title">{title}</div>
            <div class="action-desc">{desc}</div>
            <div style="margin-top:8px;">{tag_html}</div>
          </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 팀장 코멘트
# ════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="comment-panel">
  <div style="display:flex;gap:16px;align-items:flex-start;">
    <div style="font-size:32px;flex-shrink:0;">💬</div>
    <div>
      <div class="comment-label">팀장 코멘트</div>
      <p class="comment-text">
        이번 주 데이터는 <strong style="color:#1a1a1a;font-weight:500">리뉴얼 전략이 수도권 MZ층에서 유효하게 작동</strong>하고 있음을 명확히 보여줍니다.
        단, 지방 채널 정체와 가격 저항이 동시에 감지되고 있어 채널 다변화와 가치 소구 전환을 서두르지 않으면 다음 분기 성장세가 꺾일 위험이 있습니다.
        <br><br>
        가장 주목해야 할 포인트는 <span style="color:#b8860b;font-weight:500">액티브 라이프스타일 키워드의 자발적 확산</span>입니다.
        4월 캠페인에서 이 흐름을 적극 선도하여 '홍삼=에너지 부스터' 브랜드 연상을 2030 세대에 공고히 할 것을 제안합니다.
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 풋터
# ════════════════════════════════════════════
st.markdown("""
<div class="page-footer">
  <span><b>KGC 인삼공사</b> · 브랜드전략실 마케팅팀 · 기밀 문서</span>
  <span>작성일 2026.03.31 · v2.0 (Google Sheets 연동)</span>
</div>
""", unsafe_allow_html=True)
