from scraper.sentiment import analyze_sentiment

def find_contrarian_reviews(df):
    df = df.copy()
    df['sentiment_score'] = df['text'].apply(analyze_sentiment)

    overall_avg = df['sentiment_score'].mean()
    contrarianity = df['sentiment_score'].std()

    top_positive = df.sort_values('sentiment_score', ascending=False).head(5)
    top_negative = df.sort_values('sentiment_score').head(5)

    return overall_avg, contrarianity, top_positive, top_negative