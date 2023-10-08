"""
This module contains helper functions for generating summaries of youtube videos and comments.
"""
import json
import os
import subprocess
import streamlit as st
from utils.countries import languages_with_flags
from utils.translate import deepl_translate_query

class KaggleAPI:
    def __init__(self, what, type) -> None:
        self.what = what
        self.type = type
        self.is_initialized()

    def is_initialized(self):
        """
        Checks if kaggle is initialized. If not, it initializes it.

        Returns:
            str: "yes" if the kaggle is initialized, "no" otherwise.
        """
        first_time = (
            "no" if os.path.isdir(os.path.join("generated", "dataset")) else "yes"
        )
        self.first_time = first_time
        if first_time == "yes":
            self.create_files()
        return first_time


    def scraper(self):
        """
        Runs a bash script which uploads a jupyter notebook with a Scrapy and Selenium spider to kaggle.
        The script then downloads the output json file.
        """
        self.init_kernel()
        print("Starting Kaggle inference.")
        # run the bash script
        process = subprocess.Popen(
            ["bash", "utils/kaggle.sh", "none", "scraping-kernel"],
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

        print("The script has finished executing.")


    def video_query(self, ilang, olang, link, query="", qlang=None):
        """
        Runs a bash script which uploads the video link along with additional information to kaggle.
        The script then downloads the output text file. The text file is then parsed and returned to the user.

        Args:
            ilang (str): The language of the video.
            olang (str): The language of the output summary.
            what (str): The type of the summary. Either "video" or "comment".
            link (str): The YouTube link of the video.
            typ (str):  The type of the video. Either "chat" or "summarize".
                        Chat is used when you want to ask a question about the video/comment. Summarize is self-explanatory.
            query (str): The query to ask about the video/comment, if the mode is "chat".
            first_time (str): Whether this is the first time the user is using the app. Important for Kaggle initialization.
            qlang (str, optional): The language of the query, if there is one. Defaults to None.

        Returns:
            List[List[str]]: A list of lists representing the rows in the output Excel file.
        """
        if qlang and qlang != ilang:
            query = deepl_translate_query(query, ilang)
        video_metadata = {
            "link": link,
            "type": self.type,
            "query": query,
            "_1PSID": st.session_state._1PSID,
            "_1PSIDTS": st.session_state._1PSIDTS,
            "_1PSIDCC": st.session_state._1PSIDCC,
            "gapi_key": os.getenv("GAPI_KEY"),
            "input_lang": ilang,
            "output_lang": olang,
            "input_lang_code": languages_with_flags[ilang],
            "output_lang_code": languages_with_flags[olang],
        }
        self.init_kernel()
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
            [
                "bash",
                "utils/kaggle.sh",
                self.first_time,
                "cocaster-kernel" if self.what == "video" else "comment-kernel",
            ],
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

        print("The script has finished executing.")
        with open("generated/output/out.txt", encoding="utf-8") as f:
            contents = f.read()
            return contents


    def create_files(self):
        """
        Initializes a Kaggle directory.
        """
        self.init_dataset()
        if not os.path.isdir("generated/kernel"):
            os.mkdir("generated/kernel")
        subprocess.run(
            [
                "cp",
                "static/comment.ipynb",
                "static/cocaster.ipynb",
                "static/scraping.ipynb",
                "generated/kernel/",
            ],
            check=False,
        )
        os.mkdir("generated/output")
        print("Kaggle directory initialized.")


    def init_dataset(self):
        """
        Initializes a Kaggle dataset.
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


    def init_kernel(self):
        """
        Initializes a Kaggle notebook, has to be done every time we upload a new notebook, since there a are two notebooks.
        The first one is for the video summary, the second one is for the comment summary.

        Args:
            what (str): The type of the summary. Either "video" or "comment".
        """
        kernel_name = (
            "cocaster-kernel"
            if self.what == "video"
            else "comment-kernel"
            if self.what == "comment"
            else "scraping-kernel"
        )
        jntb = (
            "cocaster.ipynb"
            if self.what == "video"
            else "comment.ipynb"
            if self.what == "comment"
            else "scraping.ipynb"
        )

        kaggle_metadata = {
            "id": f"dandominko/{kernel_name}",
            "title": kernel_name,
            "code_file": jntb,
            "language": "python",
            "kernel_type": "notebook",
            "is_private": True,
            "enable_gpu": True if self.what != "scraping" else False,
            "enable_internet": True,
            "keywords": ["gpu"],
            "dataset_sources": ["dandominko/cocaster-data"],
            "kernel_sources": [],
            "competition_sources": [],
        }

        json.dump(
            kaggle_metadata,
            open(
                "generated/kernel/kernel-metadata.json",
                "w",
                encoding="utf-8",
            ),
        )

        print("Kaggle kernel initialized.")
