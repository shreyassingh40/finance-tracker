# 1_Login.py
# --------------------------------------------------------
# Login page for Personal Finance Tracker
# --------------------------------------------------------

import streamlit as st
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from streamlit_authenticator import Authenticate
from pathlib import Path

st.set_page_config(
    page_title="Login | Personal Finance Tracker",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Load config from project root ---
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "auth_config.yaml"

with open(CONFIG_PATH, "r") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- Create authenticator ---
authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# --- Optional sidebar on login page ---
with st.sidebar:
    st.markdown("## 💰 Finance Tracker")
    st.caption("Track spending. Analyse trends. Save smarter.")
    st.divider()
    st.info("Please log in to continue.")

# --- Page UI ---
st.title("🔐 Login")
st.subheader("💰 Personal Finance Tracker")
st.write("Sign in to manage your transactions and view financial insights.")

# --- Login widget ---
name, auth_status, username = authenticator.login(location="main")

if auth_status is False:
    st.error("Username or password is incorrect.")
elif auth_status is None:
    st.info("Please enter your username and password.")
else:
    st.success(f"Welcome back, {name}!")
    st.switch_page("pages/3_Dashboard.py")