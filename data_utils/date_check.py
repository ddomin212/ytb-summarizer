import datetime
import os
import subprocess


def check_date(date_string):
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
        return new_date
    else:
        print("7 days have not passed yet.")
        return date_string
