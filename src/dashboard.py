# dashboard.py
# --------------------------------------------------------
# Streamlit Dashboard for Personal Finance Tracker
# Provides a form for adding transactions,
# a data table for viewing all entries,
# and analytics charts using Pandas.
# --------------------------------------------------------

import streamlit as st
import pandas as pd
from datetime import date

# Import our own modules
from src.database import create_table, insert_transaction, fetch_transactions
from src.analytics import load_data, monthly_summary, category_breakdown

# --------------------------------------------------------
# Streamlit Page Setup
# --------------------------------------------------------
st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("💰 Personal Finance Tracker")
st.write("Track your expenses, income, and see insights over time.")

# --------------------------------------------------------
# Ensure database table exists
# --------------------------------------------------------
create_table()

# --------------------------------------------------------
# SECTION 1: Add a Transaction
# --------------------------------------------------------
st.subheader("➕ Add Transaction")

# Create a simple form for adding entries
with st.form("add_transaction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        t_date = st.date_input("Date", value=date.today())

    with col2:
        category = st.text_input("Category (e.g., Food, Rent, Salary)")

    with col3:
        t_type = st.selectbox("Type", ["expense", "income"])

    amount = st.number_input("Amount ($)", min_value=0.0, step=0.5)
    description = st.text_area("Description (optional)")

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if not category or amount == 0:
            st.error("⚠️ Please enter a valid category and amount.")
        else:
            insert_transaction(str(t_date), category, t_type, amount, description)
            st.success("✅ Transaction added successfully!")

st.divider()

# --------------------------------------------------------
# SECTION 2: View All Transactions
# --------------------------------------------------------
st.subheader("📋 All Transactions")
transactions = fetch_transactions()

if transactions:
    df = pd.DataFrame(transactions, columns=["ID", "Date", "Category", "Type", "Amount", "Description"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions yet. Add one above!")

st.divider()

# --------------------------------------------------------
# SECTION 3: Analytics Overview
# --------------------------------------------------------
st.subheader("📊 Analytics Overview")

df = load_data()

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Monthly Summary (Income vs Expense)")
        summary = monthly_summary(df)
        st.dataframe(summary)
        st.bar_chart(summary.set_index("month"))

    with col2:
        st.markdown("### Category Breakdown")
        categories = category_breakdown(df)
        st.dataframe(categories)
        st.bar_chart(categories.set_index("category"))
else:
    st.warning("⚠️ No data available for analytics yet.")
