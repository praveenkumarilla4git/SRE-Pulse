import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="SRE-Life-Ops", layout="wide", page_icon="🛡️")

# --- RADIANT THEME CSS (UPDATED FOR HIGH VISIBILITY) ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0f2c, #1a1f4d); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #0a0f2c; border-right: 2px solid #00e5ff; }
    [data-testid="stSidebar"] * { color: #ffffff !important; font-weight: 600 !important; }
    label, .stWidgetLabel p { color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; }
    h1, h2, h3 { color: #00e5ff !important; font-family: 'Courier New', monospace; }
    
    /* TABLE VISIBILITY FIX */
    .stTable { 
        border: 1px solid rgba(0,229,255,0.3); 
        border-radius: 10px; 
        background-color: rgba(0,0,0,0.4) !important; 
    }
    
    /* Force habit names and dates to be white/cyan */
    .stTable td { color: #ffffff !important; font-weight: 600 !important; font-size: 1.1rem !important; }
    .stTable th { color: #00e5ff !important; font-weight: 800 !important; text-transform: uppercase; }
    
    /* Center the checkmarks and make them glow */
    .stTable td { text-align: center !important; text-shadow: 0 0 10px #00e5ff; }

    .stButton > button { background: #00e5ff !important; color: #000 !important; font-weight: bold !important; border-radius: 10px !important; }
    input { background-color: #111 !important; color: #00e5ff !important; border: 1px solid #00e5ff !important; }
</style>
""", unsafe_allow_html=True)

# --- DATABASE LOGIC ---
USER_DB = "users.csv"
TELEMETRY_DB = "habit_telemetry.csv"

# Initialize DBs
for db, cols in [(USER_DB, ["username", "password"]), (TELEMETRY_DB, ["Date", "Habit", "Status"])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

def login_user(user, pwd):
    df = pd.read_csv(USER_DB)
    return not df[(df['username'] == user) & (df['password'] == pwd)].empty

def log_habit(habit_name):
    today = datetime.now().strftime("%Y-%m-%d")
    df = pd.read_csv(TELEMETRY_DB)
    new_entry = pd.DataFrame([[today, habit_name, "✅"]], columns=["Date", "Habit", "Status"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(TELEMETRY_DB, index=False)

# --- AUTH STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- SIDEBAR ---
st.sidebar.title("🔐 Access Control")
u_input = st.sidebar.text_input("User ID")
p_input = st.sidebar.text_input("Secret Key", type="password")

if st.sidebar.button("Sign In"):
    if login_user(u_input, p_input):
        st.session_state.authenticated = True
        st.session_state.username = u_input
    else:
        st.sidebar.error("Invalid Credentials")

# --- MAIN DASHBOARD ---
if st.session_state.authenticated:
    st.title(f"🛡️ SRE-Life-Ops Dashboard | {st.session_state.username}")
    
    # --- LAYER 1: PROGRESS DONUTS ---
    st.subheader("📊 Weekly Reliability Progress")
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]
    vals = [50.0, 33.9, 35.7, 26.8, 0.0]
    clrs = ["#FFD700", "#1E90FF", "#FF4500", "#32CD32", "#808080"]
    
    donut_cols = st.columns(5)
    for i, col in enumerate(donut_cols):
        with col:
            fig = px.pie(values=[vals[i], 100-vals[i]], hole=0.7, color_discrete_sequence=[clrs[i], "rgba(255,255,255,0.1)"])
            fig.update_layout(showlegend=False, height=140, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown(f"<p style='text-align: center;'>{weeks[i]}<br><b>{vals[i]}%</b></p>", unsafe_allow_html=True)

    # --- LAYER 2: DYNAMIC HABIT GRID ---
    st.divider()
    st.subheader("🗓️ Monthly Discipline Heatmap")
    df_tele = pd.read_csv(TELEMETRY_DB)
    
    if not df_tele.empty:
        grid_view = df_tele.pivot_table(index='Habit', columns='Date', values='Status', aggfunc='first').fillna("⬜")
        st.table(grid_view)
    else:
        st.info("No telemetry logs found. Use the form below to start!")

    # --- LAYER 3: SUBMIT FORM ---
    st.divider()
    st.subheader("🚀 Log Production Activity")
    with st.form("habit_form", clear_on_submit=True):
        col_a, col_b = st.columns([2, 1])
        with col_a:
            habit_choice = st.selectbox("Select Habit", ["Exercise 3x/wk", "Water (3L)", "Clean Room", "Study Session", "Dog Walk"])
        with col_b:
            st.write("##")
            submit_btn = st.form_submit_button("Submit Telemetry")
            
        if submit_btn:
            log_habit(habit_choice)
            st.success("Telemetry Logged!")
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
else:
    st.title("🛡️ SRE-Pulse Engine")
    st.warning("Please sign in from the sidebar.")