from typing import List, Optional, Dict, Any
from llama_index.core.tools import BaseTool
from llama_index.core.agent import ReActAgent
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from .base_agent import BaseAgent
from llama_index.core.llms import ChatMessage
import logging

logger = logging.getLogger(__name__)


class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Coordinator Agent"
        self.goal = "Manage user interaction and orchestrate specialized tools"
        self.agent = None  # To hold the ReActAgent instance
        self.system_prompt = """
    You are the central coordinator for the Coach Intelligence System, acting as the primary interface for the user (a football coach).
    Your primary responsibilities are:
    1.  **Understand User Intent:** Accurately interpret the coach's requests, whether they relate to data retrieval, analysis, planning, or visualization.
    2.  **Task Decomposition & Tool Selection:** Break down complex requests into smaller tasks and intelligently select the appropriate specialized tool(s) (Data Retrieval, Analysis, Planning, Visualization) to handle each task.
    3.  **Orchestration:** Manage the flow of information between tools if necessary.
    4.  **Synthesis & Response:** Synthesize the information and results received from the tools into a single, clear, concise, and actionable response for the coach. Avoid technical jargon where possible.
    5.  **Context Management:** Maintain conversation history to provide relevant and personalized follow-up responses.

    Address the coach directly and professionally. Your goal is to provide seamless assistance, leveraging the specialized agents behind the scenes without exposing the internal mechanics unless necessary for clarification.
    """

    def create(self, additional_tools: Optional[List[BaseTool]] = None) -> Any:
        """
        Create and return a chat-enabled agent with context management
        """
        all_tools = self.tools.copy()
        if additional_tools:
            all_tools.extend(additional_tools)

        # Create and store the ReActAgent instance
        # Let the agent manage its own memory by default
        self.agent = ReActAgent.from_tools(
            tools=all_tools,
            llm=self.llm,
            system_prompt=self.system_prompt,
            verbose=True
        )

        return self  # Return the coordinator instance itself

    def reset_memory(self):
        """Reset the internal agent's state and memory"""
        logger.info("Resetting internal ReActAgent state.")
        if self.agent:
            self.agent.reset()
        else:
            logger.warning("Attempted to reset agent before creation.")

    def load_history(self, messages: List[Dict[str, str]]):
        """Clear agent memory and load historical messages into the agent's memory"""
        if not self.agent:
            logger.error("Agent not created, cannot load history.")
            return

        logger.info(
            f"Loading history into ReActAgent memory ({len(messages)} messages). Resetting agent first.")
        self.agent.reset()  # Reset the agent's state

        # Access the agent's internal memory buffer and load messages
        agent_memory = self.agent.memory
        for msg in messages:
            logger.debug(
                f"Loading message to agent memory: Role={msg['role']}, Content='{msg['content'][:50]}...'")
            agent_memory.put(ChatMessage(
                role=msg["role"],
                content=msg["content"]
            ))
        logger.info("History loading into agent memory complete.")

    def chat(self, message: str) -> Any:
        """Process a chat message using the internal ReActAgent"""
        if not self.agent:
            raise RuntimeError(
                "Agent has not been created. Call create() first.")
        logger.info(
            f"Coordinator routing message to internal ReActAgent: '{message}'")
        # We don't need to pass history explicitly, agent manages its own memory
        return self.agent.chat(message)
