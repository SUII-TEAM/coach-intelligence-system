# Coach-Intelligence-System Prototype

A multi-agent AI system designed to empower football coaches with strategic planning, real-time data analysis, and visualization.

## Features

- **Strategy Planning**: Generate and adjust game strategies based on real-time data
- **Data Retrieval**: Fetch live match data, coaching documents, and external information
- **Data Analysis**: Process match events and recommend tactical adjustments
- **Visualization**: Display strategies and analytics with clear visuals

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/coach-intelligence-system.git
   cd coach-intelligence-system
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   Create a `.env` file in the root directory with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   SERPAPI_API_KEY=your_serpapi_key
   ```

## Usage

Run the application using:

```bash
python run.py
```

This will launch a Gradio interface where you can enter coaching commands like:

- "Suggest a defensive formation"
- "Analyze Manchester United's last match"
- "Show me a 4-3-3 formation"
- "What tactics should I use against a team that presses high?"

## Development Priority

Below is the prioritized order for developing the features of the Coach-Intelligence-System, ensuring a logical sequence based on dependencies and system requirements:

| **Order** | **Feature**          | **Description**                                       | **Dependencies**               |
| --------- | -------------------- | ----------------------------------------------------- | ------------------------------ |
| 1         | Coordinator Agent    | Central hub for user interaction and task delegation. | None                           |
| 2         | Data Retrieval Agent | Gathers data from various sources.                    | Coordinator Agent              |
| 3         | RAG Tool             | Retrieves internal coaching data.                     | Data Retrieval Agent           |
| 4         | Search Tool          | Collects external data.                               | Data Retrieval Agent           |
| 5         | Match Data Fetcher   | Retrieves real-time match data from api-football.     | Data Retrieval Agent           |
| 6         | Analysis Agent       | Interprets data for actionable insights.              | Data Retrieval Agent           |
| 7         | Match Data Analyzer  | Processes real-time match data for insights.          | Analysis Agent                 |
| 8         | Planning Agent       | Designs and refines game strategies.                  | Coordinator Agent              |
| 9         | Planning Tool        | Generates strategic recommendations.                  | Planning Agent                 |
| 10        | Visualization Agent  | Renders data and strategies visually.                 | Planning Agent, Analysis Agent |
| 11        | Visualization        | Presents strategies and analytics visually.           | Visualization Agent            |

## System Architecture

### Agents

- **Coordinator Agent**: Manages user interaction and orchestrates other agents
- **Data Retrieval Agent**: Gathers data from various sources
- **Analysis Agent**: Interprets data for actionable insights
- **Planning Agent**: Designs and refines game strategies
- **Visualization Agent**: Renders data and strategies visually

### Tools

- **RAG Tool**: Retrieves internal coaching data
- **Search Tool**: Collects external data
- **Match Data Fetcher**: Retrieves real-time match data
- **Match Data Analyzer**: Processes match data into insights
- **Planning Tool**: Generates strategic recommendations
- **Visualization Tool**: Creates visual representations

## Example Workflow

1. User enters a command: "Suggest a formation for a defensive approach"
2. Coordinator Agent understands the request and delegates tasks
3. Data Retrieval Agent gathers relevant information about defensive formations
4. Planning Agent generates a formation recommendation (e.g., 5-3-2)
5. Visualization Agent creates a visual diagram of the formation
6. Coordinator Agent compiles all information and presents it to the user

## License

GNU General Public License

---
