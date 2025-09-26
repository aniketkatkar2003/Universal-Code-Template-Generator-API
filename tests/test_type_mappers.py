import pytest
from src.type_mappers import (
    PythonTypeMapper,
    JavaTypeMapper,
    CppTypeMapper,
    JavaScriptTypeMapper,
    get_type_mapper
)


class TestPythonTypeMapper:
    """Test Python type mapper."""
    
    def test_primitive_types(self):
        mapper = PythonTypeMapper()
        
        assert mapper.map_type("int") == "int"
        assert mapper.map_type("long") == "int"
        assert mapper.map_type("float") == "float"
        assert mapper.map_type("double") == "float"
        assert mapper.map_type("bool") == "bool"
        assert mapper.map_type("string") == "str"
    
    def test_array_types(self):
        mapper = PythonTypeMapper()
        
        assert mapper.map_type("int[]") == "List[int]"
        assert mapper.map_type("string[]") == "List[str]"
    
    def test_list_types(self):
        mapper = PythonTypeMapper()
        
        assert mapper.map_type("List<int>") == "List[int]"
        assert mapper.map_type("List<int[]>") == "List[List[int]]"
    
    def test_tree_types(self):
        mapper = PythonTypeMapper()
        
        assert mapper.map_type("Tree") == "Optional[TreeNode]"
        assert mapper.map_type("Tree<int>") == "Optional[TreeNode[int]]"
    
    def test_graph_type(self):
        mapper = PythonTypeMapper()
        
        assert mapper.map_type("Graph") == "Dict[int, List[int]]"
    
    def test_imports(self):
        mapper = PythonTypeMapper()
        
        imports = mapper.get_imports(["int[]", "List<string>"])
        assert "from typing import List" in imports
        
        imports = mapper.get_imports(["Tree", "Tree<int>"])
        assert "from typing import Optional" in imports


class TestJavaTypeMapper:
    """Test Java type mapper."""
    
    def test_primitive_types(self):
        mapper = JavaTypeMapper()
        
        assert mapper.map_type("int") == "int"
        assert mapper.map_type("long") == "long"
        assert mapper.map_type("bool") == "boolean"
        assert mapper.map_type("string") == "String"
    
    def test_array_types(self):
        mapper = JavaTypeMapper()
        
        assert mapper.map_type("int[]") == "int[]"
        assert mapper.map_type("string[]") == "String[]"
    
    def test_list_types(self):
        mapper = JavaTypeMapper()
        
        assert mapper.map_type("List<int>") == "List<int>"
        assert mapper.map_type("List<int[]>") == "List<int[]>"
    
    def test_tree_types(self):
        mapper = JavaTypeMapper()
        
        assert mapper.map_type("Tree") == "TreeNode"
        assert mapper.map_type("Tree<int>") == "TreeNode<Integer>"


class TestCppTypeMapper:
    """Test C++ type mapper."""
    
    def test_primitive_types(self):
        mapper = CppTypeMapper()
        
        assert mapper.map_type("int") == "int"
        assert mapper.map_type("long") == "long long"
        assert mapper.map_type("bool") == "bool"
        assert mapper.map_type("string") == "string"
    
    def test_array_types(self):
        mapper = CppTypeMapper()
        
        assert mapper.map_type("int[]") == "vector<int>"
        assert mapper.map_type("string[]") == "vector<string>"
    
    def test_tree_types(self):
        mapper = CppTypeMapper()
        
        assert mapper.map_type("Tree") == "TreeNode*"
        assert mapper.map_type("Tree<int>") == "TreeNode<int>*"


class TestJavaScriptTypeMapper:
    """Test JavaScript type mapper."""
    
    def test_primitive_types(self):
        mapper = JavaScriptTypeMapper()
        
        assert mapper.map_type("int") == "number"
        assert mapper.map_type("bool") == "boolean"
        assert mapper.map_type("string") == "string"
    
    def test_array_types(self):
        mapper = JavaScriptTypeMapper()
        
        assert mapper.map_type("int[]") == "number[]"
        assert mapper.map_type("string[]") == "string[]"
    
    def test_tree_types(self):
        mapper = JavaScriptTypeMapper()
        
        assert mapper.map_type("Tree") == "TreeNode"
        assert mapper.map_type("Tree<int>") == "TreeNode"


def test_get_type_mapper():
    """Test the factory function for getting type mappers."""
    
    assert isinstance(get_type_mapper("python"), PythonTypeMapper)
    assert isinstance(get_type_mapper("java"), JavaTypeMapper)
    assert isinstance(get_type_mapper("cpp"), CppTypeMapper)
    assert isinstance(get_type_mapper("javascript"), JavaScriptTypeMapper)
    
    with pytest.raises(ValueError):
        get_type_mapper("unsupported")
