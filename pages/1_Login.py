# 1_Login.py
# --------------------------------------------------------
# Login page for Personal Finance Tracker
# --------------------------------------------------------

import streamlit as st
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Login | Personal Finance Tracker", layout="centered")

# --- Load config from project root ---
ROOT_DIR = Path(__file__).resolve().parent
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
    st.info("Open the Dashboard page from the sidebar.")