from typing import List
from ..models import FunctionSignature
from . import TemplateGenerator


class PythonGenerator(TemplateGenerator):
    """Template generator for Python."""
    
    def __init__(self):
        super().__init__('python')
    
    def generate_template(self, signature: FunctionSignature) -> str:
        """Generate Python template."""
        # Get all types for imports
        all_types = self.get_all_types(signature)
        imports = self.type_mapper.get_imports(all_types)
        
        # Build imports section
        imports_section = ""
        if imports:
            imports_section = "\n".join(imports) + "\n\n"
        
        # Add TreeNode definition if needed
        tree_node_def = ""
        if any('Tree' in t for t in all_types):
            tree_node_def = self._get_tree_node_definition() + "\n\n"
        
        # Generate function signature
        params = []
        for param in signature.parameters:
            param_type = self.type_mapper.map_type(param.type)
            params.append(f"{param.name}: {param_type}")
        
        return_type = self.type_mapper.map_type(signature.returns.type)
        
        function_def = f"class Solution:\n"
        function_def += f"    def {signature.function_name}(self, {', '.join(params)}) -> {return_type}:\n"
        function_def += f"        # Write your logic here\n"
        function_def += f"        pass\n\n"
        
        # Generate main section with I/O handling
        main_section = self._generate_main_section(signature)
        
        return imports_section + tree_node_def + function_def + main_section
    
    def _get_tree_node_definition(self) -> str:
        """Get TreeNode class definition."""
        return '''# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right'''
    
    def _generate_main_section(self, signature: FunctionSignature) -> str:
        """Generate the main section with I/O handling."""
        # Build parameter extraction logic
        param_extraction = []
        for param in signature.parameters:
            if self._is_tree_type(param.type):
                param_extraction.append(f"    {param.name} = self._deserialize_tree(data['{param.name}'])")
            elif param.type == 'Graph':
                param_extraction.append(f"    {param.name} = data['{param.name}']")
            else:
                param_extraction.append(f"    {param.name} = data['{param.name}']")
        
        # Build function call
        param_names = [param.name for param in signature.parameters]
        function_call = f"solution.{signature.function_name}({', '.join(param_names)})"
        
        # Build result serialization
        if self._is_tree_type(signature.returns.type):
            result_handling = f"    result = {function_call}\n    print(json.dumps(self._serialize_tree(result)))"
        else:
            result_handling = f"    result = {function_call}\n    print(json.dumps(result))"
        
        main_template = f'''if __name__ == "__main__":
    # Do not edit below this line
    import sys
    import json
    
    class TreeHelper:
        @staticmethod
        def _deserialize_tree(data):
            if not data:
                return None
            nodes = [TreeNode(val) if val is not None else None for val in data]
            kids = nodes[::-1]
            root = kids.pop()
            for node in nodes:
                if node:
                    if kids: node.left = kids.pop()
                    if kids: node.right = kids.pop()
            return root
        
        @staticmethod
        def _serialize_tree(root):
            if not root:
                return []
            result, queue = [], [root]
            while queue:
                node = queue.pop(0)
                if node:
                    result.append(node.val)
                    queue.append(node.left)
                    queue.append(node.right)
                else:
                    result.append(None)
            # Remove trailing None values
            while result and result[-1] is None:
                result.pop()
            return result
    
    data = json.loads(sys.stdin.read())
    solution = Solution()
    helper = TreeHelper()
    
{chr(10).join(param_extraction)}
    
{result_handling}'''
        
        return main_template
    
    def _is_tree_type(self, dsl_type: str) -> bool:
        """Check if the type is a tree type."""
        return 'Tree' in dsl_type
