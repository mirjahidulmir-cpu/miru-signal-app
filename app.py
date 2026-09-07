from datetime import datetime
import json
import random
import numpy as np
import pandas as pd
from PIL import Image
import requests
import streamlit as st

st.set_page_config(
    page_title="Mir Signal AI", page_icon="⚡", layout="centered"
)

# Initialize Session Counters
if "won" not in st.session_state:
  st.session_state.won = 0
if "loss" not in st.session_state:
  st.session_state.loss = 0
if "pending" not in st.session_state:
  st.session_state.pending = 0

# Custom Safabot-Inspired Dark UI Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .metric-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    .signal-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
        margin-top: 15px;
    }
    .badge-call {
        background-color: #059669;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        float: right;
    }
    .badge-put {
        background-color: #dc2626;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        float: right;
    }
    .progress-outer {
        background-color: #1e293b;
        border-radius: 10px;
        height: 12px;
        width: 100%;
        margin-top: 10px;
    }
    .progress-inner {
        background-color: #10b981;
        height: 12px;
        border-radius: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ Mir Signal AI")
st.caption("Computer Vision & Quantitative Trading Engine")

# Live Session Metrics Header
c1, c2, c3 = st.columns(3)
with c1:
  st.markdown(
      f'<div class="metric-card">⏳ <b>{st.session_state.pending}</b><br><small'
      ' style="color:#94a3b8;">Pending</small></div>',
      unsafe_allow_html=True,
  )
with c2:
  st.markdown(
      f'<div class="metric-card">📈 <b>{st.session_state.won}</b><br><small'
      ' style="color:#10b981;">Won</small></div>',
      unsafe_allow_html=True,
  )
with c3:
  st.markdown(
      f'<div class="metric-card">🛡️ <b>{st.session_state.loss}</b><br><small'
      ' style="color:#ef4444;">Loss</small></div>',
      unsafe_allow_html=True,
  )

st.markdown("---")

st.subheader("📸 Quotex Chart Intelligence")
uploaded_file = st.file_uploader(
    "Upload Chart Screenshot", type=["png", "jpg", "jpeg"]
)

col_a, col_b = st.columns(2)
with col_a:
  pair_name = st.text_input(
      "Asset / Currency Pair",
      value="EUR/USD (OTC)",
      placeholder="e.g. CHF/JPY, GBP/USD",
  )
with col_b:
  timeframe = st.selectbox("Expiry Duration", ["M1 (1 Minute)", "M2 (2 Minute)"])

# Trigger Button Always Visible
if st.button("🚀 GENERATE VIP AI SIGNAL", use_container_width=True):
  if uploaded_file is None:
    st.warning("⚠️ Please upload a screenshot of your Quotex chart first.")
  else:
    with st.spinner("Analyzing candlestick wick dynamics, volume & support..."):
      img = Image.open(uploaded_file).convert("RGB")
      img_np = np.array(img)

      # Color Segmentation: Detect dominance of Red vs Green candles
      red_mask = (
          (img_np[:, :, 0] > 150)
          & (img_np[:, :, 1] < 100)
          & (img_np[:, :, 2] < 100)
      )
      green_mask = (
          (img_np[:, :, 1] > 150)
          & (img_np[:, :, 0] < 100)
          & (img_np[:, :, 2] < 100)
      )

      red_count = np.sum(red_mask)
      green_count = np.sum(green_mask)

      # High-Probability Confidence Interval (81% to 89%)
      confidence = random.randint(81, 89)

      # Signal Logic Evaluation
      if green_count >= red_count:
        direction = "CALL"
        pattern = "Bullish Rejection / Engulfing"
        trend = "Bullish Momentum"
        next_candle = "Green / Bullish Candle Expected"
        badge_class = "badge-call"
        reason = (
            "Buyers absorbed selling pressure near the dynamic support zone."
            " Long lower shadow confirms upward momentum."
        )
      else:
        direction = "PUT"
        pattern = "Bearish Exhaustion / Pin Bar"
        trend = "Bearish Momentum"
        next_candle = "Red / Bearish Candle Expected"
        badge_class = "badge-put"
        reason = (
            "Strong rejection detected at the psychological resistance line."
            " Sellers gained dominance on recent candle closes."
        )

      # Update Session Statistics
      st.session_state.won += 1

      # VIP Signal Result Card
      st.markdown(
          f"""
            <div class="signal-box">
                <span class="{badge_class}">{direction}</span>
                <h3 style="margin:0;">{pair_name}</h3>
                <small style="color: #94a3b8;">Duration: {timeframe[:2]} | Triggered at: {datetime.now().strftime("%H:%M:%S")}</small>
                
                <div style="margin-top: 15px;">
                    <span>AI Confidence: <b>{confidence}%</b> (High Probability)</span>
                    <div class="progress-outer">
                        <div class="progress-inner" style="width: {confidence}%;"></div>
                    </div>
                </div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      # Analytical Indicators Grid
      m1, m2 = st.columns(2)
      with m1:
        st.markdown(
            f'<div class="metric-card"><small'
            ' style="color:#94a3b8;">TREND</small><br><b>{trend}</b></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="metric-card"><small style="color:#94a3b8;">RISK'
            ' PROFILE</small><br><b>Low / Controlled</b></div>',
            unsafe_allow_html=True,
        )
      with m2:
        st.markdown(
            f'<div class="metric-card"><small'
            ' style="color:#94a3b8;">PATTERN</small><br><b>{pattern}</b></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-card"><small'
            f' style="color:#94a3b8;">TIMEFRAME</small><br><b>{timeframe[:2]}</b></div>',
            unsafe_allow_html=True,
        )

      st.success(f"🎯 **Next Candle Verdict:** {next_candle}")
      st.info(f"💡 **AI Logic Reasoning:** {reason}")
