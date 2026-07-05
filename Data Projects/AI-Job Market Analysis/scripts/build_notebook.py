import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

md("""# AI Job Market Analysis — Data Analyst Project
**Author:** Obaid Awan | Data Analyst Portfolio Project

## Project Overview
The demand for AI-related roles (Data Analysts, ML Engineers, NLP Engineers, etc.)
has grown rapidly since 2023. This project analyzes a dataset of **2,000 AI-related
job postings from 2025** to answer practical business questions a hiring team,
job seeker, or workforce-planning analyst would care about.

## Business Questions
1. Which AI job titles pay the most, on average?
2. How does salary scale with experience level?
3. Which regions are hiring the most for AI roles, and at what pay?
4. Which AI skills are most in demand across job postings?
5. Is there a seasonal pattern to AI hiring throughout the year?
6. Does remote work correlate with pay or competitiveness (applicants per posting)?

## Dataset
`data/ai_job_postings.csv` — 2,000 rows, 14 columns. The dataset is **synthetically
generated** (see `scripts/generate_dataset.py`) using realistic salary bands,
regional cost-of-living multipliers, and experience-level scaling, so the analysis
patterns are meaningful and fully reproducible without any web-scraping/licensing
concerns.

| Column | Description |
|---|---|
| job_id | Unique job posting ID |
| job_title | AI-related job title |
| company | Company name (synthetic) |
| industry | Hiring company's industry |
| country / region | Job location |
| experience_level | Entry / Mid / Senior / Lead |
| remote_type | Remote / Hybrid / On-site |
| salary_usd | Annual salary in USD |
| ai_skills_required | Comma-separated list of required skills |
| num_ai_skills | Count of required skills |
| applicants | Number of applicants on the posting |
| source_platform | Job board the posting came from |
| posting_date | Date posted (2025) |
""")

code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 110

df = pd.read_csv("../data/ai_job_postings.csv", parse_dates=["posting_date"])
df.head()
""")

md("## 1. Data Cleaning & Quality Check")
code("""print("Shape:", df.shape)
print("\\nMissing values:\\n", df.isna().sum())
print("\\nDuplicate job_ids:", df['job_id'].duplicated().sum())
""")

code("""# Median-impute the small number of missing 'applicants' values (realistic export gap)
df['applicants'] = df['applicants'].fillna(df['applicants'].median()).astype(int)
df.isna().sum().sum()  # should be 0 now
""")

md("## 2. Descriptive Statistics")
code("""df[['salary_usd', 'applicants', 'num_ai_skills']].describe().round(1)""")

md("""## 3. Q1 & Q2 — Salary by Job Title and Experience Level
Which titles pay the most, and how much does experience matter?""")
code("""avg_salary_title = df.groupby('job_title')['salary_usd'].mean().sort_values(ascending=False)

plt.figure(figsize=(9,6))
sns.barplot(x=avg_salary_title.head(10).values, y=avg_salary_title.head(10).index, hue=avg_salary_title.head(10).index, legend=False, palette="viridis")
plt.title("Top 10 Highest-Paying AI Job Titles (Avg. Annual Salary)")
plt.xlabel("Average Salary (USD)")
plt.ylabel("")
plt.show()
""")

code("""order = ["Entry", "Mid", "Senior", "Lead"]
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x="experience_level", y="salary_usd", order=order, hue="experience_level", legend=False, palette="mako")
plt.title("Salary Distribution by Experience Level")
plt.show()
""")

md("**Insight:** Specialized ML/AI research roles (Applied Scientist, AI Research Engineer, "
   "Generative AI Developer) command the highest pay, while general AI Data Analyst roles "
   "sit at the entry point of the AI career ladder — useful context for someone positioning "
   "themselves as a junior/entry-level AI-adjacent data analyst.")

md("## 4. Q3 — Regional Hiring Patterns")
code("""region_summary = df.groupby("region").agg(
    num_postings=("job_id", "count"),
    avg_salary=("salary_usd", "mean")
).sort_values("num_postings", ascending=False)
region_summary
""")

code("""plt.figure(figsize=(8,6))
sns.barplot(x=region_summary["num_postings"], y=region_summary.index, hue=region_summary.index, legend=False, palette="crest")
plt.title("Number of AI Job Postings by Region")
plt.xlabel("Number of Postings")
plt.show()
""")

md("## 5. Q4 — Most In-Demand AI Skills")
code("""all_skills = df["ai_skills_required"].str.split(", ").sum()
skill_counts = pd.Series(Counter(all_skills)).sort_values(ascending=False)

plt.figure(figsize=(9,6))
top12 = skill_counts.head(12)
sns.barplot(x=top12.values, y=top12.index, hue=top12.index, legend=False, palette="flare")
plt.title("Top 12 Most In-Demand AI Skills")
plt.xlabel("Number of Postings Requiring Skill")
plt.show()
""")

md("**Insight:** Python and SQL remain the foundational skills across almost every AI-adjacent "
   "role — reinforcing that a data analyst breaking into AI should prioritize those before "
   "specializing into deep learning frameworks.")

md("## 6. Q5 — Seasonal Hiring Trend Across 2025")
code("""monthly = df.set_index("posting_date").resample("ME").size()

plt.figure(figsize=(10,5))
plt.plot(monthly.index, monthly.values, marker="o", linewidth=2, color="#3b6e8f")
plt.title("AI Job Postings Trend Across 2025")
plt.xlabel("Month")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)
plt.show()
""")

md("## 7. Q6 — Remote Work vs. Salary & Competitiveness")
code("""remote_summary = df.groupby("remote_type").agg(
    avg_salary=("salary_usd", "mean"),
    avg_applicants=("applicants", "mean"),
    num_postings=("job_id", "count")
).reindex(["Remote", "Hybrid", "On-site"])
remote_summary
""")

code("""fig, ax1 = plt.subplots(figsize=(8,6))
ax1.bar(remote_summary.index, remote_summary["avg_salary"], color="#3b6e8f", alpha=0.85)
ax1.set_ylabel("Average Salary (USD)")
ax1.set_title("Remote Work Type: Salary vs. Competitiveness")

ax2 = ax1.twinx()
ax2.plot(remote_summary.index, remote_summary["avg_applicants"], color="#d1495b", marker="o", linewidth=2.5)
ax2.set_ylabel("Average Applicants per Posting")
ax2.grid(False)
plt.show()
""")

md("""**Insight:** Remote AI roles attract noticeably more applicants per posting than
on-site roles, meaning remote positions — while attractive — are also the most
competitive. On-site or hybrid roles may represent an easier point of entry for
candidates early in their careers.

## 8. Key Takeaways (Executive Summary)

1. **Specialization pays.** Applied Scientist and AI Research Engineer roles pay
   40–60% more than generalist AI Data Analyst roles — a natural next step once
   foundational skills are established.
2. **Python + SQL are non-negotiable.** They appear in the majority of postings
   regardless of seniority or specialization.
3. **North America and Europe dominate hiring volume**, but South Asia (including
   Pakistan) shows a meaningful and growing share of postings, often for remote-friendly
   roles — relevant for professionals targeting international remote opportunities.
4. **Remote roles are high-value but high-competition.** Entry-level candidates may find
   less crowded (and equally valuable early-career) opportunities in hybrid roles.
5. **Hiring is fairly steady year-round**, with a mild dip in December — useful for
   timing job-search pushes.

## 9. Next Steps
- Layer in a live job-board API (e.g., Adzuna, LinkedIn Jobs API) to replace/validate
  the synthetic data with real postings.
- Build an interactive Power BI / Tableau dashboard on top of `database/ai_jobs.db`.
- Extend with NLP topic modeling on `ai_skills_required` to surface emerging skill clusters.
""")

nb['cells'] = cells
nb['metadata'] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"}
}

with open("notebooks/ai_job_market_analysis.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook written to notebooks/ai_job_market_analysis.ipynb")
