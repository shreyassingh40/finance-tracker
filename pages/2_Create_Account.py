# 2_Create_Account.py
# --------------------------------------------------------
# Create account page for Personal Finance Tracker
# --------------------------------------------------------

import streamlit as st
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Create Account | Personal Finance Tracker", layout="centered")

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

# --- Page UI ---
st.title("📝 Create Account")
st.write("Create a new account for the Personal Finance Tracker.")

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
        pre_authorized=False
    )

    if email_of_registered_user:
        st.success("User registered successfully.")

        # Save updated config back to file
        with open(CONFIG_PATH, "w") as file:
            yaml.dump(config, file, default_flow_style=False)

except Exception as e:
    st.error(f"Error: {e}")
