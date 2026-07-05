"""
run_sql_queries.py
-------------------
Executes each query in sql/analysis_queries.sql against database/ai_jobs.db
and writes formatted results to reports/sql_query_outputs.txt.
Used since the sandboxed environment doesn't have the sqlite3 CLI installed,
but this works identically to running the .sql file with the CLI.
"""

import sqlite3
import re
import pandas as pd

with open("sql/analysis_queries.sql") as f:
    content = f.read()

# Split on numbered comment headers like "-- 1. ..."
blocks = re.split(r"\n(?=-- \d+\.)", content)
conn = sqlite3.connect("database/ai_jobs.db")

with open("reports/sql_query_outputs.txt", "w") as out:
    for block in blocks:
        block = block.strip()
        if not block or not block.startswith("--"):
            continue
        header_match = re.match(r"-- (\d+\..*)", block)
        header = header_match.group(1) if header_match else "Query"
        # extract the SQL statement itself (skip comment lines)
        sql_lines = [l for l in block.split("\n") if not l.strip().startswith("--") and l.strip()]
        sql = "\n".join(sql_lines).strip()
        if not sql:
            continue
        out.write("=" * 78 + "\n")
        out.write(header + "\n")
        out.write("=" * 78 + "\n")
        try:
            df = pd.read_sql_query(sql, conn)
            out.write(df.to_string(index=False) + "\n\n")
        except Exception as e:
            out.write(f"[Skipped: {e}]\n\n")

conn.close()
print("Saved reports/sql_query_outputs.txt")
