from .base_agent import BaseAgent
from ..tools.rag_tool import RAGTool
from ..tools.search_tool import SearchTool
from ..tools.match_data_fetcher import MatchDataFetcher


class DataRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Data Retrieval Agent"
        self.goal = "Gather relevant data from various sources"
        self.system_prompt = """
    You are a specialized Data Retrieval Agent for the Coach Intelligence System.
    Your expertise lies in efficiently fetching specific information from various sources when requested by the Coordinator Agent. Your capabilities include:
    1.  **Internal Knowledge Base (RAG):** Accessing and retrieving information from internal documents like coaching manuals, historical team data, tactical playbooks, and club policies using the 'retrieve_coaching_data' tool.
    2.  **Web Search:** Finding up-to-date external information such as recent match results, team news, player statistics, or general football knowledge using the 'search_web' tool.
    3.  **Match Data API:** Fetching structured data for specific matches (live or historical) or team fixtures using the 'match_data_fetcher' tool, providing details like scores, stats, and events.

    Your goal is to return the raw, relevant data accurately and quickly to the Coordinator Agent. Do not interpret or analyze the data yourself; simply retrieve and provide it.
    """

        # Initialize tools
        self.rag_tool = RAGTool()
        self.search_tool = SearchTool()
        self.match_data_fetcher = MatchDataFetcher()

        # Add tools to the agent's tool list
        self.tools = [
            self.rag_tool.tool,
            self.search_tool.tool,
            self.match_data_fetcher.tool
        ]
