# 🤖 AI Job Market Analysis

A complete, end-to-end **Data Analyst project** exploring trends in the AI job
market — salaries, in-demand skills, remote work patterns, and regional hiring —
built with **Python, SQL, and data visualization**, and designed to be finished
in a single day and dropped straight into a portfolio / GitHub profile.

---

## 📌 Project Summary

| | |
|---|---|
| **Domain** | AI / Data & Analytics job market |
| **Type** | Exploratory Data Analysis + SQL analysis + Dashboard-ready outputs |
| **Tools** | Python (pandas, matplotlib, seaborn), SQL (SQLite), Jupyter |
| **Dataset** | 2,000 synthetic but realistic AI job postings (2025) |
| **Deliverables** | Cleaned dataset, SQLite DB, SQL queries, Jupyter notebook, 6 charts, executive summary report |

## 🎯 Business Questions Answered

1. Which AI job titles pay the most, on average?
2. How does salary scale with experience level (Entry → Lead)?
3. Which regions and industries are hiring the most for AI roles?
4. Which AI skills are most in demand across job postings?
5. Is there a seasonal pattern to AI hiring throughout the year?
6. Does remote work correlate with pay or competitiveness?

## 🗂️ Project Structure

```
AI_Job_Market_Analysis/
├── data/
│   └── ai_job_postings.csv          # Cleaned dataset (2,000 rows x 14 cols)
├── database/
│   └── ai_jobs.db                   # SQLite database (table: job_postings)
├── sql/
│   └── analysis_queries.sql         # 10 SQL analysis queries
├── notebooks/
│   └── ai_job_market_analysis.ipynb # Full EDA notebook (pre-run, with charts)
├── scripts/
│   ├── generate_dataset.py          # Synthetic dataset generator
│   ├── load_to_sqlite.py            # Loads CSV -> SQLite
│   ├── run_sql_queries.py           # Runs all SQL queries, saves output
│   ├── run_analysis.py              # Full EDA -> generates all 6 charts
│   └── build_notebook.py            # Builds the Jupyter notebook programmatically
├── visuals/
│   ├── 01_top_paying_job_titles.png
│   ├── 02_salary_by_experience.png
│   ├── 03_postings_by_region.png
│   ├── 04_monthly_posting_trend.png
│   ├── 05_top_ai_skills.png
│   └── 06_remote_salary_vs_competition.png
├── reports/
│   ├── summary_stats.csv
│   ├── top_ai_skills.csv
│   ├── sql_query_outputs.txt
│   └── Executive_Summary.docx       # 1-page written summary of key findings
├── requirements.txt
└── README.md
```

## 🧠 Why Synthetic Data?

Real scraped job-board data (LinkedIn, Indeed, Glassdoor, etc.) usually carries
licensing/ToS restrictions that make it risky to publish in a public GitHub repo.
This project instead **generates a statistically realistic dataset from scratch**
(`scripts/generate_dataset.py`) with deliberate, real-world patterns built in:
regional cost-of-living multipliers, experience-based salary scaling, and
realistic skill/platform distributions. This keeps the project 100% reproducible
and safe to share, while still producing genuine, non-trivial insights.

> 💡 **Want to use real data instead?** Swap `data/ai_job_postings.csv` for an
> export from a job-board API (e.g. Adzuna API, LinkedIn Jobs API, Kaggle AI
> job datasets) with the same column names, and every script/notebook/query
> in this repo will work unchanged.

## ⚙️ How to Run This Project

```bash
# 1. Clone/download the project, then install dependencies
pip install -r requirements.txt

# 2. Generate the dataset
python scripts/generate_dataset.py

# 3. Load it into a SQLite database
python scripts/load_to_sqlite.py

# 4. Run the SQL analysis queries
python scripts/run_sql_queries.py

# 5. Run the full EDA and generate all charts
python scripts/run_analysis.py

# 6. (Optional) Rebuild and re-execute the Jupyter notebook
python scripts/build_notebook.py
jupyter nbconvert --to notebook --execute --inplace notebooks/ai_job_market_analysis.ipynb
```

Or just open `notebooks/ai_job_market_analysis.ipynb` directly — it's already
executed and includes all charts and commentary inline.

## 📊 Key Findings

1. **Specialization pays.** Applied Scientist and AI Research Engineer roles
   pay 40–60% more than generalist AI Data Analyst roles — a natural next
   career step once foundational skills are established.
2. **Python + SQL are non-negotiable.** They appear in the majority of
   postings regardless of seniority or specialization.
3. **North America and Europe dominate hiring volume**, but South Asia
   (including Pakistan) shows a meaningful and growing share of postings,
   often for remote-friendly roles.
4. **Remote roles are high-value but high-competition** — they draw ~70%
   more applicants per posting than on-site roles, meaning hybrid roles can
   be an easier entry point for early-career candidates.
5. **AI hiring is fairly steady year-round**, useful context for timing a
   job search.

Full details in [`reports/Executive_Summary.docx`](reports/Executive_Summary.docx).

## 🚀 Possible Extensions

- Connect to a live job-board API to replace/validate the synthetic data.
- Build an interactive **Power BI / Tableau** dashboard on top of `ai_jobs.db`.
- Apply NLP topic modeling on `ai_skills_required` to surface emerging skill
  clusters (e.g. rise of "Prompt Engineering", "LLMOps").
- Deploy the notebook as a lightweight Streamlit app.

## 👤 Author

**Obaid Awan** — Aspiring Data Analyst
[LinkedIn](https://www.linkedin.com/in/obayd-awan) · [GitHub](https://github.com/Obaydawan)

## 📄 License

This project is released under the MIT License — see [LICENSE](LICENSE).
