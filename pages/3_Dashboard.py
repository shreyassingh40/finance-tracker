# 3_Dashboard.py
# --------------------------------------------------------
# Streamlit Dashboard for Personal Finance Tracker
# --------------------------------------------------------

import sys, os
from pathlib import Path
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import yaml
import plotly.express as px
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

from src.database import create_table, insert_transaction, fetch_transactions
from src.analytics import load_data, monthly_summary, category_breakdown

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

if st.session_state.get("authentication_status") is not True:
    st.warning("Please log in.")
    st.stop()

name = st.session_state.get("name", "User")
username = st.session_state.get("username", "")

# 🔥 SIDEBAR
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

# MAIN
st.title("📊 Dashboard")
st.write(f"Welcome back, **{name}**")

create_table()

# Add transaction
st.subheader("➕ Add Transaction")

with st.form("form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        t_date = st.date_input("Date", value=date.today())

    with c2:
        category = st.selectbox("Category", [
            "Food", "Transport", "Rent", "Entertainment",
            "Utilities", "Shopping", "Salary", "Health", "Other"
        ])

    with c3:
        t_type = st.selectbox("Type", ["expense", "income"])

    amount = st.number_input("Amount", min_value=0.0)
    desc = st.text_input("Description")

    if st.form_submit_button("Add"):
        if amount > 0:
            insert_transaction(username, str(t_date), category, t_type, amount, desc)
            st.success("Added!")

# Analytics
df = load_data(username)

if not df.empty:
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Income", f"${income:.2f}")
    m2.metric("Expenses", f"${expense:.2f}")
    m3.metric("Net", f"${income - expense:.2f}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Income vs Expense Trend")
        summary = monthly_summary(df)
        st.dataframe(summary, use_container_width=True)

        if not summary.empty:
            monthly_long = summary.melt(
                id_vars="month",
                var_name="Transaction Type",
                value_name="Amount"
            )

            fig_trend = px.line(
                monthly_long,
                x="month",
                y="Amount",
                color="Transaction Type",
                markers=True,
                title="Income and Expense Trends Over Time"
            )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        st.subheader("Expense Category Distribution")
        cats = category_breakdown(df)
        st.dataframe(cats, use_container_width=True)

        if not cats.empty:
            fig_donut = px.pie(
                cats,
                names="category",
                values="amount",
                hole=0.45,
                title="How Expenses Are Distributed Across Categories"
            )
            st.plotly_chart(fig_donut, use_container_width=True)