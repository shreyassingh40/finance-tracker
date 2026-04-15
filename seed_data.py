# seed_data.py
# --------------------------------------------------------
# Seed sample transaction data into finance.db for one user
# --------------------------------------------------------

from src.database import create_table, insert_transaction, fetch_transactions

SEED_USERNAME = "shreyas40"   # change this to the exact username you want seeded

def seed_transactions():
    create_table()

    existing = fetch_transactions(SEED_USERNAME)
    if existing:
        print(f"Database already contains data for {SEED_USERNAME}. Seed skipped.")
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
    ]

    for row in sample_data:
        insert_transaction(SEED_USERNAME, *row)

    print(f"Inserted {len(sample_data)} sample transactions for {SEED_USERNAME}.")

if __name__ == "__main__":
    seed_transactions()