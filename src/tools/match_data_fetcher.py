import os
import json
import requests
from langchain.tools import Tool
from datetime import datetime


class MatchDataFetcher:
    def __init__(self):
        self.name = "match_data_fetcher"
        self.description = """
        Use this tool to retrieve real-time or historical match data.
        This is useful for accessing live game statistics, scores, and player performance metrics.
        """
        # In a real implementation, we would use an actual API key
        # self.api_key = os.getenv("API_FOOTBALL_KEY")

        # Create the tool
        self.tool = Tool.from_function(
            func=self.fetch_match_data,
            name=self.name,
            description=self.description
        )

    def fetch_match_data(self, match_id=None, team_name=None):
        """
        Fetch match data from api-football (or mock data for prototype)

        Args:
            match_id (str, optional): The ID of the match to fetch data for
            team_name (str, optional): The name of the team to fetch recent matches for

        Returns:
            str: Match data as a formatted string
        """
        try:
            # For the prototype, we'll use mock data
            # In a real implementation, we would make API calls like:
            # url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?id={match_id}"
            # headers = {
            #     "x-rapidapi-key": self.api_key,
            #     "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
            # }
            # response = requests.get(url, headers=headers)
            # data = response.json()

            if match_id:
                return self._mock_live_match_data(match_id)
            elif team_name:
                return self._mock_team_recent_matches(team_name)
            else:
                return self._mock_upcoming_matches()

        except Exception as e:
            return f"Error fetching match data: {str(e)}"

    def _mock_live_match_data(self, match_id):
        """Generate mock data for a live match"""
        # Different mock data based on match_id to simulate different matches
        if match_id == "123456":
            return json.dumps({
                "match_id": "123456",
                "status": "LIVE",
                "minute": 65,
                "home_team": {
                    "name": "Manchester United",
                    "score": 2,
                    "possession": 48,
                    "shots_on_target": 5,
                    "corners": 4,
                    "cards": {"yellow": 2, "red": 0}
                },
                "away_team": {
                    "name": "Liverpool",
                    "score": 1,
                    "possession": 52,
                    "shots_on_target": 3,
                    "corners": 6,
                    "cards": {"yellow": 1, "red": 0}
                },
                "events": [
                    {"minute": 12, "type": "goal", "team": "Manchester United",
                        "player": "Bruno Fernandes"},
                    {"minute": 37, "type": "goal", "team": "Liverpool",
                        "player": "Mohamed Salah"},
                    {"minute": 52, "type": "goal",
                        "team": "Manchester United", "player": "Marcus Rashford"}
                ]
            }, indent=2)
        else:
            return json.dumps({
                "match_id": match_id or "654321",
                "status": "LIVE",
                "minute": 32,
                "home_team": {
                    "name": "Arsenal",
                    "score": 0,
                    "possession": 61,
                    "shots_on_target": 2,
                    "corners": 3,
                    "cards": {"yellow": 0, "red": 0}
                },
                "away_team": {
                    "name": "Chelsea",
                    "score": 1,
                    "possession": 39,
                    "shots_on_target": 3,
                    "corners": 2,
                    "cards": {"yellow": 2, "red": 0}
                },
                "events": [
                    {"minute": 18, "type": "goal",
                        "team": "Chelsea", "player": "Kai Havertz"}
                ]
            }, indent=2)

    def _mock_team_recent_matches(self, team_name):
        """Generate mock data for a team's recent matches"""
        if team_name.lower() == "manchester united":
            return json.dumps({
                "team": "Manchester United",
                "recent_matches": [
                    {"date": "2023-10-22", "competition": "Premier League",
                        "opponent": "Liverpool", "result": "W 2-1", "possession": 48},
                    {"date": "2023-10-18", "competition": "Champions League",
                        "opponent": "Bayern Munich", "result": "L 0-1", "possession": 42},
                    {"date": "2023-10-14", "competition": "Premier League",
                        "opponent": "Brentford", "result": "W 3-0", "possession": 65},
                    {"date": "2023-10-07", "competition": "Premier League",
                        "opponent": "Fulham", "result": "D 1-1", "possession": 57},
                    {"date": "2023-10-03", "competition": "Champions League",
                        "opponent": "Galatasaray", "result": "L 2-3", "possession": 68}
                ]
            }, indent=2)
        else:
            return json.dumps({
                "team": team_name or "Arsenal",
                "recent_matches": [
                    {"date": "2023-10-22", "competition": "Premier League",
                        "opponent": "Chelsea", "result": "D 1-1", "possession": 58},
                    {"date": "2023-10-18", "competition": "Champions League",
                        "opponent": "Sevilla", "result": "W 2-0", "possession": 65},
                    {"date": "2023-10-14", "competition": "Premier League",
                        "opponent": "Bournemouth", "result": "W 1-0", "possession": 72},
                    {"date": "2023-10-08", "competition": "Premier League",
                        "opponent": "Manchester City", "result": "L 0-2", "possession": 43},
                    {"date": "2023-10-03", "competition": "Champions League",
                        "opponent": "Lens", "result": "W 3-1", "possession": 62}
                ]
            }, indent=2)

    def _mock_upcoming_matches(self):
        """Generate mock data for upcoming matches"""
        return json.dumps({
            "upcoming_matches": [
                {"date": "2023-10-28", "competition": "Premier League",
                    "home": "Newcastle", "away": "Arsenal"},
                {"date": "2023-10-28", "competition": "Premier League",
                    "home": "Manchester United", "away": "Manchester City"},
                {"date": "2023-10-29", "competition": "Premier League",
                    "home": "Liverpool", "away": "Tottenham"},
                {"date": "2023-10-29", "competition": "Premier League",
                    "home": "Chelsea", "away": "Brentford"},
                {"date": "2023-10-30", "competition": "Premier League",
                    "home": "Fulham", "away": "West Ham"}
            ]
        }, indent=2)
