import os
import gradio as gr
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from typing import Dict, Any, List, Tuple
from llama_index.core.chat_engine import SimpleChatEngine

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
        # Create agent objects
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
    """Create an integrated multi-agent system with chat capabilities"""
    logger.info("Creating agent system...")

    try:
        # Extract all tools from specialized agents
        all_tools = []
        for name, agent in agents.items():
            if name != "coordinator":
                agent_tools = agent.get_tools()
                if agent_tools:
                    all_tools.extend(agent_tools)
                    logger.info(f"Added tools from {name} agent")

        # Create coordinator agent with all tools
        coordinator = agents["coordinator"]
        chat_engine = coordinator.create(all_tools)

        logger.info("Agent system created successfully")
        return chat_engine

    except Exception as e:
        logger.error(f"Error creating agent system: {str(e)}")
        raise


def create_ui(chat_engine: SimpleChatEngine, logger):
    """Create the Gradio UI for chat interaction"""
    logger.info("Setting up user interface...")

    def process_chat(message: str, history: List[Tuple[str, str]]):
        """Process chat messages through the agent system"""
        if not message.strip():
            return "", history

        logger.info(f"Processing message: {message}")

        try:
            # Process the message through the chat engine
            response = chat_engine.chat(message)
            logger.info("Message processed successfully")

            # Update history with the new message and response
            history.append((message, str(response)))
            return "", history

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(error_msg)
            history.append((message, f"Sorry, an error occurred: {str(e)}"))
            return "", history

    def reset_chat():
        """Reset the chat history and memory"""
        logger.info("Resetting chat history and memory")
        chat_engine.reset()
        return []

    with gr.Blocks(theme="default") as interface:
        gr.Markdown("# Coach Intelligence System")
        gr.Markdown(
            "AI-powered coaching assistant for strategy planning and real-time match analysis")

        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Type your message here...", lines=1)
        clear = gr.Button("Reset Chat", variant="secondary")

        # Set up examples
        examples = gr.Examples(
            examples=[
                "Suggest a defensive formation",
                "Show me a 4-3-3 formation",
                "What tactics should I use against a pressing team?",
                "Analyze data for Manchester United's recent matches"
            ],
            inputs=msg
        )

        # Set up event handlers
        msg.submit(process_chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
        clear.click(reset_chat, outputs=[chatbot])

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
        chat_engine = create_agent_system(agents, logger)
        ui = create_ui(chat_engine, logger)

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
