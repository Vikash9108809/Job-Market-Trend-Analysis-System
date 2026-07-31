import pandas as pd
import os

RAW_PATH = "data/raw/linkedin_job_postings.csv"
SKILLS_PATH = "data/raw/job_skills.csv"
OUTPUT_PATH = "data/processed/jobs_cleaned.parquet"

os.makedirs("data/processed", exist_ok=True)

use_cols = [
    "job_link",
    "job_title",
    "company",
    "job_location",
    "first_seen",
    "search_city",
    "search_country",
    "search_position",
    "job_level",
    "job_type"
]

print("Loading skills file...")
skills = pd.read_csv(SKILLS_PATH, usecols=["job_link", "job_skills"])
skills["job_skills"] = skills["job_skills"].fillna("").astype(str).str.lower()

processed_chunks = []

print("Processing job postings in chunks...")

for i, chunk in enumerate(pd.read_csv(RAW_PATH, usecols=use_cols, chunksize=100000)):
    print(f"Processing chunk {i + 1}")

    chunk = chunk.drop_duplicates(subset=["job_link"])

    text_cols = [
        "job_title",
        "company",
        "job_location",
        "search_city",
        "search_country",
        "search_position",
        "job_level",
        "job_type"
    ]

    for col in text_cols:
        chunk[col] = chunk[col].fillna("").astype(str).str.lower().str.strip()

    chunk["first_seen"] = pd.to_datetime(chunk["first_seen"], errors="coerce")
    chunk = chunk.dropna(subset=["first_seen"])

    chunk = chunk.merge(skills, on="job_link", how="left")
    chunk["job_skills"] = chunk["job_skills"].fillna("")

    processed_chunks.append(chunk)

print("Combining chunks...")
df = pd.concat(processed_chunks, ignore_index=True)

print("Saving cleaned data...")
df.to_parquet(OUTPUT_PATH, index=False)

print("Done!")
print("Saved to:", OUTPUT_PATH)
print("Final shape:", df.shape)