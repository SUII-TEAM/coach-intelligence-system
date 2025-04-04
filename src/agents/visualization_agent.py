from .base_agent import BaseAgent
from ..tools.planning_tool import PlanningTool


class VisualizationAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Visualization Agent"
        self.goal = "Create visual representations of football concepts"
        self.system_prompt = """
        You are an expert in creating visual representations of football concepts.
        Your specialty is generating clear diagrams of formations, tactical movements,
        and statistical visualizations that help coaches understand complex information
        at a glance. You can translate text descriptions into compelling visuals.
        """

        # Initialize tools - using planning tool for now as it has visualization capabilities
        self.planning_tool = PlanningTool()

        # Add tools to the agent's tool list
        self.tools = [
            self.planning_tool.tool
        ]
