import os
import gradio as gr
from dotenv import load_dotenv
from crewai import Crew
import logging

# Import agents
from src.agents import (
    CoordinatorAgent,
    DataRetrievalAgent,
    AnalysisAgent,
    PlanningAgent,
    VisualizationAgent
)

# Import utilities
from src.utils import setup_logging, format_dict


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()

    # Check if essential API keys are present
    required_keys = ['GEMINI_API_KEY', 'SERPAPI_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        logging.warning(
            f"Missing environment variables: {', '.join(missing_keys)}")
        logging.warning("Some functionality may be limited.")


def initialize_agents(logger):
    """Initialize all agents for the system"""
    logger.info("Initializing agents...")

    try:
        coordinator_agent = CoordinatorAgent().create()
        logger.info("Coordinator Agent initialized")

        data_retrieval_agent = DataRetrievalAgent().create()
        logger.info("Data Retrieval Agent initialized")

        analysis_agent = AnalysisAgent().create()
        logger.info("Analysis Agent initialized")

        planning_agent = PlanningAgent().create()
        logger.info("Planning Agent initialized")

        visualization_agent = VisualizationAgent().create()
        logger.info("Visualization Agent initialized")

        agents = {
            "coordinator": coordinator_agent,
            "data_retrieval": data_retrieval_agent,
            "analysis": analysis_agent,
            "planning": planning_agent,
            "visualization": visualization_agent
        }

        logger.info("All agents initialized successfully")
        return agents

    except Exception as e:
        logger.error(f"Error initializing agents: {str(e)}")
        raise


def create_crew(agents, logger):
    """Create a CrewAI crew with the initialized agents"""
    logger.info("Creating crew with agents...")

    try:
        crew = Crew(
            agents=[
                agents["coordinator"],
                agents["data_retrieval"],
                agents["analysis"],
                agents["planning"],
                agents["visualization"]
            ],
            tasks=[],  # Tasks will be created by the coordinator agent
            verbose=True
        )

        logger.info("Crew created successfully")
        return crew

    except Exception as e:
        logger.error(f"Error creating crew: {str(e)}")
        raise


def create_ui(crew, coordinator_agent, logger):
    """Create the Gradio UI for user interaction"""
    logger.info("Setting up user interface...")

    def process_command(command):
        """Process user commands through the agent system"""
        if not command.strip():
            return "Please enter a command."

        logger.info(f"Processing command: {command}")

        try:
            task = coordinator_agent.process_input(command)
            logger.info(f"Created task: {task.description}")

            result = crew.kickoff(task=task)
            logger.info("Task completed successfully")

            return result

        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            logger.error(error_msg)
            return f"Sorry, an error occurred: {str(e)}"

    interface = gr.Interface(
        fn=process_command,
        inputs=gr.Textbox(
            lines=2, placeholder="Enter your coaching command..."),
        outputs="text",
        title="Coach Intelligence System",
        description="AI-powered coaching assistant for strategy planning and real-time match analysis",
        theme="default",
        examples=[
            ["Suggest a defensive formation"],
            ["Show me a 4-3-3 formation"],
            ["What tactics should I use against a pressing team?"],
            ["Analyze data for Manchester United's recent matches"]
        ]
    )

    logger.info("User interface created successfully")
    return interface


def main():
    """Main application entry point"""
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Coach Intelligence System")

    # Load environment variables
    load_environment()

    try:
        # Initialize the system
        agents = initialize_agents(logger)
        crew = create_crew(agents, logger)
        ui = create_ui(crew, agents["coordinator"], logger)

        # Launch the UI
        logger.info("Launching user interface")
        ui.launch()

    except Exception as e:
        logger.critical(f"Critical error in application: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    main()
