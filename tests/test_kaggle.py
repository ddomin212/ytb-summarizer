import json
import os
import shutil


def test_is_kaggle_initialized():
    from utils.kaggle import is_kaggle_initialized

    assert is_kaggle_initialized() == "yes"

    shutil.rmtree("generated/dataset")
    shutil.rmtree("generated/kernel")
    shutil.rmtree("generated/output")


def test_init_kaggle():
    from utils.kaggle import init_kaggle

    init_kaggle()
    assert os.path.isdir("generated/kernel")
    assert os.path.isdir("generated/output")
    assert os.path.isfile("generated/kernel/comment.ipynb")
    assert os.path.isfile("generated/kernel/cocaster.ipynb")
    assert os.path.isfile("generated/kernel/scraping.ipynb")

    shutil.rmtree("generated/dataset")
    shutil.rmtree("generated/kernel")
    shutil.rmtree("generated/output")


def test_init_dataset():
    from utils.kaggle import init_dataset

    init_dataset()
    assert os.path.isdir("generated/dataset")
    assert os.path.isfile("generated/dataset/dataset-metadata.json")
    json_dict = json.load(
        open("generated/dataset/dataset-metadata.json", encoding="utf-8")
    )
    assert json_dict == {
        "title": "cocaster-data",
        "id": "dandominko/cocaster-data",
        "licenses": [{"name": "CC0-1.0"}],
    }

    shutil.rmtree("generated/dataset")


def test_init_kernel():
    from utils.kaggle import init_kaggle, init_kernel

    init_kaggle()
    init_kernel("video")
    assert os.path.isdir("generated/kernel")
    assert os.path.isfile("generated/kernel/kernel-metadata.json")
    json_dict = json.load(
        open("generated/kernel/kernel-metadata.json", encoding="utf-8")
    )
    assert json_dict == {
        "id": f"dandominko/cocaster-kernel",
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

    shutil.rmtree("generated/kernel")
