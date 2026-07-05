"""
generate_dataset.py
--------------------
Generates a realistic synthetic dataset of AI-related job postings for
the "AI Job Market Analysis" data analyst project.

Why synthetic data?
Real scraped job-board data usually comes with licensing/ToS restrictions
that make it unsafe to redistribute in a public portfolio project. This
script builds a statistically realistic dataset from scratch (with clear
patterns/relationships built in on purpose) so the analysis is meaningful
and fully reproducible by anyone who clones the repo.

Run:
    python scripts/generate_dataset.py
Output:
    data/ai_job_postings.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RANDOM_SEED = 42
N_ROWS = 2000

rng = np.random.default_rng(RANDOM_SEED)

# ---------------------------------------------------------------------------
# Reference lists
# ---------------------------------------------------------------------------
job_titles = [
    "AI Data Analyst", "Machine Learning Engineer", "Data Scientist",
    "AI Research Engineer", "NLP Engineer", "Computer Vision Engineer",
    "MLOps Engineer", "Business Intelligence Analyst (AI)", "AI Product Analyst",
    "Data Engineer (AI Systems)", "Prompt Engineer", "AI Ethics Analyst",
    "Generative AI Developer", "Applied Scientist", "AI Solutions Consultant",
]

# base salary (USD, annual) by title - used as a mean, later perturbed
title_salary_base = {
    "AI Data Analyst": 68000, "Machine Learning Engineer": 128000,
    "Data Scientist": 118000, "AI Research Engineer": 145000,
    "NLP Engineer": 132000, "Computer Vision Engineer": 130000,
    "MLOps Engineer": 125000, "Business Intelligence Analyst (AI)": 82000,
    "AI Product Analyst": 88000, "Data Engineer (AI Systems)": 112000,
    "Prompt Engineer": 98000, "AI Ethics Analyst": 90000,
    "Generative AI Developer": 135000, "Applied Scientist": 150000,
    "AI Solutions Consultant": 105000,
}

countries_regions = {
    "United States": "North America", "Canada": "North America",
    "United Kingdom": "Europe", "Germany": "Europe", "Netherlands": "Europe",
    "France": "Europe", "Ireland": "Europe", "Poland": "Europe",
    "Pakistan": "South Asia", "India": "South Asia", "UAE": "Middle East",
    "Singapore": "Southeast Asia", "Australia": "Oceania", "Brazil": "South America",
}
countries = list(countries_regions.keys())
country_weights = np.array([18, 6, 10, 9, 4, 6, 3, 3, 8, 12, 4, 4, 4, 3], dtype=float)
country_weights /= country_weights.sum()

# regional cost-of-living / market multiplier applied to base salary
region_multiplier = {
    "North America": 1.15, "Europe": 0.95, "South Asia": 0.35,
    "Middle East": 0.85, "Southeast Asia": 0.75, "Oceania": 1.05,
    "South America": 0.55,
}

experience_levels = ["Entry", "Mid", "Senior", "Lead"]
experience_multiplier = {"Entry": 0.65, "Mid": 1.0, "Senior": 1.45, "Lead": 1.9}
experience_weights = [0.32, 0.38, 0.22, 0.08]

remote_types = ["Remote", "Hybrid", "On-site"]
remote_weights = [0.38, 0.37, 0.25]

industries = [
    "Fintech", "Healthcare", "E-commerce", "Education", "Telecom",
    "Manufacturing", "Government", "Media & Entertainment", "Consulting",
    "Cybersecurity",
]

source_platforms = ["LinkedIn", "Indeed", "Glassdoor", "CompanyWebsite", "AngelList"]
platform_weights = [0.42, 0.24, 0.14, 0.12, 0.08]

ai_skill_pool = [
    "Python", "SQL", "Power BI", "Tableau", "TensorFlow", "PyTorch",
    "scikit-learn", "NLP", "Computer Vision", "LLMs", "Prompt Engineering",
    "Generative AI", "MLOps", "Excel", "R", "AWS", "Azure ML", "Docker",
    "Data Visualization", "Statistics", "A/B Testing", "ETL",
]

company_prefixes = ["Nova", "Quantum", "Vertex", "Nimbus", "Atlas", "Pulse",
                     "Orbit", "Cortex", "Lumen", "Zenith", "Vantage", "Delta",
                     "Prism", "Helix", "Arc"]
company_suffixes = ["AI", "Analytics", "Labs", "Systems", "Technologies",
                     "Solutions", "Data", "Works", "Intelligence", "Group"]

# ---------------------------------------------------------------------------
# Generate rows
# ---------------------------------------------------------------------------
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(1, N_ROWS + 1):
    title = rng.choice(job_titles)
    country = rng.choice(countries, p=country_weights)
    region = countries_regions[country]
    exp = rng.choice(experience_levels, p=experience_weights)
    remote = rng.choice(remote_types, p=remote_weights)
    industry = rng.choice(industries)
    platform = rng.choice(source_platforms, p=platform_weights)

    base = title_salary_base[title]
    salary = base * region_multiplier[region] * experience_multiplier[exp]
    salary *= rng.normal(1.0, 0.12)          # noise
    salary = max(15000, round(salary / 500) * 500)

    n_skills = rng.integers(3, 7)
    skills = rng.choice(ai_skill_pool, size=n_skills, replace=False)
    skills_str = ", ".join(sorted(skills))

    posting_offset = rng.integers(0, date_range_days)
    posting_date = start_date + timedelta(days=int(posting_offset))

    # applicants roughly correlate with remote-friendliness & seniority (entry roles attract more)
    base_applicants = {"Entry": 55, "Mid": 35, "Senior": 18, "Lead": 9}[exp]
    remote_boost = {"Remote": 1.4, "Hybrid": 1.1, "On-site": 0.8}[remote]
    applicants = max(1, int(rng.poisson(base_applicants * remote_boost)))

    company = f"{rng.choice(company_prefixes)}{rng.choice(company_suffixes)}"

    rows.append({
        "job_id": f"JOB{i:05d}",
        "job_title": title,
        "company": company,
        "industry": industry,
        "country": country,
        "region": region,
        "experience_level": exp,
        "remote_type": remote,
        "salary_usd": int(salary),
        "ai_skills_required": skills_str,
        "num_ai_skills": n_skills,
        "applicants": applicants,
        "source_platform": platform,
        "posting_date": posting_date.strftime("%Y-%m-%d"),
    })

df = pd.DataFrame(rows)

# Introduce a small, realistic amount of missing data (as real-world exports have)
missing_idx = rng.choice(df.index, size=int(0.015 * len(df)), replace=False)
df.loc[missing_idx, "applicants"] = np.nan

out_path = "data/ai_job_postings.csv"
df.to_csv(out_path, index=False)
print(f"Generated {len(df)} rows -> {out_path}")
print(df.head())
