from scraper.webscraper import RedditScraper

def main():
    scraper = RedditScraper()
    movie = input("Enter the movie name to scrape reviews for: ")
    df = scraper.scrape_movie_reviews(movie, limit=30)

    filename = f"{movie.replace(' ', '_').lower()}_reddit_reviews.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} posts and comments to '{filename}'.")

if __name__ == "__main__":
    main()