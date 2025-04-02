#!/usr/bin/env python
"""
Coach Intelligence System Runner

This script starts the Coach Intelligence System with a Gradio UI.
"""

import os
import sys
import time
import traceback


def check_python_version():
    """Check if the current Python version is compatible"""
    if sys.version_info < (3, 9):
        print("Error: This application requires Python 3.9 or higher.")
        return False
    return True


def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import gradio
        import crewai
        import matplotlib
        import dotenv
        return True
    except ImportError as e:
        print(f"Error: Missing dependency - {str(e)}")
        print("Please install all required dependencies: pip install -r requirements.txt")
        return False


def display_banner():
    """Display the application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║                  COACH INTELLIGENCE SYSTEM                        ║
    ║                                                                   ║
    ║              AI-powered football coaching assistant               ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main application launcher"""
    display_banner()

    print("Performing pre-launch checks...")

    # Check Python version
    if not check_python_version():
        return 1

    # Check dependencies
    if not check_dependencies():
        return 1

    # Check for .env file
    if not os.path.exists('.env'):
        print("\nWarning: No .env file found. API keys might be missing.")
        print("If you experience issues, create a .env file with your API keys.")
        time.sleep(2)

    print("\nAll checks passed! Starting Coach Intelligence System...\n")

    try:
        # Import the main application module
        from src.main import main as app_main

        # Run the application
        return app_main()

    except Exception as e:
        print("\nError: Failed to start the application.")
        print(f"Reason: {str(e)}")
        print("\nDetailed error information:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
