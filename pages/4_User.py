# 4_User.py

import sys, os, json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

from src.analytics import load_data

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "auth_config.yaml"
PROFILE_PATH = ROOT_DIR / "data/user_profiles.json"

with open(CONFIG_PATH, "r") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

if st.session_state.get("authentication_status") is not True:
    st.warning("Please log in.")
    st.stop()

name = st.session_state.get("name", "User")
username = st.session_state.get("username", "")

# SIDEBAR
with st.sidebar:
    st.markdown("## 💰 Finance Tracker")
    st.caption("Track spending. Analyse trends. Save smarter.")
    st.divider()

    st.page_link("pages/3_Dashboard.py", label="Dashboard", icon="📊")

    st.divider()

    st.markdown("### 👤 Account")
    st.page_link(
        "pages/4_User.py",
        label=f"{name}",
        icon="👤"
    )

    st.divider()

    authenticator.logout("Logout", "sidebar")

# LOAD PROFILE
PROFILE_PATH.parent.mkdir(exist_ok=True)

if PROFILE_PATH.exists():
    profiles = json.load(open(PROFILE_PATH))
else:
    profiles = {}

profile = profiles.get(username, {"name": name, "email": "", "bio": ""})

    # PROFILE VIEW / EDIT
if "edit" not in st.session_state:
    st.session_state.edit = False

st.title("👤 Profile")

if not st.session_state.edit:
    st.write(f"**Name:** {profile['name']}")
    st.write(f"**Email:** {profile['email']}")
    st.write(f"**Bio:** {profile['bio']}")

    if st.button("Edit Profile"):
        st.session_state.edit = True
        st.rerun()
else:
    name_in = st.text_input("Name", value=profile["name"])
    email_in = st.text_input("Email", value=profile["email"])
    bio_in = st.text_area("Bio", value=profile["bio"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Changes"):
            profiles[username] = {
                "name": name_in,
                "email": email_in,
                "bio": bio_in
            }
            json.dump(profiles, open(PROFILE_PATH, "w"))
            st.session_state.edit = False
            st.success("Profile updated successfully!")
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.session_state.edit = False
            st.rerun()

st.divider()

# FINANCIAL OVERVIEW
st.subheader("📈 Financial Overview")

df = load_data()

income = df[df["type"] == "income"]["amount"].sum() if not df.empty else 0
expense = df[df["type"] == "expense"]["amount"].sum() if not df.empty else 0
net = income - expense
transaction_count = len(df) if not df.empty else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", transaction_count)
c2.metric("Total Income", f"${income:.2f}")
c3.metric("Total Expenses", f"${expense:.2f}")
c4.metric("Net Balance", f"${net:.2f}")