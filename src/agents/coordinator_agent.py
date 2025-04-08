from typing import List, Optional, Dict, Any
from llama_index.core.tools import BaseTool
from llama_index.core.agent import ReActAgent
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Coordinator Agent"
        self.goal = "Manage user interaction and orchestrate specialized tools"
        self.memory = ChatMemoryBuffer.from_defaults()
        self.system_prompt = """
        You are the central hub of the Coach Intelligence System. Your job is to understand
        coach requests, break them down into tasks, and utilize appropriate tools to
        provide a cohesive answer to the coach.
        
        You have access to various specialized tools for:
        - Data Retrieval: Gathering data from various sources
        - Analysis: Interpreting data for actionable insights
        - Planning: Designing and refining game strategies
        - Visualization: Rendering data and strategies visually
        
        Process each request by deciding which tools to use and in what order.
        Synthesize the information you get from different sources into a clear, 
        actionable response.
        
        Maintain context from previous interactions to provide more relevant and
        personalized responses.
        """

    def create(self, additional_tools: Optional[List[BaseTool]] = None) -> Any:
        """
        Create and return a chat-enabled agent with context management
        """
        all_tools = self.tools.copy()
        if additional_tools:
            all_tools.extend(additional_tools)

        # Create a chat engine with memory
        chat_engine = SimpleChatEngine.from_defaults(
            llm=self.llm,
            system_prompt=self.system_prompt,
            memory=self.memory,
            tools=all_tools,
            chat_mode=ChatMode.REACT
        )

        return chat_engine

    def reset_memory(self):
        """Reset the conversation memory"""
        self.memory.reset()
