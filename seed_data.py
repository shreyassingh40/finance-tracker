# seed_data.py
# --------------------------------------------------------
# Seed sample transaction data into finance.db
# Run once to populate the dashboard with realistic data
# --------------------------------------------------------

from src.database import create_table, insert_transaction, fetch_transactions

def seed_transactions():
    # Create table if it does not already exist
    create_table()

    # Prevent duplicate seeding
    existing = fetch_transactions()
    if existing:
        print("Database already contains data. Seed skipped.")
        return

    sample_data = [
        ("2025-10-01", "Salary", "income", 3000, "Monthly salary"),
        ("2025-10-02", "Rent", "expense", 1200, "Monthly rent payment"),
        ("2025-10-03", "Food", "expense", 18.50, "Lunch at university"),
        ("2025-10-04", "Transport", "expense", 25.00, "Bus and train top-up"),
        ("2025-10-05", "Shopping", "expense", 80.00, "Clothes purchase"),
        ("2025-10-06", "Entertainment", "expense", 45.00, "Cinema and snacks"),
        ("2025-10-08", "Food", "expense", 65.20, "Groceries"),
        ("2025-10-10", "Health", "expense", 22.00, "Pharmacy items"),
        ("2025-10-12", "Utilities", "expense", 95.00, "Electricity bill"),
        ("2025-10-15", "Other", "expense", 30.00, "Miscellaneous spending"),

        ("2025-11-01", "Salary", "income", 3000, "Monthly salary"),
        ("2025-11-02", "Rent", "expense", 1200, "Monthly rent payment"),
        ("2025-11-03", "Food", "expense", 14.50, "Coffee and breakfast"),
        ("2025-11-05", "Transport", "expense", 20.00, "Petrol contribution"),
        ("2025-11-06", "Entertainment", "expense", 60.00, "Dinner with friends"),
        ("2025-11-08", "Shopping", "expense", 120.00, "New shoes"),
        ("2025-11-10", "Food", "expense", 72.40, "Weekly groceries"),
        ("2025-11-12", "Utilities", "expense", 88.00, "Internet bill"),
        ("2025-11-14", "Health", "expense", 35.00, "Doctor visit"),
        ("2025-11-18", "Other", "expense", 40.00, "Stationery and supplies"),

        ("2025-12-01", "Salary", "income", 3000, "Monthly salary"),
        ("2025-12-02", "Rent", "expense", 1200, "Monthly rent payment"),
        ("2025-12-03", "Food", "expense", 16.20, "Lunch"),
        ("2025-12-05", "Transport", "expense", 30.00, "Fuel"),
        ("2025-12-06", "Entertainment", "expense", 90.00, "Concert ticket"),
        ("2025-12-07", "Shopping", "expense", 150.00, "Holiday shopping"),
        ("2025-12-09", "Food", "expense", 85.00, "Groceries"),
        ("2025-12-11", "Utilities", "expense", 102.00, "Power and water"),
        ("2025-12-13", "Health", "expense", 28.00, "Supplements"),
        ("2025-12-16", "Other", "expense", 55.00, "Gift purchase"),

        ("2026-01-01", "Salary", "income", 3000, "Monthly salary"),
        ("2026-01-02", "Rent", "expense", 1200, "Monthly rent payment"),
        ("2026-01-04", "Food", "expense", 19.00, "Takeaway dinner"),
        ("2026-01-06", "Transport", "expense", 24.00, "Public transport"),
        ("2026-01-07", "Shopping", "expense", 65.00, "Gym clothes"),
        ("2026-01-09", "Entertainment", "expense", 35.00, "Streaming and games"),
        ("2026-01-10", "Food", "expense", 77.30, "Groceries"),
        ("2026-01-12", "Utilities", "expense", 91.00, "Phone and internet"),
        ("2026-01-15", "Health", "expense", 20.00, "Protein shake"),
        ("2026-01-18", "Other", "expense", 25.00, "Printing and stationery"),

        ("2026-02-01", "Salary", "income", 3000, "Monthly salary"),
        ("2026-02-02", "Rent", "expense", 1200, "Monthly rent payment"),
        ("2026-02-03", "Food", "expense", 17.80, "Lunch"),
        ("2026-02-05", "Transport", "expense", 22.00, "Bus card top-up"),
        ("2026-02-06", "Shopping", "expense", 95.00, "Headphones"),
        ("2026-02-08", "Entertainment", "expense", 50.00, "Bowling night"),
        ("2026-02-10", "Food", "expense", 79.90, "Groceries"),
        ("2026-02-13", "Utilities", "expense", 93.00, "Electricity and water"),
        ("2026-02-15", "Health", "expense", 26.00, "Pharmacy"),
        ("2026-02-18", "Other", "expense", 38.00, "Miscellaneous costs"),
    ]

    for row in sample_data:
        insert_transaction(*row)

    print(f"Inserted {len(sample_data)} sample transactions.")

if __name__ == "__main__":
    seed_transactions()