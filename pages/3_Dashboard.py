# dashboard.py
# --------------------------------------------------------
# Streamlit Dashboard for Personal Finance Tracker
# --------------------------------------------------------

import sys
import os
from pathlib import Path
from datetime import date

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
st.set_page_config(page_title="Personal Finance Tracker", layout="wide")  # 1) put this first

import pandas as pd
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

# Import our own modules
from src.database import create_table, insert_transaction, fetch_transactions
from src.analytics import load_data, monthly_summary, category_breakdown

# --- Load config (robust absolute path) ---
# This file lives in the project root, not inside /pages
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

# --- Login widget ---
st.title("🔐 Login")
name, auth_status, username = authenticator.login(location="main")

if auth_status is False:
    st.error("Username or password is incorrect.")
elif auth_status is None:
    st.info("Please enter your username and password.")
else:
    # ========== AUTHENTICATED AREA ONLY ==========
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome, {name} 👋")

    st.title("💰 Personal Finance Tracker")
    st.write("Track your expenses, income, and view financial insights over time.")

    # Ensure database table exists
    create_table()

    # SECTION 1: Add a Transaction
    st.subheader("➕ Add Transaction")
    with st.form("add_transaction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            t_date = st.date_input("Date", value=date.today())

        with col2:
            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Transport",
                    "Rent",
                    "Entertainment",
                    "Utilities",
                    "Shopping",
                    "Salary",
                    "Health",
                    "Education",
                    "Other"
                ]
            )

        with col3:
            t_type = st.selectbox("Type", ["expense", "income"])

        amount = st.number_input("Amount ($)", min_value=0.0, step=0.5)
        description = st.text_area("Description (optional)")
        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            if amount == 0:
                st.error("⚠️ Please enter a valid amount.")
            else:
                insert_transaction(str(t_date), category, t_type, amount, description)
                st.success("✅ Transaction added successfully!")

    st.divider()

    # SECTION 2: View All Transactions
    st.subheader("📋 All Transactions")
    transactions = fetch_transactions()

    if transactions:
        df_table = pd.DataFrame(
            transactions,
            columns=["ID", "Date", "Category", "Type", "Amount", "Description"]
        )
        st.dataframe(df_table, use_container_width=True)
    else:
        st.info("No transactions yet. Add one above!")

    st.divider()

    # SECTION 3: Analytics Overview
    st.subheader("📊 Analytics Overview")
    df = load_data()

    if not df.empty:
        # --- Summary metrics ---
        total_income = df[df["type"] == "income"]["amount"].sum()
        total_expense = df[df["type"] == "expense"]["amount"].sum()
        net_balance = total_income - total_expense

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Income", f"${total_income:.2f}")
        with m2:
            st.metric("Total Expenses", f"${total_expense:.2f}")
        with m3:
            st.metric("Net Balance", f"${net_balance:.2f}")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Monthly Summary (Income vs Expense)")
            summary = monthly_summary(df)
            st.dataframe(summary, use_container_width=True)

            # If 'month' is a column, set it as index for the chart
            if not summary.empty:
                if "month" in summary.columns:
                    st.bar_chart(summary.set_index("month"))
                else:
                    st.bar_chart(summary)

        with col2:
            st.markdown("### Category Breakdown")
            categories = category_breakdown(df)
            st.dataframe(categories, use_container_width=True)

            # If 'category' is a column, set it as index for the chart
            if not categories.empty:
                if "category" in categories.columns:
                    st.bar_chart(categories.set_index("category"))
                else:
                    st.bar_chart(categories)

        st.divider()

        # SECTION 4: Spending Insight
        st.subheader("💡 Smart Insight")

        expense_df = df[df["type"] == "expense"].copy()

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

            # Optional month-to-month insight
            monthly_expense = (
                expense_df.assign(month=expense_df["date"].dt.to_period("M").astype(str))
                .groupby("month")["amount"]
                .sum()
                .sort_index()
            )

            if len(monthly_expense) >= 2:
                latest = monthly_expense.iloc[-1]
                previous = monthly_expense.iloc[-2]
                change = latest - previous

                if change > 0:
                    st.info(
                        f"📈 Your expenses increased by **${change:.2f}** compared to the previous month."
                    )
                elif change < 0:
                    st.success(
                        f"📉 Your expenses decreased by **${abs(change):.2f}** compared to the previous month."
                    )
                else:
                    st.info("Your expenses were unchanged compared to the previous month.")
        else:
            st.info("Add some expense transactions to generate spending insights.")

    else:
        st.warning("⚠️ No data available for analytics yet.")