import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def run_scraper(input_df: pd.DataFrame) -> pd.DataFrame:

    base_url = "https://www.myntra.com/"
    input_df = input_df.copy()
    input_df["Myntra_url"] = base_url + input_df["Myntra ID"].astype(str)

    # --- Selenium setup ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    names = []
    ratings = []
    num_ratings = []
    num_reviews = []

    for url in tqdm(input_df["Myntra_url"], desc="Scraping", unit="product"):
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Product Name
        try:
            name = soup.find("h1", {"class": "pdp-name"})
            names.append(name.text if name else None)
        except:
            names.append(None)

        # Rating
        try:
            rating = soup.find("div", {"class": "index-overallRating"})
            ratings.append(rating.div.text if rating else None)
        except:
            ratings.append(None)

        # Number of Ratings
        try:
            rating_cnt = soup.find("div", {"class": "index-ratingsCount"})
            num_ratings.append(rating_cnt.text[:-7] if rating_cnt else None)
        except:
            num_ratings.append(None)

        # Number of Reviews
        try:
            review_cnt = soup.find("div", {"class": "detailed-reviews-headline"})
            num_reviews.append(review_cnt.text[18:-1] if review_cnt else None)
        except:
            num_reviews.append(None)

    driver.quit()

    # Add columns
    input_df["Name"] = names
    input_df["Rating"] = ratings
    input_df["Number of Ratings"] = num_ratings
    input_df["Number of Reviews"] = num_reviews

    return input_df.drop(columns=["Myntra_url"])


