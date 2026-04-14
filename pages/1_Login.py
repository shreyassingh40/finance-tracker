# 1_Login.py
# --------------------------------------------------------
# Login page for Personal Finance Tracker
# --------------------------------------------------------

import streamlit as st
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from streamlit_authenticator import Authenticate

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "auth_config.yaml"

with open(CONFIG_PATH, "r") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

st.title("🔐 Login")
st.subheader("💰 Personal Finance Tracker")
st.write("Sign in to manage your transactions and view financial insights.")

name, auth_status, username = authenticator.login(location="main")

col1, col2 = st.columns(2)

with col1:
    if st.button("Create Account"):
        st.switch_page("pages/2_Create_Account.py")

if auth_status is False:
    st.error("Incorrect username or password.")
elif auth_status is None:
    st.info("Please log in.")
else:
    st.success(f"Welcome back, {name}!")
    st.switch_page("pages/3_Dashboard.py")