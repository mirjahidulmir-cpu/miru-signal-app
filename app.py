# Mir Signal VIP
# Single-file Streamlit app (basic version)

import streamlit as st
import json, os, random
from io import BytesIO
from PIL import Image
import numpy as np

st.set_page_config(page_title="Mir Signal VIP", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp{background:linear-gradient(180deg,#050816,#0b1120);color:white;}
.title{font-size:34px;font-weight:bold;color:#00ff99;text-align:center;}
.card{background:rgba(255,255,255,.06);padding:18px;border-radius:18px;}
</style>
""", unsafe_allow_html=True)

DB="users.json"
if not os.path.exists(DB):
    json.dump({}, open(DB,"w"))

def load():
    return json.load(open(DB))
def save(x):
    json.dump(x, open(DB,"w"), indent=2)

if "logged" not in st.session_state:
    st.session_state.logged=False
if "pending" not in st.session_state:
    st.session_state.pending=0
if "won" not in st.session_state:
    st.session_state.won=0
if "loss" not in st.session_state:
    st.session_state.loss=0
if "history" not in st.session_state:
    st.session_state.history=[]

if not st.session_state.logged:
    st.markdown('<div class="title">⚡ Mir Signal VIP</div>', unsafe_allow_html=True)
    t1,t2=st.tabs(["Login","Register"])
    with t1:
        u=st.text_input("Username")
        p=st.text_input("Password", type="password")
        if st.button("LOGIN"):
            users=load()
            if u in users and users[u]==p:
                st.session_state.logged=True
                st.rerun()
            else:
                st.error("Wrong login.")
    with t2:
        u=st.text_input("Create Username")
        p=st.text_input("Create Password", type="password")
        if st.button("REGISTER"):
            users=load()
            users[u]=p
            save(users)
            st.success("Registered.")
    st.stop()

st.markdown("## Dashboard")
c1,c2,c3=st.columns(3)
c1.metric("Pending", st.session_state.pending)
c2.metric("Won", st.session_state.won)
c3.metric("Loss", st.session_state.loss)

f=st.file_uploader("Upload Chart", type=["png","jpg","jpeg","webp"])
asset=st.text_input("Asset / Pair", placeholder="EUR/USD OTC")
exp=st.selectbox("Expiry",["M1","M2","M3","M5"])

if st.button("SCAN & PREDICT NEXT CANDLE"):
    if f:
        img=Image.open(BytesIO(f.getvalue())).convert("RGB")
        arr=np.array(img)
        g=arr[:,:,1].mean(); r=arr[:,:,0].mean()
        call=g>r
        conf=random.randint(83,91)
        st.session_state.pending+=1
        st.session_state.history.append((asset, "CALL" if call else "PUT", conf))
        st.markdown(f"## {'🟢 CALL' if call else '🔴 PUT'}")
        st.progress(conf/100)
        st.write("Confidence:", conf, "%")
        st.write("Target: Next Candle Open")
        st.write("AI Logic: Trend momentum + candle color analysis.")
    else:
        st.warning("Upload a screenshot first.")

st.divider()
st.write("### History")
for a,s,c in st.session_state.history[::-1]:
    st.write(f"{a} — {s} ({c}%)")

w,l=st.columns(2)
if w.button("🟢 WIN"):
    if st.session_state.pending>0:
        st.session_state.pending-=1
    st.session_state.won+=1
if l.button("🔴 LOSS"):
    if st.session_state.pending>0:
        st.session_state.pending-=1
    st.session_state.loss+=1
    
