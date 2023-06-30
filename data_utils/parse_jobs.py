from statistics import median

import pandas as pd


def in_description(desc, technologies, tech_counts):
    """
    Counts the total number of technologies in all the scraped job descriptions.

    Args:
        desc (str): The required technologies from the job description.
        technologies (list): A list of all possible technologies.
        tech_counts (dict): A dictionary containing the technologies as keys and the count as values.
    """
    for word in desc:
        if word in technologies:
            tech_counts[word] = tech_counts.get(word, 0) + 1


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
    technologies = tech_dict.keys()
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


def get_pay(dataframe, seniorita):
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
    print(dataframe.shape)
    med_arr = dataframe[dataframe.pay != "Unknown"].pay.values.tolist()
    median_pay = median(med_arr)
    print(median_pay)
    return int(median_pay)


def get_locations(dataframe, seniorita):
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
    locations = (
        dataframe.location.str.replace(r"(?:\s\+\s|\s–\s).*", "", regex=True)
        .str.replace("Hlavní město ", "", regex=False)
        .value_counts()
    )
    return locations
