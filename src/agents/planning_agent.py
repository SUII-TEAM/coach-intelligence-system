from .base_agent import BaseAgent
from ..tools.planning_tool import PlanningTool


class PlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Planning Agent"
        self.goal = "Design effective football strategies and tactics"
        self.system_prompt = """
        You are a tactical genius in football (soccer) with deep knowledge of
        formations, playing styles, and match strategies. Your specialty is creating
        tailored game plans that account for your team's strengths and the opposition's
        weaknesses. You can suggest both pre-match strategies and in-game adaptations.
        """

        # Initialize tools
        self.planning_tool = PlanningTool()

        # Add tools to the agent's tool list
        self.tools = [
            self.planning_tool.tool
        ]
