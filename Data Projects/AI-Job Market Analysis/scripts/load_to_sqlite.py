"""
load_to_sqlite.py
------------------
Loads the generated CSV into a SQLite database so the project can
demonstrate SQL-based analysis (as well as pandas-based analysis).

Run:
    python scripts/load_to_sqlite.py
Output:
    database/ai_jobs.db  (table: job_postings)
"""

import sqlite3
import pandas as pd

CSV_PATH = "data/ai_job_postings.csv"
DB_PATH = "database/ai_jobs.db"

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
df.to_sql("job_postings", conn, if_exists="replace", index=False)

# Quick sanity check
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM job_postings;")
count = cur.fetchone()[0]
print(f"Loaded {count} rows into {DB_PATH} (table: job_postings)")

conn.close()
