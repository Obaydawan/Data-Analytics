"""
run_analysis.py
----------------
Performs the core EDA for the AI Job Market Analysis project and saves:
  - Cleaned dataset summary stats -> reports/summary_stats.csv
  - Top skills breakdown          -> reports/top_ai_skills.csv
  - 6 charts                      -> visuals/*.png

Run:
    python scripts/run_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 130
plt.rcParams["savefig.bbox"] = "tight"

DATA_PATH = "data/ai_job_postings.csv"
VIS_DIR = "visuals"
REPORT_DIR = "reports"

df = pd.read_csv(DATA_PATH, parse_dates=["posting_date"])

# ---------------------------------------------------------------------------
# 1. Data cleaning
# ---------------------------------------------------------------------------
missing_before = df.isna().sum().sum()
df["applicants"] = df["applicants"].fillna(df["applicants"].median())
df["applicants"] = df["applicants"].astype(int)
print(f"Filled {missing_before} missing values (median imputation on 'applicants').")

# ---------------------------------------------------------------------------
# 2. Summary statistics
# ---------------------------------------------------------------------------
summary = df[["salary_usd", "applicants", "num_ai_skills"]].describe().T
summary.to_csv(f"{REPORT_DIR}/summary_stats.csv")
print("Saved reports/summary_stats.csv")

# ---------------------------------------------------------------------------
# 3. Chart 1 — Average salary by job title (top 10)
# ---------------------------------------------------------------------------
avg_salary_title = (
    df.groupby("job_title")["salary_usd"].mean().sort_values(ascending=False).head(10)
)
plt.figure(figsize=(9, 6))
sns.barplot(x=avg_salary_title.values, y=avg_salary_title.index, palette="viridis")
plt.title("Top 10 Highest-Paying AI Job Titles (Avg. Annual Salary, USD)")
plt.xlabel("Average Salary (USD)")
plt.ylabel("")
for i, v in enumerate(avg_salary_title.values):
    plt.text(v + 1000, i, f"${v:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/01_top_paying_job_titles.png")
plt.close()

# ---------------------------------------------------------------------------
# 4. Chart 2 — Salary distribution by experience level
# ---------------------------------------------------------------------------
order = ["Entry", "Mid", "Senior", "Lead"]
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="experience_level", y="salary_usd", order=order, palette="mako")
plt.title("Salary Distribution by Experience Level")
plt.xlabel("Experience Level")
plt.ylabel("Salary (USD)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/02_salary_by_experience.png")
plt.close()

# ---------------------------------------------------------------------------
# 5. Chart 3 — Postings by region
# ---------------------------------------------------------------------------
region_counts = df["region"].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=region_counts.values, y=region_counts.index, palette="crest")
plt.title("Number of AI Job Postings by Region")
plt.xlabel("Number of Postings")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/03_postings_by_region.png")
plt.close()

# ---------------------------------------------------------------------------
# 6. Chart 4 — Monthly posting trend (2025)
# ---------------------------------------------------------------------------
monthly = df.set_index("posting_date").resample("ME").size()
plt.figure(figsize=(10, 5))
plt.plot(monthly.index, monthly.values, marker="o", linewidth=2)
plt.title("AI Job Postings Trend Across 2025")
plt.xlabel("Month")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/04_monthly_posting_trend.png")
plt.close()

# ---------------------------------------------------------------------------
# 7. Chart 5 — Most in-demand AI skills
# ---------------------------------------------------------------------------
all_skills = df["ai_skills_required"].str.split(", ").sum()
skill_counts = Counter(all_skills)
top_skills = pd.Series(dict(skill_counts)).sort_values(ascending=False).head(12)
top_skills.to_csv(f"{REPORT_DIR}/top_ai_skills.csv", header=["num_postings"])

plt.figure(figsize=(9, 6))
sns.barplot(x=top_skills.values, y=top_skills.index, palette="flare")
plt.title("Top 12 Most In-Demand AI Skills Across Job Postings")
plt.xlabel("Number of Postings Requiring Skill")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/05_top_ai_skills.png")
plt.close()
print("Saved reports/top_ai_skills.csv")

# ---------------------------------------------------------------------------
# 8. Chart 6 — Remote type vs avg salary & competitiveness (dual view)
# ---------------------------------------------------------------------------
remote_summary = df.groupby("remote_type").agg(
    avg_salary=("salary_usd", "mean"),
    avg_applicants=("applicants", "mean"),
    num_postings=("job_id", "count"),
).reindex(["Remote", "Hybrid", "On-site"])

fig, ax1 = plt.subplots(figsize=(8, 6))
bars = ax1.bar(remote_summary.index, remote_summary["avg_salary"], color="#3b6e8f", alpha=0.85, label="Avg Salary (USD)")
ax1.set_ylabel("Average Salary (USD)")
ax1.set_title("Remote Work Type: Salary vs. Competitiveness")
for i, v in enumerate(remote_summary["avg_salary"]):
    ax1.text(i, v + 1500, f"${v:,.0f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(remote_summary.index, remote_summary["avg_applicants"], color="#d1495b", marker="o", linewidth=2.5, label="Avg Applicants")
ax2.set_ylabel("Average Applicants per Posting")
ax2.grid(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/06_remote_salary_vs_competition.png")
plt.close()

print("All 6 charts saved to /visuals")
print("\nEDA complete.")
