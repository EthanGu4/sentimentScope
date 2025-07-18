import streamlit as st
import pandas as pd
import os
from scraper.sentiment import analyze_sentiment
from analysis.contrarian import find_contrarian_reviews
from scraper.webscraper import RedditScraper
import re

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|reddit.com\S+|/u/\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def analyze_movie_reviews(movie_name, limit=10):
    scraper = RedditScraper()
    df = scraper.scrape_movie_reviews(movie_name, limit=limit)
    if df.empty:
        return None

    df["text"] = df["text"].apply(clean_text)
    df = df[df["text"].str.len() > 25]

    if df.empty:
        return None

    avg_sentiment, contrarianity, top_pos, top_neg = find_contrarian_reviews(df)

    return {
        "avg_score": avg_sentiment,
        "contrarianity": contrarianity,
        "top_positive": top_pos["text"].tolist(),
        "top_negative": top_neg["text"].tolist()
    }


st.set_page_config(page_title="Movie Sentiment Analyzer 🎬", layout="wide")
st.title("🎥 Movie Review Sentiment Analyzer")

movie = st.text_input("Enter a movie name:", "Oppenheimer")

if st.button("Analyze"):
    with st.spinner("Scraping and analyzing Reddit reviews..."):
        result = analyze_movie_reviews(movie)

    if result is None:
        st.error("No reviews found or not enough data.")
    else:
        st.success("Analysis complete!")

        st.subheader(f"🎯 Average Sentiment Score: `{result['avg_score']:.2f}`")
        st.subheader(f"📉 Contrarianity: `{result['contrarianity']:.2f}`")

        st.markdown("### 🟢 Top Positive Comments")
        for text in result["top_positive"]:
            st.success(text)

        st.markdown("### 🔴 Top Negative Comments")
        for text in result["top_negative"]:
            st.error(text)