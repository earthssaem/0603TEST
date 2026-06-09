import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Top 10 Market Cap Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Background */
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1221;
    border-right: 1px solid #1e2740;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #8892b0;
}

/* Header */
.dash-header {
    padding: 1.5rem 0 1rem 0;
    border-bottom: 1px solid #1e2740;
    margin-bottom: 1.5rem;
}
.dash-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #e8eaf0;
    letter-spacing: -0.02em;
    line-height: 1.15;
}
.dash-subtitle {
    font-size: 0.85rem;
    color: #52607a;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.3rem;
    letter-spacing: 0.04em;
}

/* Metric cards */
.metric-card {
    background: #0f1628;
    border: 1px solid #1e2740;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #3d52a0; }
.metric-ticker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    color: #5e7ce0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.metric-name {
    font-size: 0.82rem;
    color: #8892b0;
    margin: 0.1rem 0 0.4rem 0;
}
.metric-price {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e8eaf0;
    font-family: 'JetBrains Mono', monospace;
}
.metric-change-pos {
    font-size: 0.82rem;
    color: #43d9ad;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}
.metric-change-neg {
    font-size: 0.82rem;
    color: #ff6b8a;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}
.metric-cap {
    font-size: 0.75rem;
    color: #52607a;
    margin-top: 0.2rem;
}

/* Section labels */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3d52a0;
    margin-bottom: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Divider */
hr { border-color: #1e2740; }

/* Streamlit default overrides */
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
TOP10 = {
    "AAPL":  "Apple",
    "MSFT":  "Microsoft",
    "NVDA":  "NVIDIA",
    "AMZN":  "Amazon",
    "GOOGL": "Alphabet",
    "META":  "Meta",
    "TSLA":  "Tesla",
    "AVGO":  "Broadcom",
    "BRK-B": "Berkshire",
    "TSM":   "TSMC",
}

COLORS = [
    "#5e7ce0", "#43d9ad", "#ff6b8a", "#ffd166", "#a78bfa",
    "#38bdf8", "#fb923c", "#86efac", "#f472b6", "#67e8f9",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.markdown("---")

    period_map = {
        "최근 1개월": "1mo",
        "최근 3개월": "3mo",
        "최근 6개월": "6mo",
        "최근 1년": "1y",
        "최근 2년": "2y",
    }
    period_label = st.selectbox("기간 선택", list(period_map.keys()), index=3)
    period = period_map[period_label]

    chart_type = st.radio("차트 유형", ["정규화 수익률 (%)", "캔들스틱", "거래량"])

    st.markdown("---")
    st.markdown("**종목 선택**")
    selected = {}
    for i, (ticker, name) in enumerate(TOP10.items()):
        color = COLORS[i]
        checked = st.checkbox(
            f":{color[1:]}[■] {ticker} — {name}",
            value=True,
            key=ticker,
        )
        if checked:
            selected[ticker] = name

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.72rem;color:#52607a;font-family:JetBrains Mono,monospace;'>"
        "Data · Yahoo Finance<br>Powered by Streamlit + Plotly</p>",
        unsafe_allow_html=True,
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='dash-header'>
  <div class='dash-title'>글로벌 시가총액 Top 10</div>
  <div class='dash-subtitle'>GLOBAL MARKET CAP LEADERS · STOCK PERFORMANCE DASHBOARD</div>
</div>
""", unsafe_allow_html=True)

if not selected:
    st.warning("사이드바에서 최소 1개 이상의 종목을 선택하세요.")
    st.stop()

# ── Data fetch ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_data(tickers, period):
    raw = yf.download(list(tickers), period=period, auto_adjust=True, progress=False)
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    return close

@st.cache_data(ttl=300)
def fetch_info(ticker):
    try:
        info = yf.Ticker(ticker).fast_info
        return {
            "price": getattr(info, "last_price", None),
            "mktcap": getattr(info, "market_cap", None),
        }
    except Exception:
        return {"price": None, "mktcap": None}

with st.spinner("시장 데이터 불러오는 중…"):
    close_df = fetch_data(tuple(selected.keys()), period)
    # Flatten single-ticker MultiIndex
    if isinstance(close_df.columns, pd.MultiIndex):
        close_df.columns = close_df.columns.get_level_values(1)

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>현재 시세</div>", unsafe_allow_html=True)
cols = st.columns(min(5, len(selected)))

for idx, (ticker, name) in enumerate(selected.items()):
    col = cols[idx % len(cols)]
    color = COLORS[list(TOP10.keys()).index(ticker)]

    info = fetch_info(ticker)
    price = info["price"]
    mktcap = info["mktcap"]

    # 1-day change from close_df
    if ticker in close_df.columns and len(close_df[ticker].dropna()) >= 2:
        series = close_df[ticker].dropna()
        chg = (series.iloc[-1] / series.iloc[-2] - 1) * 100
        chg_str = f"{'▲' if chg >= 0 else '▼'} {abs(chg):.2f}%"
        chg_class = "metric-change-pos" if chg >= 0 else "metric-change-neg"
    else:
        chg_str, chg_class = "—", "metric-change-pos"

    price_str = f"${price:,.2f}" if price else "—"
    cap_str = f"${mktcap/1e12:.2f}T" if mktcap and mktcap >= 1e12 else (
              f"${mktcap/1e9:.0f}B" if mktcap else "—")

    col.markdown(f"""
    <div class='metric-card'>
      <div class='metric-ticker' style='color:{color};'>{ticker}</div>
      <div class='metric-name'>{name}</div>
      <div class='metric-price'>{price_str}</div>
      <div class='{chg_class}'>{chg_str} (1일)</div>
      <div class='metric-cap'>시총 {cap_str}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main chart ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>주가 퍼포먼스</div>", unsafe_allow_html=True)

plotly_template = dict(
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#0d1221",
    font=dict(family="Space Grotesk, sans-serif", color="#8892b0", size=12),
    xaxis=dict(gridcolor="#1a2035", zerolinecolor="#1a2035", showgrid=True),
    yaxis=dict(gridcolor="#1a2035", zerolinecolor="#1a2035", showgrid=True),
    legend=dict(
        bgcolor="#0f1628", bordercolor="#1e2740", borderwidth=1,
        font=dict(size=11), orientation="h",
        x=0, y=-0.12,
    ),
    hovermode="x unified",
    margin=dict(l=10, r=10, t=40, b=10),
)

# ── Chart: Normalised returns ─────────────────────────────────────────────────
if chart_type == "정규화 수익률 (%)":
    fig = go.Figure()
    for idx, (ticker, name) in enumerate(selected.items()):
        if ticker not in close_df.columns:
            continue
        series = close_df[ticker].dropna()
        if series.empty:
            continue
        norm = (series / series.iloc[0] - 1) * 100
        color = COLORS[list(TOP10.keys()).index(ticker)]
        fig.add_trace(go.Scatter(
            x=norm.index, y=norm.values,
            name=f"{ticker}",
            line=dict(color=color, width=2),
            hovertemplate=f"<b>{ticker}</b><br>%{{x|%Y-%m-%d}}<br>수익률: %{{y:.2f}}%<extra></extra>",
        ))

    fig.add_hline(y=0, line_dash="dot", line_color="#2a3555", line_width=1)
    fig.update_layout(
        **plotly_template,
        title=dict(
            text=f"정규화 수익률 — {period_label}",
            font=dict(size=14, color="#e8eaf0"), x=0.01,
        ),
        yaxis_title="수익률 (%)",
        height=520,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Chart: Candlestick (single ticker) ───────────────────────────────────────
elif chart_type == "캔들스틱":
    cand_ticker = st.selectbox("종목 선택", list(selected.keys()))

    @st.cache_data(ttl=300)
    def fetch_ohlc(ticker, period):
        return yf.download(ticker, period=period, auto_adjust=True, progress=False)

    ohlc = fetch_ohlc(cand_ticker, period)
    if ohlc.empty:
        st.warning("데이터 없음")
    else:
        if isinstance(ohlc.columns, pd.MultiIndex):
            ohlc.columns = ohlc.columns.get_level_values(0)

        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            row_heights=[0.75, 0.25], vertical_spacing=0.04,
        )
        color = COLORS[list(TOP10.keys()).index(cand_ticker)]
        fig.add_trace(go.Candlestick(
            x=ohlc.index,
            open=ohlc["Open"], high=ohlc["High"],
            low=ohlc["Low"],   close=ohlc["Close"],
            increasing_line_color="#43d9ad",
            decreasing_line_color="#ff6b8a",
            name=cand_ticker,
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=ohlc.index, y=ohlc["Volume"],
            marker_color=color, opacity=0.5, name="거래량",
        ), row=2, col=1)

        fig.update_layout(
            **plotly_template,
            title=dict(
                text=f"{cand_ticker} — {TOP10.get(cand_ticker,'')} 캔들스틱 · {period_label}",
                font=dict(size=14, color="#e8eaf0"), x=0.01,
            ),
            height=560, xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Chart: Volume comparison ──────────────────────────────────────────────────
elif chart_type == "거래량":
    @st.cache_data(ttl=300)
    def fetch_volume(tickers, period):
        raw = yf.download(list(tickers), period=period, auto_adjust=True, progress=False)
        vol = raw["Volume"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Volume"]]
        if isinstance(vol.columns, pd.MultiIndex):
            vol.columns = vol.columns.get_level_values(1)
        return vol

    vol_df = fetch_volume(tuple(selected.keys()), period)
    fig = go.Figure()
    for idx, (ticker, name) in enumerate(selected.items()):
        if ticker not in vol_df.columns:
            continue
        color = COLORS[list(TOP10.keys()).index(ticker)]
        fig.add_trace(go.Bar(
            x=vol_df.index, y=vol_df[ticker],
            name=ticker, marker_color=color, opacity=0.8,
            hovertemplate=f"<b>{ticker}</b><br>%{{x|%Y-%m-%d}}<br>거래량: %{{y:,.0f}}<extra></extra>",
        ))

    fig.update_layout(
        **plotly_template,
        barmode="overlay",
        title=dict(
            text=f"거래량 비교 — {period_label}",
            font=dict(size=14, color="#e8eaf0"), x=0.01,
        ),
        yaxis_title="거래량",
        height=520,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Correlation heatmap ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-label'>수익률 상관관계</div>", unsafe_allow_html=True)

avail = [t for t in selected if t in close_df.columns]
if len(avail) >= 2:
    returns = close_df[avail].pct_change().dropna()
    corr = returns.corr()

    fig_corr = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns, y=corr.index,
        colorscale=[
            [0.0,  "#ff6b8a"], [0.5, "#1a2035"], [1.0, "#43d9ad"],
        ],
        zmin=-1, zmax=1,
        text=corr.round(2).values,
        texttemplate="%{text}",
        textfont=dict(size=11, family="JetBrains Mono"),
        hovertemplate="%{y} × %{x}<br>상관계수: %{z:.3f}<extra></extra>",
    ))
    fig_corr.update_layout(
        **plotly_template,
        title=dict(
            text=f"일간 수익률 상관계수 — {period_label}",
            font=dict(size=14, color="#e8eaf0"), x=0.01,
        ),
        height=420,
        xaxis=dict(side="bottom"),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ── Performance table ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-label'>기간 성과 요약</div>", unsafe_allow_html=True)

rows = []
for ticker in selected:
    if ticker not in close_df.columns:
        continue
    s = close_df[ticker].dropna()
    if len(s) < 2:
        continue
    total = (s.iloc[-1] / s.iloc[0] - 1) * 100
    high, low = s.max(), s.min()
    vol_pct = s.pct_change().std() * (252 ** 0.5) * 100
    rows.append({
        "티커": ticker,
        "회사": TOP10.get(ticker, ""),
        "기간 수익률": f"{total:+.2f}%",
        "52주 고가": f"${high:,.2f}",
        "52주 저가": f"${low:,.2f}",
        "연환산 변동성": f"{vol_pct:.1f}%",
    })

if rows:
    df_table = pd.DataFrame(rows).set_index("티커")
    st.dataframe(df_table, use_container_width=True, height=360)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem 0;
     font-size:0.72rem; color:#2a3555;
     font-family: JetBrains Mono, monospace; letter-spacing:0.06em;'>
  DATA SOURCED FROM YAHOO FINANCE · FOR INFORMATIONAL PURPOSES ONLY<br>
  NOT FINANCIAL ADVICE · © 2025 STOCK DASHBOARD
</div>
""", unsafe_allow_html=True)
