import os
import gradio as gr
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from typing import Dict, Any

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

    # Configure Gemini API
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)


def initialize_agents(logger):
    """Initialize all agents for the system"""
    logger.info("Initializing agents...")

    try:
        # Create agent objects (not actual LlamaIndex agents yet)
        coordinator = CoordinatorAgent()
        logger.info("Coordinator Agent initialized")

        data_retrieval = DataRetrievalAgent()
        logger.info("Data Retrieval Agent initialized")

        analysis = AnalysisAgent()
        logger.info("Analysis Agent initialized")

        planning = PlanningAgent()
        logger.info("Planning Agent initialized")

        visualization = VisualizationAgent()
        logger.info("Visualization Agent initialized")

        # Return agent objects in a dictionary
        agents = {
            "coordinator": coordinator,
            "data_retrieval": data_retrieval,
            "analysis": analysis,
            "planning": planning,
            "visualization": visualization
        }

        logger.info("All agents initialized successfully")
        return agents

    except Exception as e:
        logger.error(f"Error initializing agents: {str(e)}")
        raise


def create_agent_system(agents, logger):
    """Create an integrated multi-agent system"""
    logger.info("Creating agent system...")

    try:
        # Extract all tools from specialized agents
        all_tools = []
        for name, agent in agents.items():
            if name != "coordinator":
                agent_tools = agent.get_tools()
                if agent_tools:
                    # Debug: print tool information
                    for tool in agent_tools:
                        logger.info(f"Tool from {name}: {tool}")
                        try:
                            logger.info(f"Tool name: {tool.metadata.name}")
                        except Exception as e:
                            logger.error(
                                f"Error accessing tool name: {str(e)}")
                            logger.error(f"Tool type: {type(tool)}")

                    all_tools.extend(agent_tools)
                    logger.info(f"Added tools from {name} agent")

        # Create coordinator agent with all tools
        coordinator = agents["coordinator"]
        multi_agent_system = coordinator.create(all_tools)

        logger.info("Agent system created successfully")
        return multi_agent_system

    except Exception as e:
        logger.error(f"Error creating agent system: {str(e)}")
        raise


def create_ui(agent_system, logger):
    """Create the Gradio UI for user interaction"""
    logger.info("Setting up user interface...")

    def process_command(command):
        """Process user commands through the agent system"""
        if not command.strip():
            return "Please enter a command."

        logger.info(f"Processing command: {command}")

        try:
            # Process the command through the coordinator agent
            response = agent_system.chat(command)
            logger.info("Command processed successfully")

            return str(response)

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
        agent_system = create_agent_system(agents, logger)
        ui = create_ui(agent_system, logger)

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
