from langchain.tools import Tool
# We're using a simple text search for the prototype instead of vector embeddings
# from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os


class RAGTool:
    def __init__(self):
        self.name = "rag_tool"
        self.description = """
        Use this tool to retrieve information from internal coaching documents.
        This is useful for accessing historical data, coaching manuals, and team policies.
        """
        # Initialize mock data for the prototype
        self._initialize_mock_data()
        self.tool = Tool.from_function(
            func=self.retrieve_data,
            name=self.name,
            description=self.description
        )

    def _initialize_mock_data(self):
        """
        Create a simple database with mock coaching data for the prototype
        In a real implementation, this would load actual coaching documents into a vector index
        """
        # Ensure the data directory exists
        os.makedirs("src/data/coaching_docs", exist_ok=True)

        # Create some mock documents for testing
        mock_docs = [
            {"filename": "formations.txt", "content":
             """Common Football Formations:
             4-4-2: Standard formation with four defenders, four midfielders, and two strikers. Balanced for both attack and defense.
             4-3-3: Formation with four defenders, three midfielders, and three forwards. Strong offensive capabilities.
             3-5-2: Three defenders, five midfielders, and two strikers. Provides strong midfield control.
             5-3-2: Five defenders, three midfielders, and two strikers. Highly defensive formation.
             4-2-3-1: Four defenders, two defensive midfielders, three attacking midfielders, and one striker. Modern balanced formation.
             """
             },
            {"filename": "tactics.txt", "content":
             """Tactical Approaches:
             High Press: Aggressively pressure opponents in their own half to force turnovers.
             Counter-Attack: Defend deep and strike quickly when possession is won.
             Possession-Based: Maintain ball control to create attacking opportunities.
             Tiki-Taka: Short passing and movement to maintain possession and create openings.
             Gegenpressing: Immediately counter-press after losing possession to win the ball back quickly.
             """
             },
            {"filename": "player_roles.txt", "content":
             """Player Positions and Roles:
             Goalkeeper: Last line of defense, responsible for preventing goals.
             Center-Back: Central defender who marks strikers and clears dangerous balls.
             Full-Back: Side defenders who defend against wingers and provide width in attack.
             Defensive Midfielder: Shields the defense and distributes the ball forward.
             Central Midfielder: Links defense and attack, contributes to both phases.
             Attacking Midfielder: Creates scoring opportunities for strikers.
             Winger: Wide attackers who create crossing opportunities and cut inside.
             Striker: Primary goal scorer who leads the attacking line.
             """
             }
        ]

        # Write mock documents to files
        for doc in mock_docs:
            with open(f"src/data/coaching_docs/{doc['filename']}", 'w') as f:
                f.write(doc['content'])

        # In a real implementation, we would create a proper vector index here
        # For the prototype, we'll just read these files when needed
        self.docs_path = "src/data/coaching_docs"

    def retrieve_data(self, query):
        """
        Retrieve relevant information from coaching documents based on the query

        Args:
            query (str): The search query

        Returns:
            str: Relevant information from the coaching documents
        """
        # For the prototype, we do a simple text search in our mock files
        results = []

        try:
            for filename in os.listdir(self.docs_path):
                with open(os.path.join(self.docs_path, filename), 'r') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append(f"From {filename}:\n{content}")

            if results:
                return "\n\n".join(results)
            else:
                return "No relevant information found in the coaching documents."
        except Exception as e:
            return f"Error retrieving data: {str(e)}"
