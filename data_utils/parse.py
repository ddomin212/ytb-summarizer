from functools import partial
from statistics import median

import pandas as pd

from .settings import CLOUD_REGEX, DATA_REGEX, DEVOPS_REGEX, WEB_REGEX


def select_job_position(selected, df, misto, devops, data, web):
    """filters the dataframe according to the selected job position

    Args:
        selected: the job position selected
        df: dataframe with job postings
        misto: selected location
        devops: dictionary of devops technologies
        data: dictionary of data technologies
        web: dictionary of web technologies

    Returns:
        filtered dataframe
    """
    partial_filter = partial(filter_dataframe_tech, df=df, misto=misto)
    if selected == "DevOps":
        tech_data = partial_filter(tech_dict=devops, regex=DEVOPS_REGEX)
    if selected == "Web":
        tech_data = partial_filter(
            tech_dict={**web, **devops}, regex=WEB_REGEX
        )
    if selected == "Data":
        tech_data = partial_filter(
            tech_dict={**data, **devops}, regex=DATA_REGEX
        )
    if selected == "Cloud":
        tech_data = partial_filter(
            tech_dict={**web, **devops}, regex=CLOUD_REGEX
        )
    return tech_data


def filter_dataframe_tech(*, df, misto, tech_dict, regex):
    """Filter the dataframe by the selected technologies for a specific field of work.

    Args:
        df: dataframe
        misto: place you want to filter by
        tech_dict: technologies you want to filter by
        regex: the regex to parse the job description

    Returns:
        dataframe: filtered dataframe
    """
    print(type(regex))
    df = df[df.title.str.contains(regex)]
    tech_data = get_tech(df, misto, tech_dict)
    return tech_data


def in_description(desc, technologies, tech_counts):  # TODO - refactor
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


def get_tech(dataframe, misto, tech_dict):
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
        lambda x: in_description(x, technologies, tech_counts)
    )

    chart_data = pd.DataFrame(tech_counts.items(), columns=["Tech", "Count"])
    chart_data["Branch"] = chart_data.Tech.apply(lambda x: tech_dict[x])
    chart_data = chart_data.sort_values(by="Count", ascending=False)
    return chart_data


def get_pay(dataframe, misto, seniorita):
    """
    Gets the median pay for the selected seniority.

    Args:
        dataframe (pandas.DataFrame): The scraped data.
        seniorita (str): The seniority filter value.

    Returns:
        int: The median pay for the selected seniority.
    """
    if seniorita != "Všechny":
        dataframe = dataframe[
            dataframe.title.str.contains(seniorita, case=False)
        ]
    if misto != "Celá ČR":
        dataframe = dataframe[dataframe.title.str.contains(misto, case=False)]
    print(dataframe.shape)
    med_arr = dataframe[dataframe.pay != "Unknown"].pay.values.tolist()
    median_pay = median(med_arr)
    print(median_pay)
    return int(median_pay)


def get_locations(dataframe, misto, seniorita):
    """
    Gets the locations from the scraped job descriptions.

    Args:
        dataframe (pandas.DataFrame): The scraped data.
        seniorita (str): The seniority filter value.

    Returns:
        pandas.Series: A Series containing the locations and their counts.
    """
    if seniorita != "Všechny":
        dataframe = dataframe[
            dataframe.title.str.contains(seniorita, case=False)
        ]
    if misto != "Celá ČR":
        dataframe = dataframe[dataframe.title.str.contains(misto, case=False)]
    locations = (
        dataframe.location.str.replace(r"(?:\s\+\s|\s–\s).*", "", regex=True)
        .str.replace("Hlavní město ", "", regex=False)
        .value_counts()
    )
    return locations
