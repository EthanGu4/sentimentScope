import os
import re
import pandas as pd
from scraper.webscraper import RedditScraper
from scraper.sentiment import analyze_sentiment  # import sentiment helper
from analysis.contrarian import find_contrarian_reviews  # import contrarian finder

def clean_text(text):
    # Remove URLs and Reddit mentions
    text = re.sub(r"http\S+|www\S+|reddit.com\S+|/u/\S+", "", text)
    # Remove extra whitespace, lowercase
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def scrape_movies(movie_list, limit=5):
    scraper = RedditScraper()
    all_data = []

    for movie in movie_list:
        print(f"\n📽 Scraping reviews for: {movie}")
        df = scraper.scrape_movie_reviews(movie, limit=limit)
        df["movie"] = movie
        df["text"] = df["text"].apply(clean_text)
        df = df[df["text"].str.len() > 25]

        if df.empty:
            print(f"No reviews found for {movie}")
            continue

        # --- SENTIMENT ANALYSIS & CONTRARIAN FINDER ---
        print(f"🧠 Analyzing sentiment and finding contrarian reviews for {movie}...")
        avg_sentiment, contrarianity, top_positive, top_negative = find_contrarian_reviews(df)

        print(f"Overall average sentiment score: {avg_sentiment:.3f}")
        print(f"Contrarianity (std dev): {contrarianity:.3f}")

        print("\nTop Positive Reviews:")
        for _, row in top_positive.iterrows():
            print(f"  (+{row.sentiment_score:.2f}) {row.text[:150]}...")

        print("\nTop Negative Reviews:")
        for _, row in top_negative.iterrows():
            print(f"  ({row.sentiment_score:.2f}) {row.text[:150]}...")

        # Save each movie's results individually
        filename = f"data/{movie.replace(' ', '_').lower()}_reviews.csv"
        os.makedirs("data", exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(df)} cleaned rows to {filename}")

        all_data.append(df)

    # Save combined dataset for model training
    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        full_df.to_csv("data/all_movies_reviews.csv", index=False)
        print(f"\n🎉 Saved full dataset with {len(full_df)} rows to data/all_movies_reviews.csv")

if __name__ == "__main__":
    movie_list = [
        "Inception",
        "The Matrix",
        "Oppenheimer",
        "Barbie",
        "Interstellar"
    ]
    scrape_movies(movie_list)