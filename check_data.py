import pandas as pd

files = [
    "data/raw/linkedin_job_postings.csv",
    "data/raw/job_skills.csv",
    "data/raw/job_summary.csv"
]

for file in files:
    print("\nFILE:", file)
    df = pd.read_csv(file, nrows=5)
    print(df.columns.tolist())
    print(df.head())