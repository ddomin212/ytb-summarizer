import json
import re
from statistics import median

import pandas as pd


def in_description(desc, technologies, tech_counts):
    for w in desc:
        if w in technologies:
            tech_counts[w] = tech_counts.get(w, 0) + 1


# def extract_pay(pay_range):
#     cleaned_range = re.sub(r"[^\d\s]", "", pay_range)

#     values = cleaned_range.split()

#     int_values = [int(val) for val in values if int(val) != 0]

#     median_value = median(int_values)

#     return median_value


# def parse_title(t, positions):
#     for w in positions:
#         if w.lower() in t.lower():
#             return True
#     return False


# def position_select(
#     df, position
# ):  # TODO: asi spíš rozdělit nástroje než pozice
#     if position == "Data Analyst":
#         positions = [
#             "analytik",
#             "analyst",
#             "analyzuj",
#             "analýza",
#             "analýzy",
#             "Excel",
#             "SQL",
#             "Power BI",
#             "Tableau",
#         ]
#     elif position == "Data Scientist":
#         positions = [
#             "scien",
#             "věde",
#             "věda",
#             "machine",
#             "ML",
#             "strojov",
#             "uměl",
#             "tensorflow",
#             "pytorch",
#             "jax",
#         ]
#     elif position == "Data Engineer":
#         positions = [
#             "data engineer",
#             "databáz" "governance",
#             "airflow",
#             "dataops",
#             "warehouse",
#             "dwh",
#         ]
#     df = df[df.title.apply(lambda x: parse_title(x, positions))]
#     return df


def get_tech(dataframe, misto, tech_dict):
    technologies = [x for x in tech_dict.keys()]
    tech_counts = {}
    # json.dump(
    #     {k.lower(): v for k, v in data_dict.items()},
    #     open("data_technologies.json", "w", encoding="utf-8"),
    # )
    # json.dump(
    #     {k.lower(): v for k, v in devops_dict.items()},
    #     open("devops_technologies.json", "w", encoding="utf-8"),
    # )
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
    if seniorita != "Všechny":
        dataframe = dataframe[
            dataframe.title.str.contains(seniorita, case=False)
        ]
    print(dataframe.shape)
    med_arr = dataframe[dataframe.pay != "Unknown"].pay.values.tolist()
    median_pay = median(med_arr)
    print(median_pay)
    return int(median_pay)


def get_locations(dataframe, misto, seniorita):
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
