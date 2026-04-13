import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- The rest of your code starts here ---
st.set_page_config(page_title="SRE-Life-Ops", layout="wide", page_icon="🛡️")

# --- RADIANT DARK THEME CSS ---
st.markdown("""
<style>
/* 🌌 Background */
.stApp {
    background: linear-gradient(135deg, #0a0f2c, #1a1f4d);
    color: #ffffff;
}

/* 📌 Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a0f2c;
    border-right: 2px solid #00e5ff;
}

/* 🔥 Sidebar Text FIX */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* 🎯 Labels (IMPORTANT FIX) */
label, .stWidgetLabel p {
    color: #ffffff !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* 🚀 Titles */
h1 {
    color: #00e5ff !important;
    font-size: 2.2rem !important;
}

h2, h3 {
    color: #00e5ff !important;
    font-weight: 700 !important;
}

/* 🧊 Card Style Sections */
.stCheckbox, .stTimeInput, .stNumberInput, .stSlider {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(0,229,255,0.2);
    margin-bottom: 20px;
}

/* 🔘 Buttons */
.stButton > button {
    background: #00e5ff !important;
    color: #000 !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    border: none !important;
}

/* 🔢 Inputs */
input {
    background-color: #111 !important;
    color: #00e5ff !important;
    border: 1px solid #00e5ff !important;
}

/* 📊 Metrics */
[data-testid="stMetricValue"] {
    color: #00e5ff !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- DATABASE LOGIC ---
USER_DB = "users.csv"
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_DB, index=False)

def login_user(user, pwd):
    df = pd.read_csv(USER_DB)
    return not df[(df['username'] == user) & (df['password'] == pwd)].empty

# --- AUTH STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- SIDEBAR ---
st.sidebar.title("🔐 Access Control")
user_input = st.sidebar.text_input("User ID")
pass_input = st.sidebar.text_input("Secret Key", type="password")

if st.sidebar.button("Sign In"):
    if login_user(user_input, pass_input):
        st.session_state.authenticated = True
        st.session_state.username = user_input
    else:
        st.sidebar.error("Invalid Credentials")

# --- MAIN DASHBOARD ---
if st.session_state.authenticated:
    st.title(f"🛡️ SRE-Life-Ops Dashboard | {st.session_state.username}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🕔 Availability")
        st.time_input("Wake up time")
        st.number_input("Water Intake (L)", 0.0, 10.0, 2.0)
    with col2:
        st.subheader("🏃 Physical Load")
        st.number_input("Steps", 0, 50000, 10000)
    with col3:
        st.subheader("⚙️ Resource Allocation")
        st.slider("Office Hours", 0, 12, 8)

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
else:
    st.title("🛡️ SRE-Pulse Engine")
    st.warning("Please sign in from the sidebar.")