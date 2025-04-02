from crewai import Agent
from .base_agent import BaseAgent
from ..tools.match_data_analyzer import MatchDataAnalyzer


class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Analysis Agent"
        self.goal = "Interpret data to provide actionable insights"
        self.backstory = """
        You are a highly skilled football analyst with expertise in interpreting match data.
        Your specialty is taking raw statistics and events, finding patterns and insights,
        and converting them into actionable recommendations for coaches.
        You can spot trends in team and player performance that others might miss.
        """

        # Initialize tools
        self.match_data_analyzer = MatchDataAnalyzer()

    def create(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            llm=self.llm,
            tools=[
                self.match_data_analyzer.tool
            ]
        )
