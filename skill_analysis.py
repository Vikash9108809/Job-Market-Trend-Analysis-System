import pandas as pd
from collections import Counter

df = pd.read_parquet("data/processed/jobs_cleaned.parquet")

skills_series = df["job_skills"].dropna()

skill_counter = Counter()

for skills in skills_series:
    for skill in str(skills).split(","):
        skill = skill.strip().lower()
        if skill and skill != "nan":
            skill_counter[skill] += 1

top_skills = pd.DataFrame(
    skill_counter.most_common(30),
    columns=["skill", "count"]
)

top_skills.to_csv("data/processed/top_skills.csv", index=False)

print(top_skills)