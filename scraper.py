import pandas as pd
import requests
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def run_scraper(input_df: pd.DataFrame) -> pd.DataFrame:

    df = input_df.copy()

    names = []
    ratings = []
    rating_counts = []
    review_counts = []

    for pid in df["Myntra ID"]:
        try:
            url = f"https://www.myntra.com/gateway/v2/product/{pid}"
            res = requests.get(url, headers=HEADERS, timeout=20)

            if res.status_code != 200:
                raise Exception("API failed")

            data = res.json()["data"]

            names.append(data.get("name"))

            rating_info = data.get("ratings", {})
            ratings.append(rating_info.get("averageRating"))
            rating_counts.append(rating_info.get("totalCount"))
            review_counts.append(rating_info.get("reviewCount"))

            time.sleep(0.5)

        except Exception:
            names.append(None)
            ratings.append(None)
            rating_counts.append(None)
            review_counts.append(None)

    df["Name"] = names
    df["Rating"] = ratings
    df["Number of Ratings"] = rating_counts
    df["Number of Reviews"] = review_counts

    return df
