/* =========================================================================
   AI Job Market Analysis — SQL Analysis Queries
   Database: database/ai_jobs.db   |   Table: job_postings
   Run with: sqlite3 database/ai_jobs.db < sql/analysis_queries.sql
   ========================================================================= */

-- 1. Highest paying AI job titles (avg salary, rounded)
SELECT
    job_title,
    ROUND(AVG(salary_usd), 0)  AS avg_salary_usd,
    COUNT(*)                   AS num_postings
FROM job_postings
GROUP BY job_title
ORDER BY avg_salary_usd DESC;


-- 2. Average salary by experience level
SELECT
    experience_level,
    ROUND(AVG(salary_usd), 0) AS avg_salary_usd,
    COUNT(*)                  AS num_postings
FROM job_postings
GROUP BY experience_level
ORDER BY avg_salary_usd DESC;


-- 3. Remote vs Hybrid vs On-site: salary and demand comparison
SELECT
    remote_type,
    ROUND(AVG(salary_usd), 0)     AS avg_salary_usd,
    ROUND(AVG(applicants), 1)     AS avg_applicants,
    COUNT(*)                      AS num_postings
FROM job_postings
GROUP BY remote_type
ORDER BY num_postings DESC;


-- 4. Top hiring regions by number of postings and average salary
SELECT
    region,
    COUNT(*)                   AS num_postings,
    ROUND(AVG(salary_usd), 0)  AS avg_salary_usd
FROM job_postings
GROUP BY region
ORDER BY num_postings DESC;


-- 5. Industry demand for AI roles
SELECT
    industry,
    COUNT(*) AS num_postings,
    ROUND(AVG(salary_usd), 0) AS avg_salary_usd
FROM job_postings
GROUP BY industry
ORDER BY num_postings DESC;


-- 6. Monthly posting trend (seasonality of AI hiring across 2025)
SELECT
    strftime('%Y-%m', posting_date) AS month,
    COUNT(*) AS num_postings
FROM job_postings
GROUP BY month
ORDER BY month;


-- 7. Most in-demand AI skills (requires splitting the comma-separated column;
--    SQLite has no native STRING_SPLIT, so this is easiest done in pandas —
--    see notebooks/ai_job_market_analysis.ipynb, Section 4.
--    Kept here as a reference query for the raw skills field:)
SELECT ai_skills_required, COUNT(*) AS num_postings
FROM job_postings
GROUP BY ai_skills_required
ORDER BY num_postings DESC
LIMIT 10;


-- 8. Competitiveness: average applicants per posting by experience level
SELECT
    experience_level,
    ROUND(AVG(applicants), 1) AS avg_applicants,
    ROUND(AVG(salary_usd), 0) AS avg_salary_usd
FROM job_postings
WHERE applicants IS NOT NULL
GROUP BY experience_level
ORDER BY avg_applicants DESC;


-- 9. Best-paying job title + region combinations (top 10)
SELECT
    job_title,
    region,
    ROUND(AVG(salary_usd), 0) AS avg_salary_usd,
    COUNT(*) AS num_postings
FROM job_postings
GROUP BY job_title, region
HAVING num_postings >= 5
ORDER BY avg_salary_usd DESC
LIMIT 10;


-- 10. Which source platform yields the most postings, and at what average salary?
SELECT
    source_platform,
    COUNT(*) AS num_postings,
    ROUND(AVG(salary_usd), 0) AS avg_salary_usd
FROM job_postings
GROUP BY source_platform
ORDER BY num_postings DESC;
