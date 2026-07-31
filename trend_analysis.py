import pandas as pd
import os

INPUT_PATH = "data/processed/jobs_cleaned.parquet"

os.makedirs("data/processed", exist_ok=True)

df = pd.read_parquet(INPUT_PATH)

df["first_seen"] = pd.to_datetime(df["first_seen"], errors="coerce")
df = df.dropna(subset=["first_seen"])

df["date"] = df["first_seen"].dt.date.astype(str)
df["month"] = df["first_seen"].dt.to_period("M").astype(str)

daily_jobs = (
    df.groupby("date")
    .size()
    .reset_index(name="job_count")
    .sort_values("date")
)

monthly_jobs = (
    df.groupby("month")
    .size()
    .reset_index(name="job_count")
    .sort_values("month")
)

daily_jobs.to_csv("data/processed/daily_job_trends.csv", index=False)
monthly_jobs.to_csv("data/processed/monthly_job_trends.csv", index=False)

print("Daily trend rows:", len(daily_jobs))
print(daily_jobs.head())

print("Monthly trend rows:", len(monthly_jobs))
print(monthly_jobs.head())