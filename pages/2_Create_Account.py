# 2_Create_Account.py
# --------------------------------------------------------
# Create account page for Personal Finance Tracker
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

st.title("📝 Create Account")
st.subheader("💰 Personal Finance Tracker")

try:
    email, username, name = authenticator.register_user(pre_authorized=False)

    if email:
        with open(CONFIG_PATH, "w") as file:
            yaml.dump(config, file)

        st.success("Account created successfully!")
        if st.button("Go to Login"):
            st.switch_page("pages/1_Login.py")

except Exception as e:
    st.error(e)

if st.button("Back to Login"):
    st.switch_page("pages/1_Login.py")