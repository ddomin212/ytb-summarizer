import textwrap
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
from utils.customllm import GPTv1


st.set_page_config(
    page_title="Youtube Sumarizace skrze ChatGPT",
    page_icon="🤖",
    layout="wide",
)
st.header("Chat with your video!")
link = st.text_input("Youtube Link")

if link:
    loader = YoutubeLoader.from_youtube_url(link)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000)
    docs = text_splitter.split_documents(transcript)

    gptlm = GPTv1()
    # Add map_prompt and combine_prompt to the chain for custom summarization
    chain = load_summarize_chain(gptlm, chain_type="map_reduce")
    print(chain.llm_chain.prompt.template)
    print(chain.combine_document_chain.llm_chain.prompt.template)

    output_summary = chain.run(docs)
    response = textwrap.fill(
        output_summary,
        width=100,
        break_long_words=False,
        replace_whitespace=False,
    )
    st.write(response)
