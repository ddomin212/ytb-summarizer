import json
import re
from statistics import median

with open(f"jobs_cz.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open("devops_technologies.json", "r", encoding="utf-8") as f:
    devops = json.load(f)
with open("data_technologies.json", "r", encoding="utf-8") as f:
    data = json.load(f)
with open("web_technologies.json", "r", encoding="utf-8") as f:
    web = json.load(f)


def extract_pay(pay_range):
    cleaned_range = re.sub(r"[^\d\s]", "", pay_range)

    values = cleaned_range.split()

    int_values = [int(val) for val in values if int(val) != 0]

    median_value = median(int_values)

    return int(median_value * 1000)


def get_bigrams(text):
    # Split the text into individual words
    words = text.split()

    # Create a list to store the bigrams
    bigrams = []

    # Iterate through the words to generate bigrams
    for i in range(len(words) - 1):
        # Concatenate adjacent words to form a bigram
        bigram = (words[i], words[i + 1])

        # Append the bigram to the list
        bigrams.append(bigram)

    return bigrams


def keep_alphanumeric_space(text):
    # Use regex to keep only words, digits, and spaces
    cleaned_text = re.sub(r"[^\w\s\d.]", "", text)
    return cleaned_text


ultra_dict = {**data, **devops, **web}
tech = ultra_dict.keys()
new_dict = []
for idx, i in enumerate(json_data):
    i["tech"] = []
    txt_low = (
        i["text"].lower() + " " + keep_alphanumeric_space(i["title"].lower())
    )
    unigrams = txt_low.split(" ")
    bigrams = get_bigrams(txt_low)
    for q in unigrams:
        if q in tech and q not in i["tech"]:
            i["tech"] += [q]
    for q in bigrams:
        if q in tech and q not in i["tech"]:
            i["tech"] += [q]
    new_data = {
        "title": i["title"],
        "comapny": i["comapny"],
        "location": i["location"],
        "pay": extract_pay(i["pay_range"]) if i["pay_range"] else "Unknown",
        "req_tech": i["tech"],
        "text": i["text"],
        "url": i["url"],
    }
    new_dict.append(new_data)
with open("jobs_cz_docs.json", "w", encoding="utf-8") as f:
    json.dump(new_dict, f, ensure_ascii=False, indent=4)
