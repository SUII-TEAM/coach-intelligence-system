"""
Utility functions for the Coach Intelligence System
"""

import os
import logging
import datetime

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
    import json
    try:
        return json.loads(data_str)
    except (json.JSONDecodeError, TypeError):
        return data_str
