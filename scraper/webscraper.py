import praw
import pandas as pd
from datetime import datetime
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )

    def scrape_movie_reviews(self, movie_name: str, subreddit_list=None, limit=50):
        if subreddit_list is None:
            subreddit_list = ["movies", "MovieDetails", "TrueFilm", "FilmCritics"]

        results = []

        query = f'"{movie_name}"'

        for sub in subreddit_list:
            subreddit = self.reddit.subreddit(sub)
            for post in subreddit.search(query, limit=limit):
                results.append(
                    {
                        "subreddit": sub,
                        "type": "post",
                        "text": post.title,
                        "score": post.score,
                        "url": post.url,
                        "time": datetime.utcfromtimestamp(post.created_utc),
                    }
                )

                post.comments.replace_more(limit=0)
                for comment in post.comments[:10]:
                    results.append(
                        {
                            "subreddit": sub,
                            "type": "comment",
                            "text": comment.body,
                            "score": comment.score,
                            "url": f"https://reddit.com{post.permalink}",
                            "time": datetime.utcfromtimestamp(comment.created_utc),
                        }
                    )

        return pd.DataFrame(results)