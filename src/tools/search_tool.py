from llama_index.core.tools import FunctionTool
from langchain_community.utilities import SerpAPIWrapper
import os
import json


class SearchTool:
    def __init__(self):
        self.name = "search_web"
        self.description = """
        Use this tool to search the web for information not available in internal documents.
        This is useful for finding recent match results, news about teams, or player statistics.
        """
        # Initialize SerpAPI for web search
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        self.search = self._initialize_search_engine()
        self.tool = FunctionTool.from_defaults(
            name=self.name,
            description=self.description,
            fn=self.search_web
        )

    def _initialize_search_engine(self):
        """
        Initialize the search engine using SerpAPI
        Returns a mock search function if no API key is available
        """
        if self.serpapi_key:
            try:
                # Use LangChain's SerpAPIWrapper as it's well-tested
                return SerpAPIWrapper(serpapi_api_key=self.serpapi_key)
            except Exception as e:
                print(f"Error initializing SerpAPI: {str(e)}")
                return None
        else:
            print("No SerpAPI key found, using mock search results")
            return None

    def _mock_search(self, query):
        """
        Provide mock search results when no API key is available
        """
        # Mock data for common football-related queries
        mock_data = {
            "formation": """
            Common Football Formations:
            1. 4-4-2: Traditional formation with solid defensive and offensive balance
            2. 4-3-3: Attacking formation with width in the final third
            3. 3-5-2: Formation with wingbacks providing width and solid midfield presence
            4. 4-2-3-1: Modern formation with defensive midfielders and attacking midfield trio
            5. 5-3-2: Defensive formation with five at the back
            """,
            "manchester united": """
            Manchester United F.C. is an English professional football club based in Old Trafford, Greater Manchester.
            - Founded: 1878 (as Newton Heath LYR F.C.)
            - Stadium: Old Trafford (capacity: 74,140)
            - Current Manager: Erik ten Hag
            - League: Premier League
            - Recent Form: Mixed results in recent matches
            - Key Players: Bruno Fernandes, Marcus Rashford, Alejandro Garnacho
            """,
            "premier league": """
            The Premier League is the top tier of English football.
            - Founded: 1992
            - Teams: 20
            - Current Champion: Manchester City
            - Most Championships: Manchester United (13)
            - Top Scorers: Erling Haaland, Cole Palmer, Alexander Isak
            - Recent Matches: Various results across the league
            """,
            "tactics": """
            Modern Football Tactics:
            1. Gegenpressing: High-intensity pressing to win the ball back quickly after losing possession
            2. Tiki-Taka: Possession-based approach with short passing and movement
            3. Counter-attacking: Defending deep and attacking quickly on transition
            4. Positional Play: Structured approach to manipulating space and creating passing lanes
            5. Fluid Attack: Flexible forward movement with interchanging positions
            """,
            "default": """
            Football (Soccer) Information:
            - Most popular sport globally with an estimated 3.5 billion fans
            - Governed by FIFA internationally
            - Major competitions include the FIFA World Cup, UEFA Champions League, and domestic leagues
            - Top leagues: Premier League (England), La Liga (Spain), Bundesliga (Germany), Serie A (Italy)
            - Modern game continues to evolve with tactical innovations and technological advancements
            """
        }

        # Find the most relevant mock data based on keywords in the query
        query_lower = query.lower()
        for keyword, data in mock_data.items():
            if keyword in query_lower:
                return {
                    "query": query,
                    "source": "Mock Search Engine",
                    "results": data
                }

        # Return default data if no matches
        return {
            "query": query,
            "source": "Mock Search Engine",
            "results": mock_data["default"]
        }

    def search_web(self, query):
        """
        Search the web for information based on the query

        Args:
            query (str): The search query

        Returns:
            str: Search results from the web
        """
        try:
            if self.search:
                # Use SerpAPI if available
                results = self.search.run(query)
                return results
            else:
                # Use mock search if no API key
                mock_results = self._mock_search(query)
                return json.dumps(mock_results, indent=2)
        except Exception as e:
            error_msg = f"Error searching the web: {str(e)}"
            print(error_msg)
            return error_msg
