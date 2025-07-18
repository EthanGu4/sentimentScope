import matplotlib.pyplot as plt

def plot_sentiment_distribution(df, movie_name):
    plt.hist(df['sentiment_score'], bins=20, color='skyblue', edgecolor='black')
    plt.title(f"Sentiment Score Distribution for {movie_name}")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Number of Reviews")
    plt.show()