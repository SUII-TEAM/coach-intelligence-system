"""
Utility functions for the Coach Intelligence System
"""

import os
import logging
import datetime
import json
from typing import List, Dict, Any

# Setup logging


def setup_logging(level=logging.INFO):
    """
    Set up logging for the application

    Args:
        level: The logging level (default: INFO)

    Returns:
        A configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Set up logging
    logger = logging.getLogger('coach_intelligence')
    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create file handler
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(
        f'logs/coach_intelligence_{timestamp}.log')
    file_handler.setLevel(level)

    # Create formatter and add to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Format dictionary output for better readability


def format_dict(data, indent=0):
    """
    Format a dictionary for better readability in logs

    Args:
        data: The dictionary to format
        indent: The indentation level (default: 0)

    Returns:
        A formatted string representation of the dictionary
    """
    result = []
    prefix = '  ' * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                result.append(f"{prefix}{key}:")
                result.append(format_dict(value, indent + 1))
            else:
                result.append(f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                result.append(format_dict(item, indent + 1))
            else:
                result.append(f"{prefix}- {item}")
    else:
        result.append(f"{prefix}{data}")

    return '\n'.join(result)

# Helper function to safely convert data between formats


def safe_json_loads(data_str):
    """
    Safely parse JSON data

    Args:
        data_str: The JSON string to parse

    Returns:
        The parsed data or the original string if parsing failed
    """
    try:
        return json.loads(data_str)
    except (json.JSONDecodeError, TypeError):
        return data_str


class ConversationManager:
    """Manages conversation history and persistence"""

    def __init__(self, storage_dir: str = "conversations"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        # Check if we need to create example conversations
        if not os.listdir(storage_dir):
            self._create_example_conversations()

    def _create_example_conversations(self):
        """Create example conversations for demonstration purposes"""
        example_conversations = [
            {
                "id": "example_defensive_tactics",
                "title": "Defensive Formation Analysis",
                "created_at": "2023-06-15T14:30:00",
                "messages": [
                    {"role": "user", "content": "What's the best defensive formation for a team that struggles with counter-attacks?"},
                    {"role": "assistant", "content": "For teams vulnerable to counter-attacks, I recommend a 5-3-2 formation. This provides:\n\n1. Three center-backs for solid defense\n2. Wing-backs who can track back quickly\n3. Three central midfielders to control the game\n4. Two strikers for counter-attacking opportunities"},
                    {"role": "user", "content": "How should the midfielders be positioned?"},
                    {"role": "assistant",
                        "content": "In a 5-3-2, the midfielders should form a triangle:\n\n- One defensive midfielder (CDM) sitting deep\n- Two central midfielders (CM) slightly ahead\n\nThis creates a solid defensive block while maintaining passing options."}
                ]
            },
            {
                "id": "example_training_session",
                "title": "Training Session Planning",
                "created_at": "2023-06-20T09:15:00",
                "messages": [
                    {"role": "user", "content": "Create a training session focused on improving passing accuracy"},
                    {"role": "assistant",
                        "content": "Here's a 90-minute passing-focused session:\n\n1. Warm-up (15 min):\n   - Dynamic stretching\n   - Light jogging with ball\n\n2. Technical drills (30 min):\n   - Triangle passing patterns\n   - One-touch passing in squares\n\n3. Small-sided games (30 min):\n   - 4v4 with passing restrictions\n   - Focus on quick ball movement"},
                    {"role": "user", "content": "What equipment do we need?"},
                    {"role": "assistant", "content": "For this session you'll need:\n\n- 20 cones\n- 15 balls\n- 4 small goals\n- Bibs for team separation\n- Stopwatch for timing drills"}
                ]
            },
            {
                "id": "example_match_analysis",
                "title": "Match Analysis Request",
                "created_at": "2023-06-25T18:45:00",
                "messages": [
                    {"role": "user", "content": "Analyze our last match against City FC"},
                    {"role": "assistant", "content": "From the match data, here are the key observations:\n\n1. Possession: 45% vs 55%\n2. Shots on target: 4 vs 8\n3. Key defensive issues:\n   - Left flank vulnerability\n   - Slow transition from defense to attack\n4. Positive aspects:\n   - Good pressing in midfield\n   - Strong set-piece defense"},
                    {"role": "user", "content": "What tactical adjustments should we make?"},
                    {"role": "assistant", "content": "Based on the analysis, I recommend:\n\n1. Strengthen left flank with overlapping full-back\n2. Implement quicker counter-attacking patterns\n3. Adjust midfield pressing triggers\n4. Work on transition speed in training"}
                ]
            }
        ]

        # Save example conversations
        for conv in example_conversations:
            file_path = os.path.join(self.storage_dir, f"{conv['id']}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(conv, f, ensure_ascii=False, indent=2)
                    print(f"Created example conversation: {conv['title']}")

    def _generate_title(self, messages: List[Dict[str, str]]) -> str:
        """Generate a user-friendly title from conversation messages"""
        # Try to find a meaningful first user message
        first_user_message = next(
            (msg for msg in messages if msg['role'] == 'user'), None)
        if not first_user_message:
            return "New Conversation"

        content = first_user_message['content']

        # Clean and format the title
        title = content.strip()

        # Remove common prefixes and clean up
        prefixes = ["analyze", "what", "how", "can", "could",
                    "would", "please", "help", "suggest", "recommend"]
        for prefix in prefixes:
            if title.lower().startswith(prefix):
                title = title[len(prefix):].strip()

        # Capitalize first letter
        title = title[0].upper() + title[1:] if title else "New Conversation"

        # Truncate if too long
        if len(title) > 50:
            title = title[:47] + "..."

        return title

    def save_conversation(self, messages: List[Dict[str, str]], title: str = None, conversation_id: str = None) -> str:
        """
        Save a conversation to disk with an optional title

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            title: Optional title for the conversation
            conversation_id: Optional ID of an existing conversation to update

        Returns:
            The conversation ID
        """
        if not title:
            title = self._generate_title(messages)

        # Use existing conversation_id or create new one
        if not conversation_id:
            conversation_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create conversation data
        conversation_data = {
            "id": conversation_id,
            "title": title,
            "created_at": datetime.datetime.now().isoformat(),
            "messages": messages
        }

        # Save to file
        file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)

        return conversation_id

    def load_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Load a conversation by ID"""
        file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Conversation {conversation_id} not found")

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all saved conversations with formatted titles"""
        conversations = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.storage_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Format the title for display
                    display_title = data["title"]
                    conversations.append({
                        "id": data["id"],
                        "title": display_title,
                        "created_at": data["created_at"]
                    })

        # Sort by creation date, newest first
        return sorted(conversations, key=lambda x: x["created_at"], reverse=True)

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation by ID"""
        file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
