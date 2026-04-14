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
    st.page_link("pages/4_User.py", label="User", icon="👤")

    st.divider()
    st.write(f"👤 **{name}**")
    st.caption(f"@{username}")

    authenticator.logout("Logout", "sidebar")

# LOAD PROFILE
PROFILE_PATH.parent.mkdir(exist_ok=True)

if PROFILE_PATH.exists():
    profiles = json.load(open(PROFILE_PATH))
else:
    profiles = {}

profile = profiles.get(username, {"name": name, "email": "", "bio": ""})

# STATS
df = load_data()

income = df[df["type"] == "income"]["amount"].sum() if not df.empty else 0
expense = df[df["type"] == "expense"]["amount"].sum() if not df.empty else 0

c1, c2 = st.columns(2)
c1.metric("Total Income", f"${income:.2f}")
c2.metric("Total Expenses", f"${expense:.2f}")

st.divider()

# PROFILE VIEW / EDIT
if "edit" not in st.session_state:
    st.session_state.edit = False

if not st.session_state.edit:
    st.title("👤 Profile")
    st.write(f"**Name:** {profile['name']}")
    st.write(f"**Email:** {profile['email']}")
    st.write(f"**Bio:** {profile['bio']}")

    if st.button("Edit"):
        st.session_state.edit = True
        st.rerun()
else:
    name_in = st.text_input("Name", value=profile["name"])
    email_in = st.text_input("Email", value=profile["email"])
    bio_in = st.text_area("Bio", value=profile["bio"])

    if st.button("Save"):
        profiles[username] = {
            "name": name_in,
            "email": email_in,
            "bio": bio_in
        }
        json.dump(profiles, open(PROFILE_PATH, "w"))
        st.session_state.edit = False
        st.success("Saved!")
        st.rerun()