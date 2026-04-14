# app.py
# --------------------------------------------------------
# Hidden app router for Personal Finance Tracker
# --------------------------------------------------------

import streamlit as st

st.set_page_config(
    page_title="Personal Finance Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

login_page = st.Page("pages/1_Login.py", title="Login", icon="🔐")
create_account_page = st.Page("pages/2_Create_Account.py", title="Create Account", icon="📝")
dashboard_page = st.Page("pages/3_Dashboard.py", title="Dashboard", icon="📊")
user_page = st.Page("pages/4_User.py", title="User", icon="👤")

pg = st.navigation(
    [login_page, create_account_page, dashboard_page, user_page],
    position="hidden"
)

pg.run()