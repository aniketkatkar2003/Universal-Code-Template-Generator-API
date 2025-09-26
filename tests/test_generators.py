import pytest
from src.generators.factory import GeneratorFactory
from src.generators.python_generator import PythonGenerator
from src.generators.java_generator import JavaGenerator
from src.generators.cpp_generator import CppGenerator
from src.generators.javascript_generator import JavaScriptGenerator
from src.models import FunctionSignature, Parameter, ReturnType


class TestGeneratorFactory:
    """Test the generator factory."""
    
    def test_get_python_generator(self):
        generator = GeneratorFactory.get_generator("python")
        assert isinstance(generator, PythonGenerator)
    
    def test_get_java_generator(self):
        generator = GeneratorFactory.get_generator("java")
        assert isinstance(generator, JavaGenerator)
    
    def test_get_cpp_generator(self):
        generator = GeneratorFactory.get_generator("cpp")
        assert isinstance(generator, CppGenerator)
    
    def test_get_javascript_generator(self):
        generator = GeneratorFactory.get_generator("javascript")
        assert isinstance(generator, JavaScriptGenerator)
    
    def test_unsupported_language(self):
        with pytest.raises(ValueError):
            GeneratorFactory.get_generator("unsupported")


class TestPythonGenerator:
    """Test Python template generation."""
    
    def test_simple_function(self):
        signature = FunctionSignature(
            function_name="fibonacci",
            parameters=[Parameter(name="n", type="int")],
            returns=ReturnType(type="int")
        )
        
        generator = PythonGenerator()
        template = generator.generate_template(signature)
        
        assert "class Solution:" in template
        assert "def fibonacci(self, n: int) -> int:" in template
        assert "pass" in template
        assert "if __name__ == \"__main__\":" in template
    
    def test_list_parameters(self):
        signature = FunctionSignature(
            function_name="twoSum",
            parameters=[
                Parameter(name="nums", type="int[]"),
                Parameter(name="target", type="int")
            ],
            returns=ReturnType(type="int[]")
        )
        
        generator = PythonGenerator()
        template = generator.generate_template(signature)
        
        assert "from typing import List" in template
        assert "nums: List[int]" in template
        assert "-> List[int]" in template
    
    def test_tree_parameters(self):
        signature = FunctionSignature(
            function_name="inorderTraversal",
            parameters=[Parameter(name="root", type="Tree<int>")],
            returns=ReturnType(type="int[]")
        )
        
        generator = PythonGenerator()
        template = generator.generate_template(signature)
        
        assert "TreeNode" in template
        assert "Optional[TreeNode[int]]" in template
        assert "from typing import Optional" in template


class TestJavaGenerator:
    """Test Java template generation."""
    
    def test_simple_function(self):
        signature = FunctionSignature(
            function_name="fibonacci",
            parameters=[Parameter(name="n", type="int")],
            returns=ReturnType(type="int")
        )
        
        generator = JavaGenerator()
        template = generator.generate_template(signature)
        
        assert "public class Solution" in template
        assert "public int fibonacci(int n)" in template
        assert "return null;" in template
        assert "public static void main" in template
    
    def test_list_parameters(self):
        signature = FunctionSignature(
            function_name="twoSum",
            parameters=[
                Parameter(name="nums", type="int[]"),
                Parameter(name="target", type="int")
            ],
            returns=ReturnType(type="int[]")
        )
        
        generator = JavaGenerator()
        template = generator.generate_template(signature)
        
        assert "int[] nums" in template
        assert "int target" in template
        assert "int[]" in template  # return type


class TestCppGenerator:
    """Test C++ template generation."""
    
    def test_simple_function(self):
        signature = FunctionSignature(
            function_name="fibonacci",
            parameters=[Parameter(name="n", type="int")],
            returns=ReturnType(type="int")
        )
        
        generator = CppGenerator()
        template = generator.generate_template(signature)
        
        assert "class Solution" in template
        assert "int fibonacci(int n)" in template
        assert "return 0;" in template
        assert "int main()" in template
    
    def test_vector_parameters(self):
        signature = FunctionSignature(
            function_name="twoSum",
            parameters=[
                Parameter(name="nums", type="int[]"),
                Parameter(name="target", type="int")
            ],
            returns=ReturnType(type="int[]")
        )
        
        generator = CppGenerator()
        template = generator.generate_template(signature)
        
        assert "vector<int> nums" in template
        assert "vector<int>" in template  # return type
        assert "#include <vector>" in template


class TestJavaScriptGenerator:
    """Test JavaScript template generation."""
    
    def test_simple_function(self):
        signature = FunctionSignature(
            function_name="fibonacci",
            parameters=[Parameter(name="n", type="int")],
            returns=ReturnType(type="int")
        )
        
        generator = JavaScriptGenerator()
        template = generator.generate_template(signature)
        
        assert "function fibonacci(n)" in template
        assert "return 0;" in template
        assert "const readline = require('readline')" in template
    
    def test_array_parameters(self):
        signature = FunctionSignature(
            function_name="twoSum",
            parameters=[
                Parameter(name="nums", type="int[]"),
                Parameter(name="target", type="int")
            ],
            returns=ReturnType(type="int[]")
        )
        
        generator = JavaScriptGenerator()
        template = generator.generate_template(signature)
        
        assert "function twoSum(nums, target)" in template
        assert "number[]" in template  # in JSDoc comment
        assert "return [];" in template
