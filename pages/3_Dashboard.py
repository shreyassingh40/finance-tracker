# 3_Dashboard.py

import sys
import os
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

# Load user-specific data
df = load_data(username)

if not df.empty:
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    net = income - expense
    transaction_count = len(df)

    # Top metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Income", f"${income:.2f}")
    m2.metric("Expenses", f"${expense:.2f}")
    m3.metric("Net Balance", f"${net:.2f}")
    m4.metric("Transactions", transaction_count)

    st.divider()

    # Net balance over time
    st.subheader("📈 Net Balance Over Time")

    net_df = df.copy()
    net_df["month"] = net_df["date"].dt.to_period("M").astype(str)

    monthly_income = (
        net_df[net_df["type"] == "income"]
        .groupby("month")["amount"]
        .sum()
    )

    monthly_expense = (
        net_df[net_df["type"] == "expense"]
        .groupby("month")["amount"]
        .sum()
    )

    monthly_net = (
        monthly_income.subtract(monthly_expense, fill_value=0)
        .reset_index()
    )

    monthly_net.columns = ["month", "net_balance"]

    fig_net = px.bar(
        monthly_net,
        x="month",
        y="net_balance",
        title="Monthly Net Balance"
    )
    st.plotly_chart(fig_net, use_container_width=True)

    st.divider()

    # Two main analysis charts
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

    st.divider()

    # Additional data science style charts
    expense_df = df[df["type"] == "expense"].copy()

    st.subheader("📊 Average Expense per Transaction by Category")

    if not expense_df.empty:
        avg_category_spend = (
            expense_df.groupby("category", as_index=False)["amount"]
            .mean()
            .sort_values("amount", ascending=False)
        )

        fig_avg = px.bar(
            avg_category_spend,
            x="category",
            y="amount",
            title="Average Expense by Category"
        )
        st.plotly_chart(fig_avg, use_container_width=True)

    st.subheader("🧾 Transaction Frequency by Category")

    if not expense_df.empty:
        category_frequency = (
            expense_df.groupby("category")
            .size()
            .reset_index(name="transaction_count")
            .sort_values("transaction_count", ascending=False)
        )

        fig_freq = px.bar(
            category_frequency,
            x="category",
            y="transaction_count",
            title="Number of Expense Transactions by Category"
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    st.divider()

    # Smart insights
    st.subheader("💡 Smart Insights")

    if not expense_df.empty:
        top_category_summary = (
            expense_df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        top_category = top_category_summary.index[0]
        top_value = top_category_summary.iloc[0]
        saving_potential = top_value * 0.15

        st.markdown(
            f"""
            Your highest spending category is **{top_category}** at **${top_value:.2f}**.

            If you reduced spending in this category by **15%**, you could potentially save
            **${saving_potential:.2f}** over a similar period.
            """
        )

        monthly_spend = (
            expense_df.assign(month=expense_df["date"].dt.to_period("M").astype(str))
            .groupby("month")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        highest_month = monthly_spend.index[0]
        highest_month_amount = monthly_spend.iloc[0]

        st.info(
            f"📌 Your highest-spending month was **{highest_month}**, with total expenses of **${highest_month_amount:.2f}**."
        )

        largest_expense_row = expense_df.loc[expense_df["amount"].idxmax()]
        st.warning(
            f"⚠️ Your largest single expense was **${largest_expense_row['amount']:.2f}** "
            f"in **{largest_expense_row['category']}** on **{largest_expense_row['date'].strftime('%Y-%m-%d')}**."
        )

    st.divider()

    # Recent activity
    st.subheader("🕒 Recent Activity")

    transactions = fetch_transactions(username)

    if transactions:
        recent_df = df.copy().sort_values("date", ascending=False).head(5)
        recent_df["date"] = recent_df["date"].dt.strftime("%Y-%m-%d")
        recent_df = recent_df.rename(columns={
            "date": "Date",
            "category": "Category",
            "type": "Type",
            "amount": "Amount",
            "description": "Description"
        })

        st.dataframe(
            recent_df[["Date", "Category", "Type", "Amount", "Description"]],
            use_container_width=True
        )

    st.divider()

    # Full transaction table
    st.subheader("📋 All Transactions")

    if transactions:
        full_df = df.copy().sort_values("date", ascending=False)
        full_df["date"] = full_df["date"].dt.strftime("%Y-%m-%d")
        full_df = full_df.rename(columns={
            "id": "ID",
            "date": "Date",
            "category": "Category",
            "type": "Type",
            "amount": "Amount",
            "description": "Description"
        })

        st.dataframe(
            full_df[["ID", "Date", "Category", "Type", "Amount", "Description"]],
            use_container_width=True
        )

else:
    st.info("No data available yet. Add transactions to populate your dashboard.")