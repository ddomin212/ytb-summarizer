"""
This module contains helper functions for inference of the uploaded PDF file.
"""
import subprocess
import json
import os
import pandas as pd


def is_kaggle_initialized():
    first_time = (
        "no" if os.path.isdir(os.path.join("generated", "dataset")) else "yes"
    )
    if first_time == "yes":
        init_kaggle()
    return first_time


def get_kaggle(link, typ, query, first_time):
    """
    Runs a bash script to extract named entities from a PDF
    file uploaded to the app, with a spacy NER model inside a
    Kaggle Notebook for faster inference. The extracted entities
    are returned as a list of lists, where each inner list represents
    a row in the output Excel file.

    Args:
        uploaded_file (FileStorage): The uploaded PDF file.
        first_time (str): A string indicating whether this is the first time the
                                script is being run. Necessary for the Kaggle API.

    Returns:
        List[List[str]]: A list of lists representing the rows in the output Excel file.
    """
    video_metadata = {
        "link": link,
        "type": typ,
        "query": query,
        "token": os.getenv("OPEN_AI_TOKEN"),
    }
    json.dump(
        video_metadata,
        open(
            "generated/dataset/data.json",
            "w",
            encoding="utf-8",
        ),
    )
    print("Starting Kaggle inference.")
    # run the bash script
    process = subprocess.Popen(
        ["bash", "utils/kaggle.sh", first_time],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())

    while True:
        error = process.stderr.readline()
        if error == "" and process.poll() is not None:
            break
        if error:
            print(error.strip())
    # continue with Python code
    print("The script has finished executing.")
    with open("generated/output/out.txt") as f:
        contents = f.read()
        return contents


def init_kaggle():
    """
    Initializes a Kaggle notebook for the given user email.

    Args:
        user_email (str): The email of the user to initialize the notebook for.
    """
    init_dataset()
    init_kernel()
    os.mkdir("generated/output")
    print("Kaggle directory initialized.")


def init_dataset():
    """
    Initializes a Kaggle dataset.

    Args:
        None
    """
    os.mkdir("generated/dataset")
    kaggle_metadata = {
        "title": "cocaster-data",
        "id": "dandominko/cocaster-data",
        "licenses": [{"name": "CC0-1.0"}],
    }
    json.dump(
        kaggle_metadata,
        open(
            "generated/dataset/dataset-metadata.json",
            "w",
            encoding="utf-8",
        ),
    )
    print("Kaggle dataset initialized.")


def init_kernel():
    """
    Initializes a Kaggle kernel.

    Args:
        None
    """
    os.mkdir("generated/kernel")
    kaggle_metadata = {
        "id": "dandominko/cocaster-kernel",
        "title": "cocaster-kernel",
        "code_file": "cocaster.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "keywords": ["gpu"],
        "dataset_sources": ["dandominko/cocaster-data"],
        "kernel_sources": [],
        "competition_sources": [],
    }
    subprocess.run(
        [
            "cp",
            "cocaster.ipynb",
            "generated/kernel/cocaster.ipynb",
        ],
        check=False,
    )
    json.dump(
        kaggle_metadata,
        open(
            "generated/kernel/kernel-metadata.json",
            "w",
            encoding="utf-8",
        ),
    )
    print("Kaggle kernel initialized.")
