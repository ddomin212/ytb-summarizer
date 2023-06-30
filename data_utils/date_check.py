import datetime
import os
import subprocess


def check_date(date_string):
    """
    Checks if 7 days have passed since the last data update.
    If it has, it updates the date and the data, otherwise it
    just returns the date the data was last updated.

    Args:
        date_string (str): The date of the last data update.

    Returns:
        str: The date of the last data update or today.
    """

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
            ],
            check=False,
        )
        return new_date
    else:
        print("7 days have not passed yet.")
        return date_string
