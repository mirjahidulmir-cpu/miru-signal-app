from datetime import datetime
import ccxt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Mir Signal AI", page_icon="⚡", layout="centered"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .signal-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #30363d;
        text-align: center;
        margin-top: 10px;
    }
    .call-btn { color: #00ff88; font-size: 32px; font-weight: bold; }
    .put-btn { color: #ff3366; font-size: 32px; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ Mir Signal AI")
st.caption("High Precision Algorithmic VIP Engine")

pair = st.selectbox("Select Asset / Pair", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
timeframe = st.selectbox("Expiry Timeframe", ["1m", "2m"])


# ম্যানুয়াল RSI ক্যালকুলেশন ফাংশন
def calculate_rsi(series, period=14):
  delta = series.diff()
  gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
  loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
  rs = gain / loss
  return 100 - (100 / (1 + rs))


if st.button("🔍 SCAN MARKET NOW", use_container_width=True):
  with st.spinner("Analyzing Candlesticks & Technicals..."):
    try:
      exchange = ccxt.binance()
      bars = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=60)
      df = pd.DataFrame(
          bars, columns=["time", "open", "high", "low", "close", "volume"]
      )

      # টেকনিক্যাল হিসাব
      df["RSI"] = calculate_rsi(df["close"], 14)
      df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()

      last_close = df["close"].iloc[-1]
      last_rsi = df["RSI"].iloc[-1]
      ema = df["EMA_50"].iloc[-1]
      now = datetime.now().strftime("%H:%M:%S")

      if last_close > ema and last_rsi < 45:
        st.markdown(
            f"""
                <div class="signal-card">
                    <div class="call-btn">🟢 CALL / UP</div>
                    <h3>Asset: {pair} | Expiry: {timeframe}</h3>
                    <p>Entry Price: <b>${last_close}</b> | RSI: <b>{round(last_rsi, 1)}</b></p>
                    <p style="color: #00ff88;">Status: Strong Bullish Momentum</p>
                    <small>Generated at {now}</small>
                </div>
                """,
            unsafe_allow_html=True,
        )
      elif last_close < ema and last_rsi > 55:
        st.markdown(
            f"""
                <div class="signal-card">
                    <div class="put-btn">🔴 PUT / DOWN</div>
                    <h3>Asset: {pair} | Expiry: {timeframe}</h3>
                    <p>Entry Price: <b>${last_close}</b> | RSI: <b>{round(last_rsi, 1)}</b></p>
                    <p style="color: #ff3366;">Status: Strong Bearish Momentum</p>
                    <small>Generated at {now}</small>
                </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.warning(
            f"Market is Sideways (RSI: {round(last_rsi, 1)}). Wait for a clear"
            " reversal setup!"
        )
    except Exception as e:
      st.error(f"Error fetching data: {e}")
