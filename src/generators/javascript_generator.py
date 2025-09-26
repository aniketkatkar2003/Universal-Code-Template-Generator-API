from typing import List
from ..models import FunctionSignature
from . import TemplateGenerator


class JavaScriptGenerator(TemplateGenerator):
    """Template generator for JavaScript."""
    
    def __init__(self):
        super().__init__('javascript')
    
    def generate_template(self, signature: FunctionSignature) -> str:
        """Generate JavaScript template."""
        all_types = self.get_all_types(signature)
        
        # Add TreeNode definition if needed
        tree_node_def = ""
        if any('Tree' in t for t in all_types):
            tree_node_def = self._get_tree_node_definition() + "\n\n"
        
        # Generate function signature
        params = [param.name for param in signature.parameters]
        
        mapped_return_type = self.type_mapper.map_type(signature.returns.type)
        
        function_template = f'''{tree_node_def}/**
 * @param {{{"}, {".join([f"{param.name}: {self.type_mapper.map_type(param.type)}" for param in signature.parameters])}}}
 * @return {{{mapped_return_type}}}
 */
function {signature.function_name}({", ".join(params)}) {{
    // Write your logic here
    {self._get_default_return(mapped_return_type)}
}}

{self._generate_helper_functions(all_types)}

// Do not edit below this line
const readline = require('readline');
const rl = readline.createInterface({{
    input: process.stdin,
    output: process.stdout
}});

let input = '';
rl.on('line', (line) => {{
    input += line;
}});

rl.on('close', () => {{
    const data = JSON.parse(input);
    
    {self._generate_parameter_extraction(signature)}
    
    {self._generate_function_call_and_output(signature)}
}});'''
        
        return function_template
    
    def _get_tree_node_definition(self) -> str:
        """Get TreeNode class definition."""
        return '''// Definition for a binary tree node
function TreeNode(val, left, right) {
    this.val = (val===undefined ? 0 : val);
    this.left = (left===undefined ? null : left);
    this.right = (right===undefined ? null : right);
}'''
    
    def _get_default_return(self, return_type: str) -> str:
        """Get appropriate default return statement."""
        if 'Tree' in return_type:
            return "return null;"
        elif return_type == 'Map<number, number[]>':
            return "return new Map();"
        elif 'number[]' in return_type or '[]' in return_type:
            return "return [];"
        elif return_type == 'number':
            return "return 0;"
        elif return_type == 'boolean':
            return "return false;"
        elif return_type == 'string':
            return 'return "";'
        else:
            return "return null;"
    
    def _generate_helper_functions(self, all_types: List[str]) -> str:
        """Generate helper functions if needed."""
        if any('Tree' in t for t in all_types):
            return '''
function deserializeTree(data) {
    if (!data || data.length === 0) return null;
    
    const root = new TreeNode(data[0]);
    const queue = [root];
    let i = 1;
    
    while (queue.length > 0 && i < data.length) {
        const node = queue.shift();
        
        if (i < data.length && data[i] !== null) {
            node.left = new TreeNode(data[i]);
            queue.push(node.left);
        }
        i++;
        
        if (i < data.length && data[i] !== null) {
            node.right = new TreeNode(data[i]);
            queue.push(node.right);
        }
        i++;
    }
    
    return root;
}

function serializeTree(root) {
    if (!root) return [];
    
    const result = [];
    const queue = [root];
    
    while (queue.length > 0) {
        const node = queue.shift();
        
        if (node) {
            result.push(node.val);
            queue.push(node.left);
            queue.push(node.right);
        } else {
            result.push(null);
        }
    }
    
    // Remove trailing nulls
    while (result.length > 0 && result[result.length - 1] === null) {
        result.pop();
    }
    
    return result;
}'''
        return ""
    
    def _generate_parameter_extraction(self, signature: FunctionSignature) -> str:
        """Generate parameter extraction code."""
        lines = []
        for param in signature.parameters:
            if self._is_tree_type(param.type):
                lines.append(f"    const {param.name} = deserializeTree(data.{param.name});")
            else:
                lines.append(f"    const {param.name} = data.{param.name};")
        return "\n".join(lines)
    
    def _generate_function_call_and_output(self, signature: FunctionSignature) -> str:
        """Generate function call and output code."""
        param_names = [param.name for param in signature.parameters]
        function_call = f"{signature.function_name}({', '.join(param_names)})"
        
        if self._is_tree_type(signature.returns.type):
            return f"    const result = {function_call};\n    console.log(JSON.stringify(serializeTree(result)));"
        else:
            return f"    const result = {function_call};\n    console.log(JSON.stringify(result));"
    
    def _is_tree_type(self, dsl_type: str) -> bool:
        """Check if the type is a tree type."""
        return 'Tree' in dsl_type
