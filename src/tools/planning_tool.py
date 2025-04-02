from langchain.tools import Tool
import json


class PlanningTool:
    def __init__(self):
        self.name = "planning_tool"
        self.description = """
        Use this tool to generate strategic recommendations like formations, tactics, and set pieces.
        This is useful for creating game plans based on team stats and match context.
        """

        # Create the tool
        self.tool = Tool.from_function(
            func=self.generate_strategy,
            name=self.name,
            description=self.description
        )

        # Define common formations and their characteristics
        self.formations = {
            "4-4-2": {
                "description": "Traditional balanced formation with two strikers",
                "strengths": ["Balanced defense and attack", "Good width", "Simple to understand"],
                "weaknesses": ["Can be overrun in midfield", "Less flexibility"],
                "suitable_for": ["Teams with strong strikers", "When balance is needed"]
            },
            "4-3-3": {
                "description": "Attack-oriented formation with three forwards",
                "strengths": ["Strong attacking presence", "Wingers provide width", "Control in midfield"],
                "weaknesses": ["Wingers must track back", "Can leave fullbacks exposed"],
                "suitable_for": ["Teams with strong wingers", "Possession-based teams", "When goals are needed"]
            },
            "3-5-2": {
                "description": "Formation with three center-backs and wing-backs",
                "strengths": ["Strong central defense", "Numerical advantage in midfield", "Wing-backs provide width"],
                "weaknesses": ["Wing-backs must be very fit", "Can be vulnerable to quick transitions"],
                "suitable_for": ["Teams facing superior opponents", "When midfield control is crucial"]
            },
            "5-3-2": {
                "description": "Very defensive formation with five defenders",
                "strengths": ["Very solid defense", "Good for counterattacking", "Protects a lead"],
                "weaknesses": ["Limited attacking options", "Can invite pressure"],
                "suitable_for": ["Protecting a lead", "Against stronger attacking teams"]
            },
            "4-2-3-1": {
                "description": "Modern formation with two defensive midfielders",
                "strengths": ["Balanced attack and defense", "Strong central midfield", "Flexible in attack"],
                "weaknesses": ["Relies on strong no. 10 player", "Single striker can get isolated"],
                "suitable_for": ["Teams with a strong attacking midfielder", "Modern possession-based approach"]
            }
        }

        # Define tactical approaches
        self.tactics = {
            "High Press": {
                "description": "Aggressively pressure opponents in their own half",
                "strengths": ["Forces turnovers in dangerous areas", "Disrupts opponent buildup"],
                "weaknesses": ["Physically demanding", "Can leave spaces behind"],
                "suitable_for": ["Fit teams", "Against teams that build from the back"]
            },
            "Counter Attack": {
                "description": "Defend deep and strike quickly when possession is won",
                "strengths": ["Exploits spaces left by attacking teams", "Effective against possession teams"],
                "weaknesses": ["Requires fast players", "Less possession", "Can invite pressure"],
                "suitable_for": ["Teams with pace in attack", "Against possession-heavy opponents"]
            },
            "Possession": {
                "description": "Keep the ball and patiently build attacks",
                "strengths": ["Controls the game tempo", "Tires opponents", "Creates chances through combinations"],
                "weaknesses": ["Can be predictable", "Requires technical players"],
                "suitable_for": ["Technically skilled teams", "When controlling the game is important"]
            },
            "Direct Play": {
                "description": "Move the ball forward quickly, often with long passes",
                "strengths": ["Bypasses opponent press", "Creates quick chances", "Unpredictable"],
                "weaknesses": ["Lower possession", "Less control", "Requires target forwards"],
                "suitable_for": ["Teams with strong target forwards", "Against high-pressing teams"]
            },
            "Low Block": {
                "description": "Defend deep in a compact shape",
                "strengths": ["Very solid defensively", "Difficult to break down", "Good for protecting leads"],
                "weaknesses": ["Limited attacking opportunities", "Invites pressure"],
                "suitable_for": ["Defensive focus", "Against stronger teams", "Protecting a lead"]
            }
        }

        # Define set piece strategies
        self.set_pieces = {
            "Corner Kick - Near Post": {
                "description": "Aim for the near post with runners attacking that area",
                "strengths": ["Difficult for goalkeepers to defend", "Creates flick-on opportunities"],
                "setup": "Position strong headers at near post and far post. Deliver with pace and curve."
            },
            "Corner Kick - Far Post": {
                "description": "Aim for the far post with tall players attacking that area",
                "strengths": ["Can exploit height advantage", "Keeper struggles to reach far post"],
                "setup": "Position tall players at far post. Deliver with height to back post area."
            },
            "Free Kick - Direct": {
                "description": "Shoot directly at goal",
                "strengths": ["Can score directly", "Unpredictable"],
                "setup": "Specialist free kick taker with good technique. Others provide dummy runs."
            },
            "Free Kick - Training Ground": {
                "description": "Rehearsed routine with multiple movements and passes",
                "strengths": ["Can surprise opponents", "Creates open chances"],
                "setup": "Requires practiced movements and timing. Use dummy runners to create space."
            }
        }

    def generate_strategy(self, context_json=None, strategy_type="formation", team_situation=None):
        """
        Generate strategic recommendations based on the provided context

        Args:
            context_json (str, optional): JSON string containing match context, team data, etc.
            strategy_type (str): Type of strategy to generate (formation, tactics, set_piece)
            team_situation (str, optional): Brief description of team's current situation

        Returns:
            str: Strategic recommendation with explanation
        """
        try:
            # Parse context if provided
            context = None
            if context_json:
                if isinstance(context_json, str):
                    context = json.loads(context_json)
                else:
                    context = context_json

            # If no specific situation is provided, generate a general recommendation
            if not team_situation and not context:
                return self._generate_general_recommendation(strategy_type)

            # Generate recommendation based on the provided context or situation
            if strategy_type.lower() == "formation":
                return self._recommend_formation(context, team_situation)
            elif strategy_type.lower() == "tactics":
                return self._recommend_tactics(context, team_situation)
            elif strategy_type.lower() == "set_piece":
                return self._recommend_set_piece(context, team_situation)
            else:
                return f"Unknown strategy type: {strategy_type}. Please use formation, tactics, or set_piece."

        except Exception as e:
            return f"Error generating strategy: {str(e)}"

    def _generate_general_recommendation(self, strategy_type):
        """Generate a general recommendation without specific context"""
        if strategy_type.lower() == "formation":
            formations_info = []
            for formation, details in self.formations.items():
                formations_info.append(
                    f"• {formation}: {details['description']}\n  Strengths: {', '.join(details['strengths'])}\n  Suitable for: {', '.join(details['suitable_for'])}")

            return "Formation Recommendations:\n\n" + "\n\n".join(formations_info)

        elif strategy_type.lower() == "tactics":
            tactics_info = []
            for tactic, details in self.tactics.items():
                tactics_info.append(
                    f"• {tactic}: {details['description']}\n  Strengths: {', '.join(details['strengths'])}\n  Suitable for: {', '.join(details['suitable_for'])}")

            return "Tactical Approach Recommendations:\n\n" + "\n\n".join(tactics_info)

        elif strategy_type.lower() == "set_piece":
            set_pieces_info = []
            for set_piece, details in self.set_pieces.items():
                set_pieces_info.append(
                    f"• {set_piece}: {details['description']}\n  Strengths: {', '.join(details['strengths'])}\n  Setup: {details['setup']}")

            return "Set Piece Recommendations:\n\n" + "\n\n".join(set_pieces_info)

        else:
            return f"Unknown strategy type: {strategy_type}. Please use formation, tactics, or set_piece."

    def _recommend_formation(self, context, team_situation):
        """
        Recommend a formation based on the team situation

        This is a simplified rule-based recommendation for the prototype
        In a real implementation, this would use more sophisticated logic
        """
        recommendation = "Formation Recommendation:\n\n"

        # Check for keywords in the situation to make recommendations
        if team_situation:
            situation_lower = team_situation.lower()

            if "defensive" in situation_lower or "protect lead" in situation_lower:
                recommendation += f"Recommended Formation: 5-3-2\n\n"
                recommendation += f"Reasoning: {self.formations['5-3-2']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.formations['5-3-2']['strengths'])}\n"
                recommendation += f"• This formation is ideal when {', '.join(self.formations['5-3-2']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Ensure center-backs maintain tight spacing and communicate well\n"
                recommendation += "• Wing-backs should focus more on defensive duties than attacking\n"
                recommendation += "• Central midfielders should prioritize screening the defense\n"

            elif "attacking" in situation_lower or "need goals" in situation_lower:
                recommendation += f"Recommended Formation: 4-3-3\n\n"
                recommendation += f"Reasoning: {self.formations['4-3-3']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.formations['4-3-3']['strengths'])}\n"
                recommendation += f"• This formation is ideal when {', '.join(self.formations['4-3-3']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Position wingers high and wide to stretch the defense\n"
                recommendation += "• Full-backs should provide overlapping runs\n"
                recommendation += "• Central midfielders should focus on quick forward passes\n"

            elif "midfield control" in situation_lower or "possession" in situation_lower:
                recommendation += f"Recommended Formation: 4-2-3-1\n\n"
                recommendation += f"Reasoning: {self.formations['4-2-3-1']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.formations['4-2-3-1']['strengths'])}\n"
                recommendation += f"• This formation is ideal when {', '.join(self.formations['4-2-3-1']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• The two defensive midfielders should stay disciplined and protect the backline\n"
                recommendation += "• The attacking midfielder is the key creative force\n"
                recommendation += "• Wide attackers should move inside to create overloads\n"

            elif "balanced" in situation_lower or "versatile" in situation_lower:
                recommendation += f"Recommended Formation: 4-4-2\n\n"
                recommendation += f"Reasoning: {self.formations['4-4-2']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.formations['4-4-2']['strengths'])}\n"
                recommendation += f"• This formation is ideal when {', '.join(self.formations['4-4-2']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Ensure the midfield stays compact both horizontally and vertically\n"
                recommendation += "• The two strikers should work together, with one possibly dropping deeper\n"
                recommendation += "• Wide midfielders must contribute both offensively and defensively\n"

            else:
                # Default recommendation when keywords don't match
                recommendation += "Based on the situation described, I recommend analyzing the opponent's formation first.\n\n"
                recommendation += "Without specific details about your team's strengths or the opposition, "
                recommendation += "a balanced 4-4-2 formation provides solid defensive structure while maintaining attacking options.\n\n"
                recommendation += "Alternative options to consider:\n"
                recommendation += "• 4-2-3-1: For more midfield control\n"
                recommendation += "• 4-3-3: If you have strong wingers and need more attacking power\n"
                recommendation += "• 3-5-2: If you need extra midfield presence against strong opponents\n"
        else:
            # No situation provided, give general advice
            recommendation += "Without specific match context, I recommend a balanced 4-3-3 formation.\n\n"
            recommendation += "This provides good balance between defense, midfield, and attack. "
            recommendation += "It offers attacking options through width and can adapt to most situations.\n\n"
            recommendation += "Consider these alternatives based on your team's strengths:\n"
            recommendation += "• 4-4-2: Traditional balanced approach, good if you have striker partnerships\n"
            recommendation += "• 4-2-3-1: More defensive stability with attacking options\n"
            recommendation += "• 3-5-2: If you have good wing-backs and want midfield control\n"

        return recommendation

    def _recommend_tactics(self, context, team_situation):
        """Recommend tactics based on the team situation"""
        recommendation = "Tactical Approach Recommendation:\n\n"

        # Check for keywords in the situation to make recommendations
        if team_situation:
            situation_lower = team_situation.lower()

            if "stronger opponent" in situation_lower or "defensive" in situation_lower:
                recommendation += f"Recommended Tactic: Counter Attack\n\n"
                recommendation += f"Reasoning: {self.tactics['Counter Attack']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.tactics['Counter Attack']['strengths'])}\n"
                recommendation += f"• This tactic is ideal when {', '.join(self.tactics['Counter Attack']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Maintain a compact shape when defending\n"
                recommendation += "• Position fast attackers ready to break forward\n"
                recommendation += "• Practice quick transitions from defense to attack\n"

            elif "possession" in situation_lower or "control" in situation_lower:
                recommendation += f"Recommended Tactic: Possession\n\n"
                recommendation += f"Reasoning: {self.tactics['Possession']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.tactics['Possession']['strengths'])}\n"
                recommendation += f"• This tactic is ideal when {', '.join(self.tactics['Possession']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Focus on short, accurate passing\n"
                recommendation += "• Create triangles all over the pitch\n"
                recommendation += "• Be patient - not every pass needs to be forward\n"

            elif "pressing" in situation_lower or "aggressive" in situation_lower:
                recommendation += f"Recommended Tactic: High Press\n\n"
                recommendation += f"Reasoning: {self.tactics['High Press']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.tactics['High Press']['strengths'])}\n"
                recommendation += f"• This tactic is ideal when {', '.join(self.tactics['High Press']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Press as a unit - timing and coordination are essential\n"
                recommendation += "• Focus on cutting passing lanes\n"
                recommendation += "• Have a clear trigger for when to press\n"

            elif "direct" in situation_lower or "long ball" in situation_lower:
                recommendation += f"Recommended Tactic: Direct Play\n\n"
                recommendation += f"Reasoning: {self.tactics['Direct Play']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.tactics['Direct Play']['strengths'])}\n"
                recommendation += f"• This tactic is ideal when {', '.join(self.tactics['Direct Play']['suitable_for']).lower()}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Position players to win second balls\n"
                recommendation += "• Target forwards should be skilled at holding up play\n"
                recommendation += "• Midfielders should make forward runs to support\n"

            else:
                # Default recommendation
                recommendation += "Based on the limited information provided, a balanced approach combining elements of possession and counter-attacking is recommended.\n\n"
                recommendation += "Adapt your tactical approach based on:\n"
                recommendation += "• The opponent's strengths and weaknesses\n"
                recommendation += "• Your team's technical abilities\n"
                recommendation += "• Match situation (score, time remaining)\n\n"
                recommendation += "Consider these tactical options:\n"
                recommendation += "• High Press: If opponent struggles under pressure\n"
                recommendation += "• Counter Attack: If opponent commits players forward\n"
                recommendation += "• Possession: If your team is technically superior\n"
        else:
            # No situation provided
            recommendation += "Without specific match context, I recommend a flexible approach combining possession with direct counter-attacks when opportunities arise.\n\n"
            recommendation += "Maintain defensive shape when not in possession, but press selectively in the middle third.\n\n"
            recommendation += "Key tactical elements to consider:\n"
            recommendation += "• Balance is key - don't overcommit to attack or defense\n"
            recommendation += "• Adapt based on how the match develops\n"
            recommendation += "• Consider the strengths of your key players\n"

        return recommendation

    def _recommend_set_piece(self, context, team_situation):
        """Recommend set piece strategies based on the team situation"""
        recommendation = "Set Piece Recommendation:\n\n"

        # Check for keywords in the situation to make recommendations
        if team_situation:
            situation_lower = team_situation.lower()

            if "corner" in situation_lower and "attacking" in situation_lower:
                # Recommend corner kick strategy
                if "tall players" in situation_lower or "height advantage" in situation_lower:
                    recommendation += f"Recommended Set Piece: Corner Kick - Far Post\n\n"
                    recommendation += f"Reasoning: {self.set_pieces['Corner Kick - Far Post']['description']}\n"
                    recommendation += f"• Strengths: {', '.join(self.set_pieces['Corner Kick - Far Post']['strengths'])}\n"
                    recommendation += f"• Setup: {self.set_pieces['Corner Kick - Far Post']['setup']}\n\n"
                    recommendation += "Implementation Tips:\n"
                    recommendation += "• Deliver the ball with height to the far post area\n"
                    recommendation += "• Position 2-3 tall players to attack this area\n"
                    recommendation += "• Have players ready for rebounds\n"
                else:
                    recommendation += f"Recommended Set Piece: Corner Kick - Near Post\n\n"
                    recommendation += f"Reasoning: {self.set_pieces['Corner Kick - Near Post']['description']}\n"
                    recommendation += f"• Strengths: {', '.join(self.set_pieces['Corner Kick - Near Post']['strengths'])}\n"
                    recommendation += f"• Setup: {self.set_pieces['Corner Kick - Near Post']['setup']}\n\n"
                    recommendation += "Implementation Tips:\n"
                    recommendation += "• Deliver the ball with pace to the near post\n"
                    recommendation += "• Have a player attacking the near post for a flick-on\n"
                    recommendation += "• Position players at the far post and penalty spot\n"

            elif "free kick" in situation_lower and ("shooting" in situation_lower or "goal" in situation_lower):
                # Direct free kick near goal
                recommendation += f"Recommended Set Piece: Free Kick - Direct\n\n"
                recommendation += f"Reasoning: {self.set_pieces['Free Kick - Direct']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.set_pieces['Free Kick - Direct']['strengths'])}\n"
                recommendation += f"• Setup: {self.set_pieces['Free Kick - Direct']['setup']}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Have your best free kick taker as the primary option\n"
                recommendation += "• Position 1-2 additional players as decoys\n"
                recommendation += "• Consider shot placement based on wall and goalkeeper position\n"

            elif "free kick" in situation_lower and "wide" in situation_lower:
                # Free kick in wide position
                recommendation += f"Recommended Set Piece: Free Kick - Training Ground\n\n"
                recommendation += f"Reasoning: {self.set_pieces['Free Kick - Training Ground']['description']}\n"
                recommendation += f"• Strengths: {', '.join(self.set_pieces['Free Kick - Training Ground']['strengths'])}\n"
                recommendation += f"• Setup: {self.set_pieces['Free Kick - Training Ground']['setup']}\n\n"
                recommendation += "Implementation Tips:\n"
                recommendation += "• Use dummy runners to create space\n"
                recommendation += "• Consider a short pass to create a better crossing angle\n"
                recommendation += "• Position players at both posts and the penalty spot\n"

            else:
                # Default recommendation
                recommendation += "Based on the situation described, here are general set piece recommendations:\n\n"
                recommendation += "For Corners:\n"
                recommendation += "• Mix up delivery between near and far post\n"
                recommendation += "• Consider short corners to create different angles\n"
                recommendation += "• Position your best headers in the best scoring positions\n\n"
                recommendation += "For Free Kicks:\n"
                recommendation += "• In shooting range: Consider direct shots or training ground routines\n"
                recommendation += "• Wide positions: Create crossing opportunities or rehearsed movements\n"
                recommendation += "• Defensive half: Consider quick restarts to counter-attack\n"
        else:
            # No situation provided
            recommendation += "Without specific match context, here are general set piece recommendations:\n\n"
            recommendation += "Corner Kicks:\n"
            recommendation += "• Alternate between near and far post deliveries to be unpredictable\n"
            recommendation += "• Position 4-5 attackers in the box with specific assignments\n"
            recommendation += "• Keep 2-3 players outside the box for defensive security\n\n"
            recommendation += "Free Kicks:\n"
            recommendation += "• Attacking third: Direct shots or choreographed routines\n"
            recommendation += "• Middle third: Quick transitions to attack or possession retention\n"
            recommendation += "• Defensive third: Safe clearance and shape maintenance\n"

        return recommendation
