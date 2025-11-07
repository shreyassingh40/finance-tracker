# Personal Finance Tracker – Data Analytics App (2025)

A **Python + Streamlit** application that helps users track income and expenses, analyze monthly summaries, and visualize category-based spending.  
All data is stored locally using **SQLite**, and analytics are powered by **Pandas**.

---

## Features

- Add income or expense transactions
- Monthly summary comparing income vs expense
- Category-wise spending breakdown
- Interactive Streamlit dashboard
- Local SQLite database (no internet needed)
- Real-time analytics using Pandas

---

## Tech Stack

| Layer                    | Technology                             |
| ------------------------ | -------------------------------------- |
| **Frontend / Dashboard** | Streamlit                              |
| **Backend / Logic**      | Python 3, Pandas                       |
| **Database**             | SQLite                                 |
| **Visualization**        | Streamlit Charts / Matplotlib / Plotly |
| **Version Control**      | Git & GitHub Desktop                   |

---

## Setup & Run Locally

```bash
# 1. Clone this repo
git clone https://github.com/<your-username>/personal-finance-tracker.git
cd personal-finance-tracker

# 2. (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run src/dashboard.py

```
