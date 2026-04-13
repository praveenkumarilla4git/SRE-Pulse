import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="SRE-Life-Ops", layout="wide", page_icon="🛡️")

# --- RADIANT DARK THEME CSS ---
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(26, 26, 46, 0.95);
        border-right: 2px solid #00d4ff;
    }

    /* Titles and Subheaders Neon Effect */
    h1, h2, h3 {
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        font-family: 'Courier New', Courier, monospace;
    }

    /* Glowing Metrics */
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
        font-weight: bold;
    }

    /* Radiant Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #005f73) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 2rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5) !important;
    }

    /* Cards/Containers */
    .stCheckbox, .stTimeInput, .stNumberInput, .stSlider {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(0, 212, 255, 0.1);
        margin-bottom: 10px;
    }

    /* Input text color */
    input {
        color: #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATABASE (CSV) ---
USER_DB = "users.csv"

if not os.path.exists(USER_DB):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_DB, index=False)

def register_user(user, pwd):
    df = pd.read_csv(USER_DB)
    if user in df['username'].values:
        return False
    new_user = pd.DataFrame([[user, pwd]], columns=["username", "password"])
    new_user.to_csv(USER_DB, mode='a', header=False, index=False)
    return True

def login_user(user, pwd):
    df = pd.read_csv(USER_DB)
    return not df[(df['username'] == user) & (df['password'] == pwd)].empty

# --- SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- SIDEBAR AUTH ---
st.sidebar.title("🔐 Access Control")
auth_mode = st.sidebar.radio("Mode", ["Login", "Register"])
user_input = st.sidebar.text_input("User ID")
pass_input = st.sidebar.text_input("Secret Key", type="password")

if auth_mode == "Register":
    if st.sidebar.button("Create Account"):
        if register_user(user_input, pass_input):
            st.sidebar.success("Account Created! Switch to Login.")
        else:
            st.sidebar.error("User already exists.")

elif auth_mode == "Login":
    if st.sidebar.button("Sign In"):
        if login_user(user_input, pass_input):
            st.session_state.authenticated = True
            st.session_state.username = user_input
        else:
            st.sidebar.error("Invalid Credentials")

# --- MAIN APP (ONLY AFTER LOGIN) ---
if st.session_state.authenticated:

    st.title(f"🛡️ SRE-Life-Ops Dashboard | User: {st.session_state.username}")
    st.markdown("### SLIs (Service Level Indicators) for Personal Performance")

    # --- TELEMETRY INPUT ---
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🕔 Availability")
            wake_time = st.time_input("Wake up time", datetime.strptime("06:00", "%H:%M"))
            water = st.number_input("Water Intake (Liters)", min_value=0.0, max_value=10.0, step=0.5)

        with col2:
            st.subheader("🏃 Physical Load")
            steps = st.number_input("Step Count", min_value=0, step=100)
            weight = st.number_input("Morning Weight (kg)", min_value=30.0, step=0.1)

        with col3:
            st.subheader("⚙️ Resource Allocation")
            office_hrs = st.slider("Office Hours", 0, 12, 8)
            dev_hrs = st.slider("Project/Study Hours", 0, 8, 1)

    # --- ACTIVITY LOG ---
    st.divider()
    st.subheader("🏋️ Activity Log")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        crunches = st.checkbox("Crunches (25 * 2 sets)")
    with c_col2:
        walking = st.checkbox("Evening Walk (30 mins)")

    # --- REPORT & ALERT SYSTEM ---
    st.divider()
    if st.button("Generate Production Report"):

        alerts = []

        if water < 2:
            alerts.append("⚠️ Low hydration detected")

        if steps < 5000:
            alerts.append("⚠️ Low activity level")

        if dev_hrs < 1:
            alerts.append("⚠️ No self-development time")

        st.write("### 📝 Daily Status Summary")

        summary = f"""
        - **Wake-up Time:** {wake_time}
        - **Water Intake:** {water}L
        - **Steps:** {steps}
        - **Office Hours:** {office_hrs}
        - **Dev Hours:** {dev_hrs}
        - **Weight:** {weight}kg
        - **Crunches:** {"Done" if crunches else "Pending"}
        - **Walking:** {"Done" if walking else "Pending"}
        """

        st.info(summary)

        # --- ALERT DISPLAY ---
        if alerts:
            st.error("🚨 Alerts Detected")
            for alert in alerts:
                st.write(alert)
        else:
            st.success("✅ System Healthy")

    # --- METRICS ---
    st.divider()
    st.metric(label="Uptime Streak", value="12 Days", delta="2 Days")

    # --- LOGOUT ---
    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- IF NOT LOGGED IN ---
else:
    st.title("🛡️ Self-Healing Discipline Engine")
    st.warning("Please Login or Register from the sidebar to access your Telemetry.")
    st.image(
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000",
        caption="Secure Life-Ops Access"
    )