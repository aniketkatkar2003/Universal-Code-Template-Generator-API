import pytest
import json
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Universal Code Template Generator API" in response.json()["message"]


def test_get_supported_languages():
    """Test the supported languages endpoint."""
    response = client.get("/api/v1/languages")
    assert response.status_code == 200
    languages = response.json()["languages"]
    assert len(languages) == 4
    language_names = [lang["name"] for lang in languages]
    assert "python" in language_names
    assert "java" in language_names
    assert "cpp" in language_names
    assert "javascript" in language_names


def test_get_supported_types():
    """Test the supported types endpoint."""
    response = client.get("/api/v1/types")
    assert response.status_code == 200
    types_info = response.json()
    assert "primitives" in types_info["types"]
    assert "collections" in types_info["types"]
    assert "special" in types_info["types"]


class TestTemplateGeneration:
    """Test template generation for various scenarios."""
    
    def test_python_fibonacci(self):
        """Test single primitive input: Fibonacci(n: int) -> int"""
        request = {
            "question_id": "fibonacci",
            "title": "Fibonacci Number",
            "description": "Calculate the nth Fibonacci number",
            "signature": {
                "function_name": "fibonacci",
                "parameters": [
                    {"name": "n", "type": "int"}
                ],
                "returns": {"type": "int"}
            },
            "language": "python"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "python"
        assert "class Solution:" in result["template"]
        assert "def fibonacci(self, n: int) -> int:" in result["template"]
        assert "if __name__ == \"__main__\":" in result["template"]
    
    def test_python_two_sum(self):
        """Test multiple mixed inputs: twoSum(nums: int[], target: int) -> int[]"""
        request = {
            "question_id": "two-sum",
            "title": "Two Sum",
            "description": "Given an integer array...",
            "signature": {
                "function_name": "twoSum",
                "parameters": [
                    {"name": "nums", "type": "int[]"},
                    {"name": "target", "type": "int"}
                ],
                "returns": {"type": "int[]"}
            },
            "language": "python"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "python"
        assert "from typing import List" in result["template"]
        assert "def twoSum(self, nums: List[int], target: int) -> List[int]:" in result["template"]
    
    def test_python_tree_problem(self):
        """Test tree input: LowestCommonAncestor(root: Tree, p: Tree, q: Tree) -> Tree"""
        request = {
            "question_id": "lca",
            "title": "Lowest Common Ancestor",
            "description": "Find the lowest common ancestor of two nodes in a binary tree",
            "signature": {
                "function_name": "lowestCommonAncestor",
                "parameters": [
                    {"name": "root", "type": "Tree"},
                    {"name": "p", "type": "Tree"},
                    {"name": "q", "type": "Tree"}
                ],
                "returns": {"type": "Tree"}
            },
            "language": "python"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "python"
        assert "TreeNode" in result["template"]
        assert "Optional[TreeNode]" in result["template"]
    
    def test_java_template_generation(self):
        """Test Java template generation."""
        request = {
            "question_id": "two-sum",
            "title": "Two Sum",
            "description": "Given an integer array...",
            "signature": {
                "function_name": "twoSum",
                "parameters": [
                    {"name": "nums", "type": "int[]"},
                    {"name": "target", "type": "int"}
                ],
                "returns": {"type": "int[]"}
            },
            "language": "java"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "java"
        assert "public class Solution" in result["template"]
        assert "public int[] twoSum(int[] nums, int target)" in result["template"]
        assert "public static void main(String[] args)" in result["template"]
    
    def test_cpp_template_generation(self):
        """Test C++ template generation."""
        request = {
            "question_id": "two-sum",
            "title": "Two Sum",
            "description": "Given an integer array...",
            "signature": {
                "function_name": "twoSum",
                "parameters": [
                    {"name": "nums", "type": "int[]"},
                    {"name": "target", "type": "int"}
                ],
                "returns": {"type": "int[]"}
            },
            "language": "cpp"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "cpp"
        assert "class Solution" in result["template"]
        assert "vector<int> twoSum(vector<int> nums, int target)" in result["template"]
        assert "int main()" in result["template"]
    
    def test_javascript_template_generation(self):
        """Test JavaScript template generation."""
        request = {
            "question_id": "two-sum",
            "title": "Two Sum",
            "description": "Given an integer array...",
            "signature": {
                "function_name": "twoSum",
                "parameters": [
                    {"name": "nums", "type": "int[]"},
                    {"name": "target", "type": "int"}
                ],
                "returns": {"type": "int[]"}
            },
            "language": "javascript"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "javascript"
        assert "function twoSum(nums, target)" in result["template"]
        assert "const readline = require('readline')" in result["template"]
    
    def test_graph_problem(self):
        """Test Graph input: DetectCycle(graph: Graph) -> bool"""
        request = {
            "question_id": "detect-cycle",
            "title": "Detect Cycle",
            "description": "Detect if there is a cycle in the graph",
            "signature": {
                "function_name": "detectCycle",
                "parameters": [
                    {"name": "graph", "type": "Graph"}
                ],
                "returns": {"type": "bool"}
            },
            "language": "python"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 201
        
        result = response.json()
        assert result["language"] == "python"
        assert "Dict[int, List[int]]" in result["template"]


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_unsupported_language(self):
        """Test unsupported language error."""
        request = {
            "question_id": "test",
            "title": "Test",
            "description": "Test description",
            "signature": {
                "function_name": "test",
                "parameters": [{"name": "x", "type": "int"}],
                "returns": {"type": "int"}
            },
            "language": "ruby"  # Unsupported language
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 422  # Validation error from Pydantic enum
    
    def test_missing_required_fields(self):
        """Test missing required fields error."""
        request = {
            "question_id": "test",
            "title": "Test",
            "description": "Test description",
            "signature": {
                "function_name": "",  # Empty function name
                "parameters": [{"name": "x", "type": "int"}],
                "returns": {"type": "int"}
            },
            "language": "python"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 400
    
    def test_invalid_json(self):
        """Test invalid JSON payload."""
        response = client.post(
            "/api/v1/template",
            data="invalid json",
            headers={"content-type": "application/json"}
        )
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_missing_parameters(self):
        """Test missing parameters in signature."""
        request = {
            "question_id": "test",
            "title": "Test",
            "description": "Test description",
            "signature": {
                "function_name": "test",
                "parameters": [{"name": "", "type": "int"}],  # Empty parameter name
                "returns": {"type": "int"}
            },
            "language": "python"
        }
        
        response = client.post("/api/v1/template", json=request)
        assert response.status_code == 400
