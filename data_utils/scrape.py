import datetime
import json
import os
import subprocess

import pandas as pd


def scrape_new_data():
    """
    Checks if 7 days have passed since the last data update.
    If it has, it updates the date and the data, otherwise it
    just returns the date the data was last updated.
    """
    date_string = os.getenv("START_DATE")

    # Convert string to date object
    date = datetime.datetime.strptime(
        date_string, "%Y-%m-%d"  # os.getenv("START_DATE")
    ).date()

    # Get today's date
    today = datetime.date.today()

    # Calculate the timedelta between the dates
    delta = today - date

    if delta.days >= 7:
        # Update the date with the new one
        new_date = today.strftime("%Y-%m-%d")
        print("7 days have passed. Updating the date to", new_date)
        if not os.path.isdir(os.path.join("generated", "scraped")):
            os.mkdir("generated/scraped")
        subprocess.run(
            [
                "kaggle",
                "kernels",
                "output",
                "jobs-scraper",
                "-p",
                "generated/scraped",
            ]
        )
        os.environ["START_DATE"] = new_date
    else:
        print("7 days have not passed yet.")


def load_data():
    """
    Loads the scraped data from Kaggle API from the generated/scraped/jobs_cz_docs.json file.

    Returns:
        tuple: A tuple of four elements. The first one is a pandas DataFrame,
                the other three are dictionaries containing the various technologies
                related to the dictionary variable name.
    """
    with open(
        "generated/scraped/jobs_cz_docs.json", "r", encoding="utf-8"
    ) as f:
        json_data = json.load(f)
    with open("static/devops_technologies.json", "r", encoding="utf-8") as f:
        devops = json.load(f)
    with open("static/data_technologies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("static/web_technologies.json", "r", encoding="utf-8") as f:
        web = json.load(f)
    df = pd.DataFrame(json_data)
    return df, devops, data, web
