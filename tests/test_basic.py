"""
Basic tests for the Coach Intelligence System
"""

from src.visualization import VisualizationTool
from src.tools import RAGTool, SearchTool, PlanningTool
from src.agents import CoordinatorAgent, DataRetrievalAgent
import os
import sys
import unittest

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestImports(unittest.TestCase):
    """Test that all modules can be imported correctly"""

    def test_agent_imports(self):
        """Test that agent modules can be imported"""
        self.assertIsNotNone(CoordinatorAgent)
        self.assertIsNotNone(DataRetrievalAgent)

    def test_tool_imports(self):
        """Test that tool modules can be imported"""
        self.assertIsNotNone(RAGTool)
        self.assertIsNotNone(SearchTool)
        self.assertIsNotNone(PlanningTool)

    def test_visualization_imports(self):
        """Test that visualization modules can be imported"""
        self.assertIsNotNone(VisualizationTool)


class TestRAGTool(unittest.TestCase):
    """Test the RAG Tool functionality"""

    def setUp(self):
        """Set up the test environment"""
        self.rag_tool = RAGTool()

    def test_initialization(self):
        """Test that the RAG tool can be initialized"""
        self.assertIsNotNone(self.rag_tool)
        self.assertIsNotNone(self.rag_tool.tool)

    def test_mock_data_creation(self):
        """Test that mock data is created"""
        # Check that the docs path exists
        self.assertTrue(os.path.exists(self.rag_tool.docs_path))

        # Check that files were created
        files = os.listdir(self.rag_tool.docs_path)
        self.assertGreater(len(files), 0)

    def test_simple_query(self):
        """Test a simple query to the RAG tool"""
        # Test a query that should match
        result = self.rag_tool.retrieve_data("formation")
        self.assertIn("4-4-2", result)

        # Test a query that shouldn't match
        result = self.rag_tool.retrieve_data("xyzabc123")
        self.assertIn("No relevant information", result)


class TestPlanningTool(unittest.TestCase):
    """Test the Planning Tool functionality"""

    def setUp(self):
        """Set up the test environment"""
        self.planning_tool = PlanningTool()

    def test_initialization(self):
        """Test that the Planning tool can be initialized"""
        self.assertIsNotNone(self.planning_tool)
        self.assertIsNotNone(self.planning_tool.tool)

    def test_formation_recommendation(self):
        """Test formation recommendation functionality"""
        # Test with a defensive situation
        result = self.planning_tool.generate_strategy(
            strategy_type="formation",
            team_situation="We need a defensive approach"
        )
        self.assertIn("5-3-2", result)

        # Test with an attacking situation
        result = self.planning_tool.generate_strategy(
            strategy_type="formation",
            team_situation="We need more goals"
        )
        self.assertIn("4-3-3", result)


if __name__ == '__main__':
    unittest.main()
