from googlesearch import search
import streamlit as st
import pandas as pd
from datetime import datetime

SEARCH_QUERY = 'site:linkedin.com/jobs "procurement analyst" (California OR Tampa OR Remote)'
NUM_RESULTS = 20  # Adjust as needed

@st.cache_data(ttl=86400)
def run_google_search():
    results = []
    for url in search(SEARCH_QUERY, num_results=NUM_RESULTS, lang="en"):
        results.append({
            "title": url.split("/")[-1].replace("-", " ").title(),
            "url": url,
            "date_logged": datetime.now().strftime("%Y-%m-%d")
        })
    return results

st.title("🔎 Google Job Search Log")
jobs = run_google_search()

if jobs:
    df = pd.DataFrame(jobs)
    st.write(df)

    # Optional: save to log file
    df.to_csv("job_log.csv", mode="a", header=False, index=False)
    st.success("✅ Logged job links")

else:
    st.warning("No results found.")
