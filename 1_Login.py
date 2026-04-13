import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

# Load YAML config
with open("auth_config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# Login page layout
st.title("🔐 Login to Finance Tracker")
st.write("Please log in to continue.")

name, auth_status, username = authenticator.login(location="main")

if auth_status is False:
    st.error("Incorrect username or password.")
elif auth_status is None:
    st.warning("Please enter your credentials.")
else:
    st.success(f"Welcome back, {name}! Redirecting...")
    st.switch_page("pages/3_Dashboard.py")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🆕 Create an Account"):
        st.switch_page("pages/2_Create_Account.py")
with col2:
    if st.button("❓ Forgot Password"):
        st.info("Forgot password functionality coming soon...")
