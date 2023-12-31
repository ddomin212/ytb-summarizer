import json
import re
from statistics import median


def process_json_file(file_path):
    """
    Process a JSON file and return a dictionary

    Args:
        file_path (str): The path to the JSON file

    Returns:
        dict: A dictionary containing the JSON data
    """
    with open(file_path, "r", encoding="utf-8") as file:
        # Read the JSON file as a string
        json_string = file.read()

    # Remove combinations: "\n][\n", "]\n", and "[\n"
    modified_string = json_string.replace("\n][\n", ",\n")

    # Load the modified string as a dictionary
    data = json.loads(modified_string)

    return data


def extract_pay(pay_range):
    """
    Extract the median pay from a pay range

    Args:
        pay_range (str): A string containing the pay range

    Returns:
        int: The median pay
    """
    cleaned_range = re.sub(r"[^\d\s]", "", pay_range)

    values = cleaned_range.split()

    int_values = [int(val) for val in values if int(val) != 0]

    median_value = median(int_values)

    return int(median_value * 1000)


def get_bigrams(text):
    """
    Generate bigrams from a text. Useful later for extracting technologies
    that are not single words, for example: "google bigquery".

    Args:
        text (str): The text to generate bigrams from

    Returns:
        list: A list of bigrams
    """
    # Split the text into individual words
    words = text.split()

    # Create a list to store the bigrams
    bigrams = []

    # Iterate through the words to generate bigrams
    for i in range(len(words) - 1):
        # Concatenate adjacent words to form a bigram
        bigram = (words[i].strip(), words[i + 1].strip())

        # Append the bigram to the list
        bigrams.append(bigram)

    return bigrams


def keep_alphanumeric_space(text):
    """
    Keep only alphanumeric characters and spaces in a text

    Args:
        text (str): The text to clean

    Returns:
        str: The cleaned text
    """
    # Use regex to keep only words, digits, and spaces
    cleaned_text = re.sub(r"[^\w\s\d.]", "", text)
    return cleaned_text


def write_updated_json():
    """
    Write the edited JSON file to generated/scraped/jobs_cz_docs.json
    The formt of the JSON file is as follows:
    [
        {
            "title": "Data Scientist",
            "company": "Google",
            "location": "Prague",
            "pay": 100000,
            "text": "This is a job description",
            "req_tech": ["python", "sql", "bigquery"]
            "url": "https://www.jobs.cz/12345"
        },
        ...
    ]

    Returns:
        None
    """
    file_path = "generated/scraped/jobs_cz.json"
    json_data = process_json_file(file_path)

    with open("static/devops_technologies.json", "r", encoding="utf-8") as f:
        devops = json.load(f)
    with open("static/data_technologies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("static/web_technologies.json", "r", encoding="utf-8") as f:
        web = json.load(f)

    ultra_dict = {**data, **devops, **web}
    tech = ultra_dict.keys()
    new_dict = []
    for _, i in enumerate(json_data):
        i["tech"] = []
        txt_low = (
            keep_alphanumeric_space(i["text"].lower())
            + " "
            + keep_alphanumeric_space(i["title"].lower())
        )
        unigrams = txt_low.split(" ")
        bigrams = get_bigrams(txt_low)
        for q in unigrams:
            q = q.strip()
            for j in tech:
                if q in j and q not in i["tech"]:
                    i["tech"] += [q]
        for q in bigrams:
            if q in tech and q not in i["tech"]:
                i["tech"] += [q]
        new_data = {
            "title": i["title"],
            "comapny": i["comapny"],
            "location": i["location"],
            "pay": extract_pay(i["pay_range"])
            if i["pay_range"]
            else "Unknown",
            "req_tech": i["tech"],
            "text": i["text"],
            "url": i["url"],
        }
        new_dict.append(new_data)
    with open(
        "generated/scraped/jobs_cz_docs.json", "w", encoding="utf-8"
    ) as f:
        json.dump(new_dict, f, ensure_ascii=False, indent=4)
