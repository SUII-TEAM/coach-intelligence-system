import os
from typing import List, Optional
from llama_index.core.agent import ReActAgent
from llama_index.llms.gemini import Gemini
from llama_index.core.tools import BaseTool
from llama_index.core.agent.types import BaseAgentWorker


class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.llm = Gemini(api_key=self.api_key,
                          model_name="models/gemini-2.0-flash")
        self.system_prompt = "You are an AI assistant."
        self.tools = []

    def get_tools(self) -> List[BaseTool]:
        """
        Get the tools that this agent provides

        Returns:
            List[BaseTool]: List of tools provided by this agent
        """
        return self.tools

    def create(self, additional_tools: Optional[List[BaseTool]] = None) -> BaseAgentWorker:
        """
        Create and return a LlamaIndex agent with specific role and tools

        Args:
            additional_tools: Optional list of additional tools to add to the agent

        Returns:
            BaseAgentWorker: The created agent worker
        """
        all_tools = self.tools.copy()
        if additional_tools:
            all_tools.extend(additional_tools)

        return ReActAgent.from_tools(
            tools=all_tools,
            llm=self.llm,
            system_prompt=self.system_prompt,
            verbose=True
        )
