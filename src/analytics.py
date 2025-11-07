# analytics.py
# ----------------------------------------------------------
# This module loads transaction data from the database
# and performs simple financial analysis using Pandas.
# ----------------------------------------------------------

import pandas as pd
from src.database import fetch_transactions  # reuses database functions

def load_data():
    """
    Load all transactions from the database and return them as a Pandas DataFrame.
    If there are no transactions yet, it returns an empty DataFrame.
    """
    data = fetch_transactions()  # Get rows from DB
    columns = ["id", "date", "category", "type", "amount", "description"]
    df = pd.DataFrame(data, columns=columns)

    # Convert the 'date' column into a proper datetime format (for grouping)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

def monthly_summary(df):
    """
    Create a monthly summary that compares income and expenses.
    Returns a new DataFrame with total income and expense per month.
    """
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expense"])

    # Extract month (YYYY-MM)
    df["month"] = df["date"].dt.to_period("M")

    # Group by month and type, then sum up
    summary = (
        df.groupby(["month", "type"])["amount"]
          .sum()
          .unstack(fill_value=0)
          .reset_index()
    )

    # Rename columns for clarity
    summary.columns.name = None
    return summary

def category_breakdown(df):
    """
    Summarize spending by category.
    Returns a DataFrame sorted by total amount descending.
    """
    if df.empty:
        return pd.DataFrame(columns=["category", "total"])

    # Group by category and sum amounts
    breakdown = (
        df.groupby("category")["amount"]
          .sum()
          .reset_index()
          .sort_values("amount", ascending=False)
    )
    breakdown.rename(columns={"amount": "total"}, inplace=True)
    return breakdown
