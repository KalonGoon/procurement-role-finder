# streamlit_app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json

SEARCH_URLS = [
    "https://www.indeed.com/jobs?q=procurement+analyst+remote+California",
    "https://www.indeed.com/jobs?q=procurement+analyst+remote+Tampa",
    # Add LinkedIn or ZipRecruiter URLs as needed
]

@st.cache_data(ttl=3600)
def fetch_jobs(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for div in soup.find_all("div", class_="jobsearch-SerpJobCard"):
        title = div.find("a", class_="jobtitle").text.strip()
        company = div.find("span", class_="company").text.strip()
        loc = div.find("div", class_="location").text.strip()
        link = "https://indeed.com" + div.find("a")["href"]
        jobs.append({"title": title, "company": company, "location": loc, "link": link})
    return jobs

def main():
    st.title("🛠️ Procurement Analytics Job Tracker")
    jobs = []
    for url in SEARCH_URLS:
        jobs += fetch_jobs(url)
    st.write(f"Found {len(jobs)} jobs")
    for job in jobs:
        st.write(f"[**{job['title']}**]({job['link']}) – {job['company']} | {job['location']}")

    if st.button("Show me new jobs"):
        new = fetch_jobs(SEARCH_URLS[0])
        st.write(f"Latest from CA: {len(new)} jobs")
        for j in new[:5]:
            st.write(f"- {j['title']} at {j['company']}")

if __name__ == "__main__":
    main()
