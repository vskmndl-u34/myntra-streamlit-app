import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_scraper(input_df: pd.DataFrame) -> pd.DataFrame:

    base_url = "https://www.myntra.com/"
    df = input_df.copy()
    df["Myntra_url"] = base_url + df["Myntra ID"].astype(str)

    # ---------------------------
    # Selenium setup (INSIDE function)
    # ---------------------------
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)

    names = []
    ratings = []
    num_ratings = []
    num_reviews = []

    for url in df["Myntra_url"]:
        try:
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Product Name
            name = soup.find("h1", {"class": "pdp-name"})
            names.append(name.text if name else None)

            # Rating
            rating = soup.find("div", {"class": "index-overallRating"})
            ratings.append(rating.div.text if rating else None)

            # Number of Ratings
            rating_cnt = soup.find("div", {"class": "index-ratingsCount"})
            num_ratings.append(rating_cnt.text[:-7] if rating_cnt else None)

            # Number of Reviews
            review_cnt = soup.find("div", {"class": "detailed-reviews-headline"})
            num_reviews.append(review_cnt.text[18:-1] if review_cnt else None)

        except Exception:
            names.append(None)
            ratings.append(None)
            num_ratings.append(None)
            num_reviews.append(None)

    driver.quit()

    df["Name"] = names
    df["Rating"] = ratings
    df["Number of Ratings"] = num_ratings
    df["Number of Reviews"] = num_reviews

    return df.drop(columns=["Myntra_url"])
