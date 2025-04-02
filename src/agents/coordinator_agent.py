from crewai import Agent, Task
from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.role = "Coordinator Agent"
        self.goal = "Manage user interaction and orchestrate other agents"
        self.backstory = """
        You are the central hub of the Coach Intelligence System. Your job is to understand
        coach requests, break them down into tasks, delegate them to specialized agents,
        and compile their responses into a cohesive answer for the coach.
        """

    def create(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            llm=self.llm
        )

    def process_input(self, user_input):
        """
        Process user input and create appropriate tasks

        Args:
            user_input (str): The command from the user/coach

        Returns:
            Task: A CrewAI task based on the user input
        """
        return Task(
            description=f"Process the following coaching request: {user_input}",
            expected_output="Comprehensive response to the coach's request, including any relevant data, analysis, and visualizations.",
            agent=self.create()
        )
