# Coach Intelligence System

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                  COACH INTELLIGENCE SYSTEM                        ║
║                                                                   ║
║              AI-powered football coaching assistant               ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

A sophisticated multi-agent AI system designed to empower football (soccer) coaches with strategic planning, real-time data analysis, and tactical visualization.

## Core Capabilities

- **Strategic Analysis:** Generate formations, tactics, and set-piece strategies based on team strengths and opponent weaknesses
- **Match Data Processing:** Retrieve and analyze live or historical match statistics to inform in-game decisions
- **Knowledge Retrieval:** Access relevant coaching documents and external football information through RAG and search tools
- **Visual Representations:** Display tactics, formations, and match analytics through clear, coach-friendly visualizations
- **Conversation Memory:** Maintain context across coaching sessions for continuous improvement

## System Architecture


### Multi-Agent Framework

The system employs a carefully designed multi-agent architecture:

- **Coordinator Agent:** Central orchestrator handling user requests and delegating specialized tasks
- **Data Retrieval Agent:** Gathers information from various sources including:
  - RAG Tool for accessing internal coaching documents
  - Search Tool for external football knowledge
  - Match Data Fetcher for real-time statistics
- **Analysis Agent:** Processes raw data into actionable insights via:
  - Match Data Analyzer for statistical interpretation
- **Planning Agent:** Develops strategic recommendations through:
  - Planning Tool for formations, tactics, and set pieces
- **Visualization Agent:** Creates visual representations of concepts and data

### Technology Stack

- **LlamaIndex:** Core framework for specialized LLM agents and RAG capabilities
- **Gemini Pro:** Powers agent reasoning and natural language understanding
- **LangChain:** Integrated for specific tools (e.g., SerpAPI web search)
- **Gradio:** Intuitive chat interface for coach interaction
- **Matplotlib/Plotly:** Data visualization libraries

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/coach-intelligence-system.git
   cd coach-intelligence-system
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   Create a `.env` file in the root directory with:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   SERPAPI_API_KEY=your_serpapi_key  # Optional: Enables web search capabilities
   ```

## Usage

Run the application using:

```bash
python run.py
```

This launches a Gradio interface where you can interact with the system using natural language. Here are example queries:

### Formation & Tactics

- "What's the best formation to counter a high-pressing team?"
- "Create a defensive strategy for protecting a 1-0 lead"
- "Show me a 4-3-3 formation with attacking fullbacks"
- "Suggest tactical changes to increase midfield control"
- "Design a set piece routine for corners against zonal marking"

### Analysis

- "Analyze Manchester United's possession statistics from their last match"
- "What are Arsenal's defensive weaknesses based on recent games?"
- "Compare the pressing effectiveness of Liverpool and Manchester City"
- "Show shot map and xG data from Chelsea's last match"
- "Identify patterns in how Bayern Munich transitions from defense to attack"

### Training

- "Generate a training session focusing on defensive transitions"
- "What drills should I use to improve our pressing game?"
- "Create a warm-up routine for match day"

## Project Structure

- **`src/`**: Core codebase
  - **`agents/`**: Multi-agent system implementation
  - **`tools/`**: Specialized capabilities (RAG, search, match data, planning, etc.)
  - **`visualization/`**: Generation of tactical diagrams and data plots
  - **`data/`**: Internal knowledge base and coaching documents
  - **`main.py`**: Application entry point
- **`conversations/`**: Storage for past coaching sessions
- **`logs/`**: System activity logs for debugging
- **`frontend-app/`**: Additional web interface components
- **`tests/`**: Testing suite

## Development Workflow

The current system has implemented the following components (checked items):

- [x] Coordinator Agent
- [x] Data Retrieval Agent
- [x] RAG Tool for coaching documents
- [x] Search Tool for external information
- [x] Match Data Fetcher (with mock data)
- [x] Analysis Agent
- [x] Match Data Analyzer
- [x] Planning Agent
- [x] Planning Tool (formations, tactics, set pieces)
- [x] Visualization Agent
- [x] Visualization Tool (formations, tactics)
- [x] Conversation management system

## Contributing

Contributions that enhance the system's capabilities are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

GNU General Public License

---
