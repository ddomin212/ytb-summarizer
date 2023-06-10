import os
from typing import Any, List, Mapping, Optional
from revChatGPT.V1 import Chatbot
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM


class GPTv1(LLM):
    chatbot = Chatbot(
        config={
            "access_token": os.getenv("OPEN_AI_KEY"),
        }
    )

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        print(prompt)
        response = ""
        for data in self.chatbot.ask(prompt):
            response = data["message"]
        print("actually using revChatGPT")
        return response
