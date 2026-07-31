import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib
import os

os.makedirs("models", exist_ok=True)

df = pd.read_parquet("data/processed/jobs_cleaned.parquet")

df["combined_text"] = (
    df["job_title"].fillna("") + " " +
    df["search_position"].fillna("") + " " +
    df["job_skills"].fillna("") + " " +
    df["job_level"].fillna("") + " " +
    df["job_type"].fillna("")
)

df = df[df["combined_text"].str.strip() != ""]
df = df.head(50000)

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english"
)

X = vectorizer.fit_transform(df["combined_text"])

model = NearestNeighbors(
    n_neighbors=10,
    metric="cosine"
)

model.fit(X)

joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(model, "models/job_recommender.pkl")
df[["job_title", "company", "job_location", "job_skills", "job_type", "job_level", "job_link"]].to_parquet(
    "models/recommendation_data.parquet",
    index=False
)

print("Model trained successfully")