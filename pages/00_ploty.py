import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="글로벌 시가총액 Top 10",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp { background: #0a0e1a; color: #e8eaf0; }

/* Sidebar background */
[data-testid="stSidebar"] > div:first-child {
    background-color: #0d1221;
    border-right: 1px solid #1e2740;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #c8cfe0 !important;
}
[data-testid="stSidebar"] .stSelectbox label { color: #c8cfe0 !important; }

/* Main area text */
.stMarkdown p { color: #c8cfe0; }

/* Metric card */
.mcard {
    background: #0f1628;
    border: 1px solid #1e2740;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.5rem;
}
.mcard-ticker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
}
.mcard-name  { font-size: 0.78rem; color: #8892b0; margin: 0.1rem 0 0.35rem; }
.mcard-price { font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 600; color: #e8eaf0; }
.mcard-pos   { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #43d9ad; }
.mcard-neg   { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #ff6b8a; }
.mcard-cap   { font-size: 0.72rem; color: #52607a; margin-top: 0.15rem; }

/* Section label */
.slabel {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3d52a0;
    margin-bottom: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Dashboard title */
.dash-title    { font-size: 1.85rem; font-weight: 700; color: #e8eaf0; letter-spacing: -0.02em; }
.dash-subtitle { font-size: 0.78rem; color: #52607a; font-family: 'JetBrains Mono', monospace; margin-top: 0.25rem; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
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
TICKER_LIST = list(TOP10.keys())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.divider()

    period_map = {
        "최근 1개월": "1mo",
        "최근 3개월": "3mo",
        "최근 6개월": "6mo",
        "최근 1년":   "1y",
        "최근 2년":   "2y",
    }
    period_label = st.selectbox("📅 기간 선택", list(period_map.keys()), index=3)
    period = period_map[period_label]

    chart_type = st.radio(
        "📊 차트 유형",
        ["정규화 수익률 (%)", "캔들스틱", "거래량 비교"],
    )

    st.divider()
    st.markdown("**종목 선택**")

    selected = {}
    for i, (ticker, name) in enumerate(TOP10.items()):
        dot = "🟢" if i % 3 == 0 else ("🔵" if i % 3 == 1 else "🟣")
        checked = st.checkbox(f"{dot} {ticker}  —  {name}", value=True, key=f"chk_{ticker}")
        if checked:
            selected[ticker] = name

    st.divider()
    st.markdown(
        "<p style='font-size:0.7rem;color:#52607a;font-family:JetBrains Mono,monospace;'>"
        "Data · Yahoo Finance<br>Streamlit + Plotly</p>",
        unsafe_allow_html=True,
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:1.2rem 0 1rem;border-bottom:1px solid #1e2740;margin-bottom:1.4rem;'>
  <div class='dash-title'>📈 글로벌 시가총액 Top 10</div>
  <div class='dash-subtitle'>GLOBAL MARKET CAP LEADERS · STOCK PERFORMANCE DASHBOARD</div>
</div>
""", unsafe_allow_html=True)

if not selected:
    st.warning("⚠️ 사이드바에서 최소 1개 종목을 선택해 주세요.")
    st.stop()

# ── Data fetch ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_close(tickers: tuple, period: str) -> pd.DataFrame:
    raw = yf.download(list(tickers), period=period, auto_adjust=True, progress=False)
    if raw.empty:
        return pd.DataFrame()
    if isinstance(raw.columns, pd.MultiIndex):
        close = raw["Close"]
        close.columns = close.columns.get_level_values(0)
    else:
        close = raw[["Close"]]
        close.columns = [tickers[0]]
    return close

@st.cache_data(ttl=300)
def fetch_ohlcv(ticker: str, period: str) -> pd.DataFrame:
    raw = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    return raw

@st.cache_data(ttl=60)
def fetch_info(ticker: str) -> dict:
    try:
        fi = yf.Ticker(ticker).fast_info
        return {"price": getattr(fi, "last_price", None),
                "mktcap": getattr(fi, "market_cap", None)}
    except Exception:
        return {"price": None, "mktcap": None}

with st.spinner("시장 데이터 불러오는 중…"):
    close_df = fetch_close(tuple(selected.keys()), period)

# Ensure columns match selected tickers
if close_df.empty:
    st.error("데이터를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")
    st.stop()

# ── Plotly base layout ────────────────────────────────────────────────────────
BASE_LAYOUT = dict(
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#0d1221",
    font=dict(family="Space Grotesk, sans-serif", color="#8892b0", size=12),
    xaxis=dict(gridcolor="#1a2035", zerolinecolor="#1a2035"),
    yaxis=dict(gridcolor="#1a2035", zerolinecolor="#1a2035"),
    legend=dict(
        bgcolor="#0f1628", bordercolor="#1e2740", borderwidth=1,
        font=dict(size=11), orientation="h", x=0, y=-0.14,
    ),
    hovermode="x unified",
    margin=dict(l=10, r=10, t=45, b=10),
)

def color_of(ticker: str) -> str:
    idx = TICKER_LIST.index(ticker) if ticker in TICKER_LIST else 0
    return COLORS[idx]

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown("<div class='slabel'>현재 시세</div>", unsafe_allow_html=True)
cols = st.columns(min(5, len(selected)))

for idx, (ticker, name) in enumerate(selected.items()):
    col = cols[idx % len(cols)]
    c = color_of(ticker)
    info = fetch_info(ticker)
    price = info["price"]
    mktcap = info["mktcap"]

    if ticker in close_df.columns:
        s = close_df[ticker].dropna()
        if len(s) >= 2:
            chg = (s.iloc[-1] / s.iloc[-2] - 1) * 100
            chg_str = f"{'▲' if chg >= 0 else '▼'} {abs(chg):.2f}%"
            chg_cls = "mcard-pos" if chg >= 0 else "mcard-neg"
        else:
            chg_str, chg_cls = "— %", "mcard-pos"
    else:
        chg_str, chg_cls = "— %", "mcard-pos"

    price_str = f"${price:,.2f}" if price else "—"
    if mktcap:
        cap_str = f"${mktcap/1e12:.2f}T" if mktcap >= 1e12 else f"${mktcap/1e9:.0f}B"
    else:
        cap_str = "—"

    col.markdown(f"""
    <div class='mcard'>
      <div class='mcard-ticker' style='color:{c};'>{ticker}</div>
      <div class='mcard-name'>{name}</div>
      <div class='mcard-price'>{price_str}</div>
      <div class='{chg_cls}'>{chg_str} &nbsp;(1일)</div>
      <div class='mcard-cap'>시총 {cap_str}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='slabel'>주가 퍼포먼스</div>", unsafe_allow_html=True)

# ── Chart: Normalised returns ─────────────────────────────────────────────────
if chart_type == "정규화 수익률 (%)":
    fig = go.Figure()
    for ticker in selected:
        if ticker not in close_df.columns:
            continue
        s = close_df[ticker].dropna()
        if s.empty:
            continue
        norm = (s / s.iloc[0] - 1) * 100
        fig.add_trace(go.Scatter(
            x=norm.index, y=norm.values,
            name=ticker,
            line=dict(color=color_of(ticker), width=2),
            hovertemplate=f"<b>{ticker}</b><br>%{{x|%Y-%m-%d}}<br>수익률: %{{y:.2f}}%<extra></extra>",
        ))
    fig.add_hline(y=0, line_dash="dot", line_color="#2a3555", line_width=1)
    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(text=f"정규화 수익률 — {period_label}", font=dict(size=14, color="#e8eaf0"), x=0.01),
        yaxis_title="수익률 (%)", height=520,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Chart: Candlestick ────────────────────────────────────────────────────────
elif chart_type == "캔들스틱":
    cand_ticker = st.selectbox("종목 선택", list(selected.keys()))
    ohlc = fetch_ohlcv(cand_ticker, period)
    if ohlc.empty:
        st.warning("OHLC 데이터 없음")
    else:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.75, 0.25], vertical_spacing=0.04)
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
            marker_color=color_of(cand_ticker), opacity=0.5, name="거래량",
        ), row=2, col=1)
        fig.update_layout(
            **BASE_LAYOUT,
            title=dict(text=f"{cand_ticker} — {TOP10.get(cand_ticker,'')} 캔들스틱 · {period_label}",
                       font=dict(size=14, color="#e8eaf0"), x=0.01),
            height=560, xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Chart: Volume ─────────────────────────────────────────────────────────────
elif chart_type == "거래량 비교":
    @st.cache_data(ttl=300)
    def fetch_volume(tickers: tuple, period: str) -> pd.DataFrame:
        raw = yf.download(list(tickers), period=period, auto_adjust=True, progress=False)
        if raw.empty:
            return pd.DataFrame()
        vol = raw["Volume"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Volume"]]
        if isinstance(vol.columns, pd.MultiIndex):
            vol.columns = vol.columns.get_level_values(0)
        return vol

    vol_df = fetch_volume(tuple(selected.keys()), period)
    fig = go.Figure()
    for ticker in selected:
        if ticker not in vol_df.columns:
            continue
        fig.add_trace(go.Bar(
            x=vol_df.index, y=vol_df[ticker],
            name=ticker, marker_color=color_of(ticker), opacity=0.75,
            hovertemplate=f"<b>{ticker}</b><br>%{{x|%Y-%m-%d}}<br>거래량: %{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(
        **BASE_LAYOUT, barmode="overlay",
        title=dict(text=f"거래량 비교 — {period_label}", font=dict(size=14, color="#e8eaf0"), x=0.01),
        yaxis_title="거래량", height=520,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Correlation heatmap ───────────────────────────────────────────────────────
avail = [t for t in selected if t in close_df.columns]
if len(avail) >= 2:
    st.divider()
    st.markdown("<div class='slabel'>수익률 상관관계</div>", unsafe_allow_html=True)
    corr = close_df[avail].pct_change().dropna().corr()
    fig_h = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0.0, "#ff6b8a"], [0.5, "#1a2035"], [1.0, "#43d9ad"]],
        zmin=-1, zmax=1,
        text=corr.round(2).values,
        texttemplate="%{text}",
        textfont=dict(size=11, family="JetBrains Mono"),
        hovertemplate="%{y} × %{x}<br>상관계수: %{z:.3f}<extra></extra>",
    ))
    fig_h.update_layout(
        **BASE_LAYOUT,
        title=dict(text=f"일간 수익률 상관계수 — {period_label}",
                   font=dict(size=14, color="#e8eaf0"), x=0.01),
        height=420,
    )
    st.plotly_chart(fig_h, use_container_width=True)

# ── Performance table ─────────────────────────────────────────────────────────
st.divider()
st.markdown("<div class='slabel'>기간 성과 요약</div>", unsafe_allow_html=True)

rows = []
for ticker in selected:
    if ticker not in close_df.columns:
        continue
    s = close_df[ticker].dropna()
    if len(s) < 2:
        continue
    total = (s.iloc[-1] / s.iloc[0] - 1) * 100
    vol_pct = s.pct_change().std() * (252 ** 0.5) * 100
    rows.append({
        "티커": ticker,
        "회사명": TOP10.get(ticker, ""),
        "기간 수익률": f"{total:+.2f}%",
        "52주 고가": f"${s.max():,.2f}",
        "52주 저가": f"${s.min():,.2f}",
        "연환산 변동성": f"{vol_pct:.1f}%",
    })

if rows:
    df_table = pd.DataFrame(rows).set_index("티커")
    st.dataframe(df_table, use_container_width=True, height=380)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:2rem 0 1rem;
     font-size:0.68rem;color:#2a3555;
     font-family:JetBrains Mono,monospace;letter-spacing:0.06em;'>
  DATA · YAHOO FINANCE · FOR INFORMATIONAL PURPOSES ONLY · NOT FINANCIAL ADVICE
</div>
""", unsafe_allow_html=True)
