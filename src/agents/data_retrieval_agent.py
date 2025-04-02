from crewai import Agent
from .base_agent import BaseAgent
from ..tools.rag_tool import RAGTool
from ..tools.search_tool import SearchTool
from ..tools.match_data_fetcher import MatchDataFetcher


class DataRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Data Retrieval Agent"
        self.goal = "Gather relevant data from various sources"
        self.backstory = """
        You are a specialist in retrieving information from multiple sources.
        Your expertise is in finding the most relevant and up-to-date data from 
        internal documents, real-time match feeds, and external websites.
        You aggregate this data to provide a comprehensive information package
        for other agents to analyze and use.
        """

        # Initialize tools
        self.rag_tool = RAGTool()
        self.search_tool = SearchTool()
        self.match_data_fetcher = MatchDataFetcher()

    def create(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            llm=self.llm,
            tools=[
                self.rag_tool.tool,
                self.search_tool.tool,
                self.match_data_fetcher.tool
            ]
        )
