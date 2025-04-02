from crewai import Agent
from .base_agent import BaseAgent
from ..tools.planning_tool import PlanningTool


class PlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Planning Agent"
        self.goal = "Design and refine game strategies"
        self.backstory = """
        You are a tactical genius with deep understanding of football strategies.
        Your expertise is in creating formations, set-piece routines, and in-game
        adjustments that exploit opponent weaknesses and maximize team strengths.
        You can adapt quickly to changing match conditions and provide clear,
        actionable tactical advice.
        """

        # Initialize tools
        self.planning_tool = PlanningTool()

    def create(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            llm=self.llm,
            tools=[
                self.planning_tool.tool
            ]
        )
