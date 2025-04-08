import os
import gradio as gr
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from typing import Dict, Any, List, Tuple
from llama_index.core.chat_engine import SimpleChatEngine
import json
from datetime import datetime
from llama_index.core.llms import ChatMessage

# Import agents
from src.agents import (
    CoordinatorAgent,
    DataRetrievalAgent,
    AnalysisAgent,
    PlanningAgent,
    VisualizationAgent
)

# Import utilities
from src.utils import setup_logging, format_dict, ConversationManager

# Initialize conversation manager
conversation_manager = ConversationManager()


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

        # Create coordinator agent with all tools and internal engine
        coordinator = agents["coordinator"]
        # Coordinator now creates and stores its engine
        coordinator.create(all_tools)

        logger.info("Agent system created successfully")
        return coordinator  # Return the coordinator instance

    except Exception as e:
        logger.error(f"Error creating agent system: {str(e)}")
        raise


def create_ui(coordinator: CoordinatorAgent, agents: Dict[str, Any], logger):
    """Create the Gradio UI for chat interaction"""
    logger.info("Setting up user interface...")

    def get_conversation_display_mapping():
        """Get mapping of display names to conversation IDs"""
        try:
            conversations = conversation_manager.list_conversations()
            display_to_id = {}

            for conv in conversations:
                try:
                    date = datetime.fromisoformat(conv['created_at'])
                    date_str = date.strftime('%b %d, %Y')
                except:
                    date_str = "Example"

                title = conv['title']
                if 'example_' in conv['id']:
                    title = f"📋 {title} (Example)"

                display_text = f"{title} - {date_str}"
                display_to_id[display_text] = conv['id']

            return display_to_id
        except Exception as e:
            logger.error(f"Error creating conversation mapping: {str(e)}")
            return {}

    def get_conversation_choices():
        """Get display names for conversations"""
        mapping = get_conversation_display_mapping()
        return list(mapping.keys())

    def load_conversation_by_display(display_name: str):
        """Load a conversation by its display name"""
        if not display_name:
            return [], None

        try:
            # Convert display name to conversation ID
            mapping = get_conversation_display_mapping()
            conversation_id = mapping.get(display_name)

            if not conversation_id:
                logger.error(
                    f"Could not find conversation ID for display name: {display_name}")
                return [], None

            conversation = conversation_manager.load_conversation(
                conversation_id)

            # Convert to message format
            messages = []
            for msg in conversation["messages"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Reset chat engine memory via coordinator
            # No need to reset engine here, load_history handles it
            coordinator.load_history(messages)

            # Log the loaded conversation
            logger.info(
                f"Loaded conversation: {conversation['title']} ({conversation_id})")
            logger.debug(f"Messages loaded from file: {messages}")

            return messages, conversation_id
        except Exception as e:
            logger.error(f"Error loading conversation: {str(e)}")
            return [], None

    def create_new_chat():
        """Create a new chat session and provide a welcome message."""
        # Explicitly reset coordinator memory (which also resets its engine)
        coordinator.reset_memory()
        logger.info("New chat created, coordinator memory and engine reset.")

        # Define the welcome message
        welcome_message = {
            "role": "assistant",
            "content": "Hello Coach! How can I assist you today? I can help with:\n- Analyzing match data\n- Planning tactics and formations\n- Scouting opponents\n- Suggesting training drills"
        }

        # Return the welcome message as the initial history
        return [welcome_message], None

    def process_chat(message: str, history: List[Dict[str, str]], conversation_id: str = None):
        """Process chat messages through the agent system"""
        if not message.strip():
            return "", history, conversation_id

        logger.info(f"Processing message via Coordinator: {message}")

        try:
            # Log memory state before processing
            # Ensure agent exists before trying to access its memory
            if coordinator.agent:
                pre_process_memory = coordinator.agent.memory.get_all()
                logger.debug(
                    f"Memory BEFORE chat processing ({len(pre_process_memory)} messages): {[(m.role.value, m.content[:50] + '...') for m in pre_process_memory]}")
            else:
                logger.debug(
                    "Memory BEFORE chat processing: Agent not yet initialized.")

            # Process the message through the coordinator's chat method
            response = coordinator.chat(message)
            logger.info("Message processed successfully by coordinator")

            # Retrieve the full history from the agent's memory
            full_history_msgs = coordinator.agent.memory.get_all()
            logger.debug(
                f"Memory AFTER chat processing ({len(full_history_msgs)} messages): {[(m.role.value, m.content[:50] + '...') for m in full_history_msgs]}")

            # Convert ChatMessage objects to the dict format for saving and display
            history_to_save_and_display = [
                {"role": msg.role.value, "content": msg.content}
                for msg in full_history_msgs
            ]

            # Save the complete, updated conversation history
            conversation_id = conversation_manager.save_conversation(
                messages=history_to_save_and_display,  # Save the full history
                conversation_id=conversation_id
            )

            # Return updated history and conversation ID for Gradio UI
            # Use the full history to update the chatbot display
            return "", history_to_save_and_display, conversation_id

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(error_msg)
            # Append user message and error to the *current* Gradio history for display
            history.append({"role": "user", "content": message})
            history.append(
                {"role": "assistant", "content": f"Sorry, an error occurred: {str(e)}"})
            # Return the history with the error appended, but don't save over the last good state
            return "", history, conversation_id

    with gr.Blocks(title="Coach Intelligence System") as interface:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("# 💬 Conversations")

                # New chat button
                new_chat_btn = gr.Button("+ New Chat", variant="primary")

                # Conversation selector with user-friendly display names
                conversation_dropdown = gr.Dropdown(
                    choices=get_conversation_choices(),
                    label="Previous Conversations",
                    value=None,
                    interactive=True,
                    allow_custom_value=False
                )

                gr.Markdown("### Need help?")
                gr.Markdown(
                    "Ask about formations, tactics, training sessions, or match analysis.")

            with gr.Column(scale=3):
                # Main chat interface
                gr.Markdown("# Coach Intelligence System")
                gr.Markdown(
                    "AI-powered coaching assistant for strategy planning and real-time match analysis")

                chatbot = gr.Chatbot(
                    height=450,
                    type="messages",
                    show_label=False,
                    avatar_images=(
                        None, "https://api.dicebear.com/7.x/bottts/svg?seed=coach")
                )

                # Hidden components
                conversation_id = gr.State()

                # Input area
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        lines=1,
                        container=False,
                        show_label=False,
                        scale=9
                    )
                    submit = gr.Button("Send", variant="primary", scale=1)

        # Event handlers
        msg.submit(
            process_chat,
            inputs=[msg, chatbot, conversation_id],
            outputs=[msg, chatbot, conversation_id]
        )
        submit.click(
            process_chat,
            inputs=[msg, chatbot, conversation_id],
            outputs=[msg, chatbot, conversation_id]
        )
        conversation_dropdown.change(
            load_conversation_by_display,
            inputs=[conversation_dropdown],
            outputs=[chatbot, conversation_id]
        )
        new_chat_btn.click(
            create_new_chat,
            outputs=[chatbot, conversation_id]
        )

        # Refresh conversation list after saving new messages
        def refresh_conversation_list():
            return gr.Dropdown(choices=get_conversation_choices())

        # Update dropdown on page load
        interface.load(refresh_conversation_list,
                       outputs=[conversation_dropdown])

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
        coordinator = create_agent_system(
            agents, logger)  # Get coordinator instance
        ui = create_ui(coordinator, agents, logger)  # Pass coordinator to UI

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
