import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class LetterboxdScraper:
    def __init__(self, driver_path="chromedriver.exe", headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def slugify(self, movie_name):
        # Convert movie name to letterboxd URL slug
        return movie_name.lower().translate(
            str.maketrans("", "", r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~""")
        ).replace(" ", "-")

    def clean_text(self, text):
        # Remove URLs and extra whitespace
        text = re.sub(r"http\S+|www\S+|letterboxd.com\S+", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def scrape_movie_reviews(self, movie_name, pages=2):
        movie_slug = self.slugify(movie_name)
        all_reviews = []

        for page in range(1, pages + 1):
            url = f"https://letterboxd.com/film/{movie_slug}/reviews/page/{page}/"
            print(f"Fetching: {url}")
            self.driver.get(url)

            try:
                # Wait for reviews to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.film-reviews li"))
                )
            except Exception as e:
                print(f"Timeout or error loading page: {e}")
                continue

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            reviews = soup.select("ul.film-reviews li")
            print(f"Found {len(reviews)} reviews on page {page}")

            for review in reviews:
                body = review.select_one("div.body-text")
                if body:
                    text = self.clean_text(body.get_text(separator=" "))
                    if len(text) > 20:
                        all_reviews.append({
                            "movie": movie_name,
                            "text": text,
                            "page": page,
                            "url": url,
                        })

            # Be polite to the server
            time.sleep(2)

        print(f"Collected {len(all_reviews)} total reviews for {movie_name}")
        return pd.DataFrame(all_reviews)

    def close(self):
        self.driver.quit()