from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import os


class RAGTool:
    def __init__(self):
        self.name = "retrieve_coaching_data"
        self.description = """
        Use this tool to retrieve information from internal coaching documents.
        This is useful for accessing historical data, coaching manuals, and team policies.
        """
        # Initialize LlamaIndex components
        self._initialize_document_index()
        self.tool = FunctionTool.from_defaults(
            name=self.name,
            description=self.description,
            fn=self.retrieve_data
        )

    def _initialize_document_index(self):
        """
        Create a document index using LlamaIndex
        In the prototype, we'll use mock data. In production, this would use real documents.
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

        # Write mock documents to files if they don't exist
        for doc in mock_docs:
            doc_path = f"src/data/coaching_docs/{doc['filename']}"
            if not os.path.exists(doc_path):
                with open(doc_path, 'w') as f:
                    f.write(doc['content'])

        # Set up LlamaIndex components
        self.docs_path = "src/data/coaching_docs"

        try:
            # Load documents
            documents = SimpleDirectoryReader(self.docs_path).load_data()

            # Create embeddings and index
            # Use GeminiEmbedding for embedding if API key is available, otherwise use default
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                embed_model = GeminiEmbedding(
                    model_name="models/embedding-001", api_key=api_key)
                self.index = VectorStoreIndex.from_documents(
                    documents,
                    embed_model=embed_model
                )
            else:
                # Fall back to default embedding if no API key
                self.index = VectorStoreIndex.from_documents(documents)

            # Create retriever
            self.retriever = self.index.as_retriever(similarity_top_k=2)

        except Exception as e:
            print(f"Error initializing document index: {str(e)}")
            # Create empty index as fallback
            self.index = None
            self.retriever = None

    def retrieve_data(self, query):
        """
        Retrieve relevant information from coaching documents based on the query

        Args:
            query (str): The search query

        Returns:
            str: Relevant information from the coaching documents
        """
        try:
            if self.index is None:
                # Fallback to simple file search if index creation failed
                return self._simple_file_search(query)

            # Use LlamaIndex retriever
            nodes = self.retriever.retrieve(query)

            if nodes:
                results = []
                for node in nodes:
                    source = node.metadata.get("file_name", "unknown source")
                    results.append(f"From {source}:\n{node.text}")
                return "\n\n".join(results)
            else:
                return "No relevant information found in the coaching documents."

        except Exception as e:
            return f"Error retrieving data: {str(e)}"

    def _simple_file_search(self, query):
        """Fallback method for simple text search in files"""
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
