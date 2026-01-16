import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

def run_scraper(input_df: pd.DataFrame) -> pd.DataFrame:

    base_url = "https://www.myntra.com/"
    df = input_df.copy()
    df["Myntra_url"] = base_url + df["Myntra ID"].astype(str)

    names, ratings, num_ratings, num_reviews = [], [], [], []

    for url in df["Myntra_url"]:
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(response.text, "html.parser")

            # Product Name
            name = soup.find("h1", {"class": "pdp-name"})
            names.append(name.text if name else None)

            # Rating
            rating = soup.find("div", {"class": "index-overallRating"})
            ratings.append(rating.text if rating else None)

            # Number of Ratings
            rating_cnt = soup.find("div", {"class": "index-ratingsCount"})
            num_ratings.append(rating_cnt.text[:-7] if rating_cnt else None)

            # Number of Reviews
            review_cnt = soup.find("div", {"class": "detailed-reviews-headline"})
            num_reviews.append(review_cnt.text[18:-1] if review_cnt else None)

            time.sleep(1)  # polite delay

        except Exception:
            names.append(None)
            ratings.append(None)
            num_ratings.append(None)
            num_reviews.append(None)

    df["Name"] = names
    df["Rating"] = ratings
    df["Number of Ratings"] = num_ratings
    df["Number of Reviews"] = num_reviews

    return df.drop(columns=["Myntra_url"])
