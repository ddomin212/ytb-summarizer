from langchain.agents import create_pandas_dataframe_agent

from utils.customllm import GPTv1


def init_agent(df):
    llm = GPTv1()
    return create_pandas_dataframe_agent(llm, df)


def query(string, agent):
    return agent.run(string)
