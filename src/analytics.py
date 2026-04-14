# analytics.py
# --------------------------------------------------------
# Analytics functions for Personal Finance Tracker
# --------------------------------------------------------

import pandas as pd
from src.database import fetch_transactions

def load_data(username):
    rows = fetch_transactions(username)

    if not rows:
        return pd.DataFrame(columns=["id", "username", "date", "category", "type", "amount", "description"])

    df = pd.DataFrame(
        rows,
        columns=["id", "username", "date", "category", "type", "amount", "description"]
    )

    df["date"] = pd.to_datetime(df["date"])
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["type"] = df["type"].astype(str).str.strip().str.lower()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    return df

def monthly_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["month"])

    monthly_df = df.copy()
    monthly_df["month"] = monthly_df["date"].dt.to_period("M").astype(str)

    summary = (
        monthly_df.groupby(["month", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
        .sort_values("month")
    )

    return summary

def category_breakdown(df):
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])

    expense_df = df[df["type"] == "expense"].copy()

    if expense_df.empty:
        return pd.DataFrame(columns=["category", "amount"])

    category_df = (
        expense_df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )

    return category_df