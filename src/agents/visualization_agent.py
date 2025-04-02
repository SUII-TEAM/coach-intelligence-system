from crewai import Agent
from .base_agent import BaseAgent
from ..visualization.visualization_tool import VisualizationTool


class VisualizationAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Visualization Agent"
        self.goal = "Render data and strategies visually"
        self.backstory = """
        You are a specialist in visual communication who can transform complex
        football data and strategies into clear, intuitive visual representations.
        Your visualizations help coaches quickly understand match situations,
        tactical options, and player performances through diagrams, charts, and
        interactive displays.
        """

        # Initialize tools
        self.visualization_tool = VisualizationTool()

    def create(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            llm=self.llm,
            tools=[
                self.visualization_tool.tool
            ]
        )
