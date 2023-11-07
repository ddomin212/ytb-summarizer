from functools import partial
from statistics import median
import json

import pandas as pd

from ..settings import CLOUD_REGEX, DATA_REGEX, DEVOPS_REGEX, WEB_REGEX

class Parser:
    def __init__(self, misto, seniorita):
        self.misto = misto
        self.seniorita = seniorita
        self.load_data()

    def load_data(self):
        """Loads the scraped data from Kaggle API from the generated/scraped/jobs_cz_docs.json file."""
        with open(
            "generated/scraped/jobs_cz_docs.json", "r", encoding="utf-8"
        ) as f:
            json_data = json.load(f)
        with open("static/devops_technologies.json", "r", encoding="utf-8") as f:
            self.devops = json.load(f)
        with open("static/data_technologies.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        with open("static/web_technologies.json", "r", encoding="utf-8") as f:
            self.web = json.load(f)
        self.df = pd.DataFrame(json_data)

    def select_job_position(self, selected):
        """filters the dataframe according to the selected job position
        """
        partial_filter = partial(self.filter_dataframe_tech, df=self.df, misto=self.misto)
        if selected == "DevOps":
            regex = DEVOPS_REGEX
            tech_data = partial_filter(tech_dict=self.devops, regex=regex)
        if selected == "Web":
            regex = WEB_REGEX
            tech_data = partial_filter(
                tech_dict={**self.web, **self.devops}, regex=regex
            )
        if selected == "Data":
            regex = DATA_REGEX
            tech_data = partial_filter(
                tech_dict={**self.data, **self.devops}, regex=regex
            )
        if selected == "Cloud":
            regex = CLOUD_REGEX
            tech_data = partial_filter(
                tech_dict={**self.web, **self.devops}, regex=regex
            )
        return tech_data, regex


    def filter_dataframe_tech(self, *, df, misto, tech_dict, regex):
        """Filter the dataframe by the selected technologies for a specific field of work.

        Args:
            df: dataframe
            misto: place you want to filter by
            tech_dict: technologies you want to filter by
            regex: the regex to parse the job description

        Returns:
            dataframe: filtered dataframe
        """
        df = df[df.title.str.contains(regex)]
        tech_data = self.get_tech(df, misto, tech_dict)
        return tech_data


    def in_description(self, desc, technologies, tech_counts):
        """
        Counts the total number of technologies in all the scraped job descriptions.

        Args:
            desc (str): The required technologies from the job description.
            technologies (list): A list of all possible technologies.
            tech_counts (dict): A dictionary containing the technologies as keys and the count as values.
        """
        for w in desc:
            if w in technologies:
                tech_counts[w] = tech_counts.get(w, 0) + 1


    def get_tech(self, dataframe, misto, tech_dict):
        """
        Gets the technologies from the scraped job descriptions.

        Args:
            dataframe (pandas.DataFrame): The scraped data.
            misto (str): The location filter value.
            tech_dict (dict): A dictionary containing the technologies as keys and their branch as values.
                                Example - {"Node": "Backend", "Docker": "DevOps"}

        Returns:
            pandas.DataFrame: A DataFrame containing the technologies and their counts.
        """
        technologies = [x for x in tech_dict.keys()]
        tech_counts = {}
        if misto != "Celá ČR":
            dataframe = dataframe[
                dataframe.location.str.contains(misto, case=False)
            ]

        dataframe.req_tech.apply(
            lambda x: self.in_description(x, technologies, tech_counts)
        )

        chart_data = pd.DataFrame(tech_counts.items(), columns=["Tech", "Count"])
        chart_data["Branch"] = chart_data.Tech.apply(lambda x: tech_dict[x])
        chart_data = chart_data.sort_values(by="Count", ascending=False)
        return chart_data


    def get_pay(self, regex):
        """
        Gets the median pay for the selected seniority.
        """
        dataframe = self.df[self.df.title.str.contains(regex)]
        if self.seniorita != "Všechny":
            dataframe = dataframe[
                dataframe.title.str.contains(self.seniorita, case=False)
            ]
        if self.misto != "Celá ČR":
            dataframe = dataframe[dataframe.title.str.contains(self.misto, case=False)]
        print(dataframe.shape)
        med_arr = dataframe[dataframe.pay != "Unknown"].pay.values.tolist()
        median_pay = median(med_arr)
        print(median_pay)
        return int(median_pay)


    def get_locations(self, regex):
        """
        Gets the locations from the scraped job descriptions.

        Args:
            dataframe (pandas.DataFrame): The scraped data.
            seniorita (str): The seniority filter value.

        Returns:
            pandas.Series: A Series containing the locations and their counts.
        """
        dataframe = self.df[self.df.title.str.contains(regex)]
        if self.seniorita != "Všechny":
            dataframe = dataframe[
                dataframe.title.str.contains(self.seniorita, case=False)
            ]
        if self.misto != "Celá ČR":
            dataframe = dataframe[dataframe.title.str.contains(self.misto, case=False)]
        locations = (
            dataframe.location.str.replace(r"(?:\s\+\s|\s–\s).*", "", regex=True)
            .str.replace("Hlavní město ", "", regex=False)
            .value_counts()
        )
        return locations
