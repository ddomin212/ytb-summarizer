import pytest


@pytest.mark.skip()
def test_ideation_prompt():
    from utils.ideation import video_ideation

    abstract = (
        "I want to create a video about the best places to visit in Prague."
    )
    script, title, thumb = video_ideation(abstract)
    assert isinstance(script, str)
    assert isinstance(title, str)
    assert isinstance(thumb, str)


def test_no_translate():
    from utils.translate import deepl_translate_query

    text = "I want to create a video about the best places to visit in Prague."
    input_lang = "English"
    translated_text = deepl_translate_query(text, input_lang)
    assert isinstance(translated_text, str)
    assert translated_text == text


def test_translate():
    from utils.translate import deepl_translate_query

    text = "Zdravím, jak se máš?"
    input_lang = "English"
    translated_text = deepl_translate_query(text, input_lang)
    assert isinstance(translated_text, str)
    assert translated_text == "Hi, how are you?"
