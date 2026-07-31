import joblib
import pandas as pd

vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/job_recommender.pkl")
jobs = pd.read_parquet("models/recommendation_data.parquet")

def recommend_jobs(user_skills):
    query = " ".join(user_skills)
    query_vector = vectorizer.transform([query])

    distances, indices = model.kneighbors(query_vector)

    results = jobs.iloc[indices[0]].copy()
    results["match_score"] = 1 - distances[0]

    return results