# analytics.py
# ----------------------------------------------------------
# This module loads transaction data from the database
# and performs simple financial analysis using Pandas.
# ----------------------------------------------------------

import pandas as pd
from src.database import fetch_transactions

def load_data():
    rows = fetch_transactions()

    if not rows:
        return pd.DataFrame(columns=["id", "date", "category", "type", "amount", "description"])

    df = pd.DataFrame(
        rows,
        columns=["id", "date", "category", "type", "amount", "description"]
    )

    df["date"] = pd.to_datetime(df["date"])
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["type"] = df["type"].astype(str).str.strip().str.lower()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    return df

def monthly_summary(df):
    if df.empty:
        return pd.DataFrame()

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
        return pd.DataFrame()

    expense_df = df[df["type"] == "expense"].copy()

    if expense_df.empty:
        return pd.DataFrame(columns=["category", "total"])

    category_df = (
        expense_df.groupby("category", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total"})
        .sort_values("total", ascending=False)
    )

    return category_df
