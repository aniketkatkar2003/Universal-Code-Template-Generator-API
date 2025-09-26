from abc import ABC, abstractmethod
from typing import Dict, List
import re


class TypeMapper(ABC):
    """Abstract base class for type mapping between DSL and target languages."""
    
    @abstractmethod
    def map_type(self, dsl_type: str) -> str:
        """Map a DSL type to the target language type."""
        pass
    
    @abstractmethod
    def get_imports(self, dsl_types: List[str]) -> List[str]:
        """Get required imports for the given DSL types."""
        pass


class PythonTypeMapper(TypeMapper):
    """Type mapper for Python."""
    
    TYPE_MAPPING = {
        'int': 'int',
        'long': 'int',
        'float': 'float',
        'double': 'float',
        'bool': 'bool',
        'string': 'str',
        'Graph': 'Dict[int, List[int]]'
    }
    
    def map_type(self, dsl_type: str) -> str:
        # Handle arrays: int[] -> List[int]
        array_match = re.match(r'(\w+)\[\]', dsl_type)
        if array_match:
            base_type = array_match.group(1)
            mapped_base = self.TYPE_MAPPING.get(base_type, base_type)
            return f'List[{mapped_base}]'
        
        # Handle generic List: List<int[]> -> List[List[int]]
        list_match = re.match(r'List<(.+)>', dsl_type)
        if list_match:
            inner_type = list_match.group(1)
            mapped_inner = self.map_type(inner_type)
            return f'List[{mapped_inner}]'
        
        # Handle Tree: Tree<int> -> Optional[TreeNode[int]]
        tree_match = re.match(r'Tree<(.+)>', dsl_type)
        if tree_match:
            inner_type = tree_match.group(1)
            mapped_inner = self.map_type(inner_type)
            return f'Optional[TreeNode[{mapped_inner}]]'
        
        # Handle simple Tree
        if dsl_type == 'Tree':
            return 'Optional[TreeNode]'
        
        return self.TYPE_MAPPING.get(dsl_type, dsl_type)
    
    def get_imports(self, dsl_types: List[str]) -> List[str]:
        imports = set()
        
        for dsl_type in dsl_types:
            if 'List' in dsl_type or '[]' in dsl_type:
                imports.add('from typing import List')
            if 'Tree' in dsl_type:
                imports.add('from typing import Optional')
        
        return sorted(list(imports))


class JavaTypeMapper(TypeMapper):
    """Type mapper for Java."""
    
    TYPE_MAPPING = {
        'int': 'int',
        'long': 'long',
        'float': 'float',
        'double': 'double',
        'bool': 'boolean',
        'string': 'String',
        'Graph': 'Map<Integer, List<Integer>>'
    }
    
    def map_type(self, dsl_type: str) -> str:
        # Handle arrays: int[] -> int[]
        array_match = re.match(r'(\w+)\[\]', dsl_type)
        if array_match:
            base_type = array_match.group(1)
            mapped_base = self.TYPE_MAPPING.get(base_type, base_type)
            return f'{mapped_base}[]'
        
        # Handle generic List: List<int[]> -> List<int[]>
        list_match = re.match(r'List<(.+)>', dsl_type)
        if list_match:
            inner_type = list_match.group(1)
            mapped_inner = self.map_type(inner_type)
            return f'List<{mapped_inner}>'
        
        # Handle Tree: Tree<int> -> TreeNode<Integer>
        tree_match = re.match(r'Tree<(.+)>', dsl_type)
        if tree_match:
            inner_type = tree_match.group(1)
            mapped_inner = self.map_type(inner_type)
            # Convert primitive to wrapper for generics
            if mapped_inner == 'int':
                mapped_inner = 'Integer'
            elif mapped_inner == 'boolean':
                mapped_inner = 'Boolean'
            return f'TreeNode<{mapped_inner}>'
        
        # Handle simple Tree
        if dsl_type == 'Tree':
            return 'TreeNode'
        
        return self.TYPE_MAPPING.get(dsl_type, dsl_type)
    
    def get_imports(self, dsl_types: List[str]) -> List[str]:
        imports = set()
        
        for dsl_type in dsl_types:
            if 'List' in dsl_type:
                imports.add('import java.util.List;')
            if 'Graph' in dsl_type:
                imports.add('import java.util.Map;')
                imports.add('import java.util.List;')
        
        return sorted(list(imports))


class CppTypeMapper(TypeMapper):
    """Type mapper for C++."""
    
    TYPE_MAPPING = {
        'int': 'int',
        'long': 'long long',
        'float': 'float',
        'double': 'double',
        'bool': 'bool',
        'string': 'string',
        'Graph': 'unordered_map<int, vector<int>>'
    }
    
    def map_type(self, dsl_type: str) -> str:
        # Handle arrays: int[] -> vector<int>
        array_match = re.match(r'(\w+)\[\]', dsl_type)
        if array_match:
            base_type = array_match.group(1)
            mapped_base = self.TYPE_MAPPING.get(base_type, base_type)
            return f'vector<{mapped_base}>'
        
        # Handle generic List: List<int[]> -> vector<vector<int>>
        list_match = re.match(r'List<(.+)>', dsl_type)
        if list_match:
            inner_type = list_match.group(1)
            mapped_inner = self.map_type(inner_type)
            return f'vector<{mapped_inner}>'
        
        # Handle Tree: Tree<int> -> TreeNode<int>*
        tree_match = re.match(r'Tree<(.+)>', dsl_type)
        if tree_match:
            inner_type = tree_match.group(1)
            mapped_inner = self.map_type(inner_type)
            return f'TreeNode<{mapped_inner}>*'
        
        # Handle simple Tree
        if dsl_type == 'Tree':
            return 'TreeNode*'
        
        return self.TYPE_MAPPING.get(dsl_type, dsl_type)
    
    def get_imports(self, dsl_types: List[str]) -> List[str]:
        imports = set()
        
        for dsl_type in dsl_types:
            if 'List' in dsl_type or '[]' in dsl_type:
                imports.add('#include <vector>')
            if 'string' in dsl_type:
                imports.add('#include <string>')
            if 'Graph' in dsl_type:
                imports.add('#include <unordered_map>')
                imports.add('#include <vector>')
        
        return sorted(list(imports))


class JavaScriptTypeMapper(TypeMapper):
    """Type mapper for JavaScript."""
    
    def map_type(self, dsl_type: str) -> str:
        # JavaScript is dynamically typed, so we return generic descriptions
        # Handle arrays: int[] -> number[]
        array_match = re.match(r'(\w+)\[\]', dsl_type)
        if array_match:
            base_type = array_match.group(1)
            js_base = self._get_js_type(base_type)
            return f'{js_base}[]'
        
        # Handle generic List: List<int[]> -> number[][]
        list_match = re.match(r'List<(.+)>', dsl_type)
        if list_match:
            inner_type = list_match.group(1)
            mapped_inner = self.map_type(inner_type)
            return f'{mapped_inner}[]'
        
        # Handle Tree: Tree<int> -> TreeNode
        tree_match = re.match(r'Tree<(.+)>', dsl_type)
        if tree_match:
            return 'TreeNode'
        
        # Handle simple Tree
        if dsl_type == 'Tree':
            return 'TreeNode'
        
        if dsl_type == 'Graph':
            return 'Map<number, number[]>'
        
        return self._get_js_type(dsl_type)
    
    def _get_js_type(self, dsl_type: str) -> str:
        mapping = {
            'int': 'number',
            'long': 'number',
            'float': 'number',
            'double': 'number',
            'bool': 'boolean',
            'string': 'string'
        }
        return mapping.get(dsl_type, dsl_type)
    
    def get_imports(self, dsl_types: List[str]) -> List[str]:
        # JavaScript doesn't require explicit imports for basic types
        return []


def get_type_mapper(language: str) -> TypeMapper:
    """Factory function to get the appropriate type mapper."""
    mappers = {
        'python': PythonTypeMapper(),
        'java': JavaTypeMapper(),
        'cpp': CppTypeMapper(),
        'javascript': JavaScriptTypeMapper()
    }
    
    if language not in mappers:
        raise ValueError(f"Unsupported language: {language}")
    
    return mappers[language]
