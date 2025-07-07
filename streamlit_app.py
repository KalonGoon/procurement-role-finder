import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from datetime import datetime

# -------------------------------
# SETUP
# -------------------------------
st.set_page_config(page_title="Procurement Job Finder", page_icon="🔎")
st.title("🔎 Procurement Job Finder via Google Search")

params = {
    "engine": "google",
    "q": 'site:linkedin.com/jobs "procurement analyst" (remote OR tampa OR california)',
    "hl": "en",
    "num": 15,
    "api_key": st.secrets["SERPAPI_KEY"]
}

# -------------------------------
# SEARCH FUNCTION
# -------------------------------
@st.cache_data(ttl=86400)
def fetch_search_results():
    search = GoogleSearch(params)
    results = search.get_dict()
    links = []
    for r in results.get("organic_results", []):
        links.append({
            "title": r.get("title"),
            "url": r.get("link"),
            "source": "Google",
            "date_logged": datetime.now().strftime("%Y-%m-%d")
        })
    return links

# -------------------------------
# MAIN APP
# -------------------------------
st.info("Searching Google for new job listings...")

results = fetch_search_results()

if results:
    df = pd.DataFrame(results)
    st.success(f"✅ Found {len(df)} job listings!")
    st.dataframe(df)

    # Save to CSV log
    df.to_csv("job_log.csv", mode="a", header=False, index=False)
    st.caption("🗃️ Results appended to job_log.csv")

else:
    st.warning("No results found. Try adjusting your query or check your API key.")
