import os
from crewai import Agent
import google.generativeai as genai


class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.llm = "gemini-2.5-pro"  # Using Gemini 2.5 Pro

    def create(self):
        """
        Create and return a CrewAI agent with specific role and tools
        This method should be implemented by subclasses
        """
        raise NotImplementedError(
            "Subclasses must implement the create method")
