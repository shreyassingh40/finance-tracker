# 3_Dashboard.py

# --------------------------------------------------------
# Personal Finance Tracker Dashboard
# This page handles:
# - Adding transactions
# - Displaying analytics
# - Visualising spending patterns
# --------------------------------------------------------

import sys
import os
from pathlib import Path
from datetime import date

# Allow imports from parent folder (src/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import yaml
import plotly.express as px
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

# Custom modules
from src.database import create_table, insert_transaction, fetch_transactions
from src.analytics import load_data, monthly_summary, category_breakdown

# Load authentication config
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "auth_config.yaml"

with open(CONFIG_PATH, "r") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialise authenticator
authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# Stop access if user is not logged in
if st.session_state.get("authentication_status") is not True:
    st.warning("Please log in.")
    st.stop()

# Retrieve logged-in user details
name = st.session_state.get("name", "User")
username = st.session_state.get("username", "")

# --------------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------------
with st.sidebar:
    st.markdown("## 💰 Finance Tracker")
    st.caption("Track spending. Analyse trends. Save smarter.")
    st.divider()

    # Navigation links
    st.page_link("pages/3_Dashboard.py", label="Dashboard", icon="📊")

    st.divider()

    # Account section
    st.markdown("### 👤 Account")
    st.page_link("pages/4_User.py", label=f"{name}", icon="👤")

    st.divider()

    # Logout button
    authenticator.logout("Logout", "sidebar")

# --------------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------------
st.title("📊 Dashboard")
st.write(f"Welcome back, **{name}**")

# Ensure database exists
create_table()

# --------------------------------------------------------
# ADD TRANSACTION FORM
# --------------------------------------------------------
st.subheader("➕ Add Transaction")

with st.form("form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        t_date = st.date_input("Date", value=date.today())

    with c2:
        category = st.selectbox(
            "Category",
            [
                "Food", "Transport", "Rent", "Entertainment",
                "Utilities", "Shopping", "Salary", "Health",
                "Education", "Other"
            ]
        )

    with c3:
        t_type = st.selectbox("Type", ["expense", "income"])

    amount = st.number_input("Amount", min_value=0.0)
    desc = st.text_input("Description")

    # Insert into DB when submitted
    if st.form_submit_button("Add"):
        if amount > 0:
            insert_transaction(username, str(t_date), category, t_type, amount, desc)
            st.success("Added!")

# --------------------------------------------------------
# LOAD USER DATA
# --------------------------------------------------------
df = load_data(username)

# Only show analytics if data exists
if not df.empty:

    # Basic financial calculations
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    net = income - expense
    transaction_count = len(df)

    # --------------------------------------------------------
    # TOP METRICS
    # --------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Income", f"${income:.2f}")
    m2.metric("Expenses", f"${expense:.2f}")
    m3.metric("Net Balance", f"${net:.2f}")
    m4.metric("Transactions", transaction_count)

    st.divider()

    # --------------------------------------------------------
    # NET BALANCE OVER TIME (Monthly)
    # --------------------------------------------------------
    st.subheader("📈 Net Balance Over Time")

    net_df = df.copy()
    net_df["month"] = net_df["date"].dt.to_period("M").astype(str)

    # Aggregate income and expenses per month
    monthly_income = net_df[net_df["type"] == "income"].groupby("month")["amount"].sum()
    monthly_expense = net_df[net_df["type"] == "expense"].groupby("month")["amount"].sum()

    # Calculate net balance
    monthly_net = monthly_income.subtract(monthly_expense, fill_value=0).reset_index()
    monthly_net.columns = ["month", "net_balance"]

    fig_net = px.bar(
        monthly_net,
        x="month",
        y="net_balance",
        title="Monthly Net Balance"
    )
    st.plotly_chart(fig_net, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # MAIN ANALYSIS (Trend + Distribution)
    # --------------------------------------------------------
    col1, col2 = st.columns(2)

    # Time series trend
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
                markers=True
            )
            st.plotly_chart(fig_trend, use_container_width=True)

    # Category distribution
    with col2:
        st.subheader("Expense Category Distribution")

        cats = category_breakdown(df)
        st.dataframe(cats, use_container_width=True)

        if not cats.empty:
            fig_donut = px.pie(
                cats,
                names="category",
                values="amount",
                hole=0.4
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # BEHAVIOURAL ANALYSIS
    # --------------------------------------------------------
    expense_df = df[df["type"] == "expense"].copy()

    # Average spending
    st.subheader("📊 Average Expense per Transaction by Category")

    if not expense_df.empty:
        avg_category_spend = (
            expense_df.groupby("category", as_index=False)["amount"]
            .mean()
            .sort_values("amount", ascending=False)
        )

        fig_avg = px.bar(avg_category_spend, x="category", y="amount")
        st.plotly_chart(fig_avg, use_container_width=True)

    # Transaction frequency
    st.subheader("🧾 Transaction Frequency by Category")

    if not expense_df.empty:
        category_frequency = (
            expense_df.groupby("category")
            .size()
            .reset_index(name="transaction_count")
        )

        fig_freq = px.bar(category_frequency, x="category", y="transaction_count")
        st.plotly_chart(fig_freq, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # PATTERN EXPLORATION
    # --------------------------------------------------------
    st.subheader("🔎 Expense Pattern Exploration")

    if not expense_df.empty:
        scatter_df = expense_df.copy()
        scatter_df["day"] = scatter_df["date"].dt.day

        fig_scatter = px.scatter(
            scatter_df,
            x="day",
            y="amount",
            color="category",
            size="amount",
            hover_data=["date", "description"]
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # SMART INSIGHTS (simple derived insights)
    # --------------------------------------------------------
    st.subheader("💡 Insights")

    if not expense_df.empty:
        top_category = (
            expense_df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

        st.write(f"Top spending category: **{top_category}**")

else:
    st.info("No data available yet. Add transactions to populate your dashboard.")