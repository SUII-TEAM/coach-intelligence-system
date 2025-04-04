import json
from llama_index.core.tools import FunctionTool


class MatchDataAnalyzer:
    def __init__(self):
        self.name = "analyze_match_data"
        self.description = """
        Use this tool to analyze match data and provide tactical insights.
        This is useful for interpreting statistics, identifying patterns, and suggesting adjustments.
        """

        # Create the tool
        self.tool = FunctionTool.from_defaults(
            name=self.name,
            description=self.description,
            fn=self.analyze_match_data
        )

    def analyze_match_data(self, match_data):
        """
        Analyze match data to provide tactical insights

        Args:
            match_data (str): JSON-formatted match data (from Match Data Fetcher)

        Returns:
            str: Analysis and recommendations
        """
        try:
            # Parse the match data JSON
            data = None
            if isinstance(match_data, str):
                data = json.loads(match_data)
            else:
                data = match_data

            # Check what type of data we have and analyze accordingly
            if "status" in data and data.get("status") == "LIVE":
                return self._analyze_live_match(data)
            elif "recent_matches" in data:
                return self._analyze_team_form(data)
            elif "upcoming_matches" in data:
                return "Analysis of upcoming matches is not yet implemented."
            else:
                return "Unable to determine the type of match data provided."

        except Exception as e:
            return f"Error analyzing match data: {str(e)}"

    def _analyze_live_match(self, data):
        """Analyze live match data and provide tactical recommendations"""
        home_team = data["home_team"]["name"]
        away_team = data["away_team"]["name"]
        minute = data["minute"]
        home_score = data["home_team"]["score"]
        away_score = data["away_team"]["score"]

        home_possession = data["home_team"]["possession"]
        away_possession = data["away_team"]["possession"]

        home_shots = data["home_team"]["shots_on_target"]
        away_shots = data["away_team"]["shots_on_target"]

        analysis = f"Match Analysis: {home_team} vs {away_team} (Minute {minute})\n\n"
        analysis += f"Current Score: {home_team} {home_score} - {away_score} {away_team}\n\n"

        # Add possession analysis
        analysis += "Possession Analysis:\n"
        if abs(home_possession - away_possession) <= 5:
            analysis += "• Possession is evenly balanced. Focus on quality of possession in attacking areas.\n"
        elif home_possession > away_possession:
            analysis += f"• {home_team} is dominating possession ({home_possession}%). "
            if home_score <= away_score:
                analysis += "Need to be more direct and create more clear-cut chances.\n"
            else:
                analysis += "Continue controlling the tempo and look for opportunities to extend the lead.\n"
        else:
            analysis += f"• {away_team} is dominating possession ({away_possession}%). "
            if home_score >= away_score:
                analysis += f"{home_team} should focus on counterattacks and set pieces.\n"
            else:
                analysis += f"{home_team} needs to press more effectively to regain possession.\n"

        # Add shot analysis
        analysis += "\nShooting Analysis:\n"
        shot_efficiency_home = home_score / home_shots if home_shots > 0 else 0
        shot_efficiency_away = away_score / away_shots if away_shots > 0 else 0

        if home_shots > away_shots + 3:
            analysis += f"• {home_team} creating more chances ({home_shots} shots on target vs {away_shots}).\n"
        elif away_shots > home_shots + 3:
            analysis += f"• {away_team} creating more chances ({away_shots} shots on target vs {home_shots}).\n"
        else:
            analysis += f"• Both teams creating similar number of chances ({home_shots} vs {away_shots} shots on target).\n"

        # Add tactical recommendations
        analysis += "\nTactical Recommendations:\n"

        # Based on score
        if home_score > away_score + 1:
            analysis += f"• {home_team} should consider a more defensive formation (e.g., switch to 5-3-2) to protect the lead.\n"
        elif away_score > home_score + 1:
            analysis += f"• {home_team} should switch to a more attacking formation (e.g., 4-3-3 or 3-4-3) to create more chances.\n"

        # Based on possession
        if home_possession < 40:
            analysis += f"• {home_team} struggling to maintain possession. Consider adding an extra midfielder for control.\n"
        elif home_possession > 65:
            analysis += f"• {home_team} has strong possession but needs to be more direct in the final third.\n"

        # Additional situational advice
        if minute > 75:
            if home_score == away_score:
                analysis += "• Consider making attacking substitutions for a late push to win.\n"
            elif abs(home_score - away_score) == 1:
                if home_score > away_score:
                    analysis += "• Potential to bring on defensive reinforcements to secure the result.\n"
                else:
                    analysis += "• All-out attack recommended - consider removing a defender for an additional attacker.\n"

        return analysis

    def _analyze_team_form(self, data):
        """Analyze a team's recent form and provide insights"""
        team_name = data["team"]
        matches = data["recent_matches"]

        # Calculate basic stats
        total_matches = len(matches)
        wins = sum(1 for match in matches if match["result"].startswith("W"))
        losses = sum(1 for match in matches if match["result"].startswith("L"))
        draws = sum(1 for match in matches if match["result"].startswith("D"))

        win_percentage = (wins / total_matches) * \
            100 if total_matches > 0 else 0
        avg_possession = sum(match.get("possession", 0)
                             for match in matches) / total_matches if total_matches > 0 else 0

        # Generate analysis
        analysis = f"Form Analysis: {team_name}\n\n"
        analysis += f"Recent Results: {wins} wins, {draws} draws, {losses} losses ({win_percentage:.1f}% win rate)\n"
        analysis += f"Average Possession: {avg_possession:.1f}%\n\n"

        # Analyze form trend
        recent_results = [match["result"][0]
                          for match in matches]  # W, L, or D
        trend = "".join(recent_results)

        analysis += "Form Trend Analysis:\n"
        if trend.startswith("W"):
            analysis += f"• {team_name} starting matches well - capitalize on confidence early in games.\n"
        if trend.endswith("L"):
            analysis += f"• Recent loss may affect team morale - focus on positive reinforcement.\n"
        if "WW" in trend:
            analysis += "• Team showing ability to maintain momentum - build on this consistency.\n"
        if "LL" in trend:
            analysis += "• Consecutive losses indicate potential tactical or fitness issues to address.\n"

        # Competition-specific analysis
        premier_league_matches = [
            m for m in matches if m["competition"] == "Premier League"]
        champions_league_matches = [
            m for m in matches if m["competition"] == "Champions League"]

        if premier_league_matches:
            pl_wins = sum(
                1 for m in premier_league_matches if m["result"].startswith("W"))
            pl_matches = len(premier_league_matches)
            analysis += f"\nPremier League Form: {pl_wins} wins from {pl_matches} matches.\n"

        if champions_league_matches:
            cl_wins = sum(
                1 for m in champions_league_matches if m["result"].startswith("W"))
            cl_matches = len(champions_league_matches)
            analysis += f"Champions League Form: {cl_wins} wins from {cl_matches} matches.\n"

        # Tactical recommendations
        analysis += "\nTactical Recommendations Based on Form:\n"

        if win_percentage >= 60:
            analysis += "• Team in good form - maintain tactical approach but prepare for opponents adapting.\n"
        elif win_percentage <= 30:
            analysis += "• Consider significant tactical changes or formation shift to reverse poor form.\n"
        else:
            analysis += "• Mixed form suggests need for minor tactical adjustments based on opponent.\n"

        if avg_possession > 60:
            analysis += "• Strong possession stats - focus on converting possession into clear chances.\n"
        elif avg_possession < 45:
            analysis += "• Lower possession approach - optimize counterattacking and set piece opportunities.\n"

        return analysis
