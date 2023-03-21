import urllib
from google.cloud import bigquery
import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup

import urllib.request
import os
import string
import random
import reddit
from reddit import FLAIR_ID
import polars as pl

from foxwq import FOXWQ_NEWS_URL, FOXWQ_URL
from dnutils import is_valid_url

page = requests.get(FOXWQ_NEWS_URL)

if page.status_code != 200:
    print("Error: ", page.status_code)
    sys.exit(1)


soup = BeautifulSoup(page.content, 'html.parser')

times = [elem.text for elem in soup.find_all("span", class_='news-time')]
titles = [elem.find("a").text for elem in soup.find_all(
    "div", class_='news-title')]
urls = [elem.find("a")["href"]
        for elem in soup.find_all("div", class_='news-title')]

# if you download the page on the same date then times is the timestamp HH:MM instead of MM-DD
latest_date = [t for t in times if "-" in t][0]
if len([t for t in times if ":" in t]) > 0:
    latest_date = [t for t in times if "-" in t][0]
    if latest_date == "12-31":
        latest_date = "01-01"


def swap_time_for_date(t):
    if ":" in t:
        return latest_date
    else:
        return t


times_for_df = [swap_time_for_date(t) for t in times]

# for each of the urls in urls, download the page and extract the content
df = pl.DataFrame({"date": times_for_df, "titles": titles, "urls": urls})



# extrac the latest from biqquery
print("Just before authentication")

# Construct a BigQuery client object.
client = bigquery.Client()

print("Got past authentication")

query = """
    SELECT
        *
    FROM
        `testing-of-bigquery.shoulderhit.daily_news`
    where
        date in (
            select
                max(date)
            from
                `testing-of-bigquery.shoulderhit.daily_news`
                )
"""
query_job = client.query(query)  # Make an API request.

latest_bq = pl.from_pandas(query_job.to_dataframe())#.to_parquet('latest-daily-news.parquet')

latest_date = latest_bq.get_column("date")[0]

# compare the latest from bq with the from the fox website
new_stories = df.filter(pl.col("date") >= latest_date).join(
    latest_bq.select(["urls"]), on="urls", how="anti")


# df = pl.read_parquet("todays-news.parquet")

"""Extract pis from the url"""
def extract_pics(url, verbose=False):
    page = requests.get(FOXWQ_URL + url)
    if page.status_code != 200:
        print("Error: ", page.status_code)
        sys.exit(1)
    soup = BeautifulSoup(page.content, 'html.parser')
    elems = soup.find_all("img")

    if verbose:
        print(f"# pictures {len(elems)}")


    images = [elem["src"] for elem in elems if is_valid_url(elem["src"])]
    tmp_dir = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    output_dir = os.path.join("./tmp", tmp_dir)
    os.makedirs(output_dir)
    images_paths = [os.path.join(".", "tmp", tmp_dir, str(i)+".peg")
                    for (i, _) in enumerate(images)]
    for image, tmp_file in zip(images, images_paths):
        urllib.request.urlretrieve(image, tmp_file)

    return output_dir


url = new_stories["urls"][0]

chinese_title = new_stories["titles"][0]
english_titles = []

for (chinese_title, url) in zip(new_stories["titles"], new_stories["urls"]):
    print(f"Downloding pics from {url}")
    pic_path = extract_pics(url)
    print(pic_path)
    title = input(f"Translate this into English\n{chinese_title}\n")
    english_titles.append(title)

    print("submitting now:")
    reddit.submit_gallery_by_folder(title, pic_path)

new_stories = new_stories.to_pandas()

new_stories["english_tiles"] = english_titles

pl.from_pandas(new_stories).write_parquet("todays-news.parquet")
