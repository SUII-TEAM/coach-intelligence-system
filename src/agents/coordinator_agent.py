from typing import List, Optional
from llama_index.core.tools import BaseTool
from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Coordinator Agent"
        self.goal = "Manage user interaction and orchestrate specialized tools"
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
        """
