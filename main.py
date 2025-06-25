from scraper.webscraper import RedditScraper


def main():
    scraper = RedditScraper()
    movie = input("Enter the movie name to scrape reviews for: ")
    df = scraper.scrape_movie_reviews(movie, limit=30)
    output_file = f"{movie.replace(' ', '_').lower()}_reddit_reviews.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} reviews/comments to {output_file}")


if __name__ == "__main__":
    main()