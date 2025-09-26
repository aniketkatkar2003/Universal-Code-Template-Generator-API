from typing import List
from ..models import FunctionSignature
from . import TemplateGenerator


class CppGenerator(TemplateGenerator):
    """Template generator for C++."""
    
    def __init__(self):
        super().__init__('cpp')
    
    def generate_template(self, signature: FunctionSignature) -> str:
        """Generate C++ template."""
        # Get all types for imports
        all_types = self.get_all_types(signature)
        imports = self.type_mapper.get_imports(all_types)
        
        # Standard includes
        standard_includes = [
            '#include <iostream>',
            '#include <string>',
            '#include <vector>',
            '#include <queue>',
            '#include <sstream>'
        ]
        
        # Combine imports
        all_imports = standard_includes + imports
        imports_section = "\n".join(sorted(set(all_imports))) + "\n"
        
        # Add JSON library
        json_include = '#include <nlohmann/json.hpp>\n'
        
        # Using declarations
        using_section = '''using namespace std;
using json = nlohmann::json;

'''
        
        # Add TreeNode definition if needed
        tree_node_def = ""
        if any('Tree' in t for t in all_types):
            tree_node_def = self._get_tree_node_definition() + "\n\n"
        
        # Generate function signature
        params = []
        for param in signature.parameters:
            param_type = self.type_mapper.map_type(param.type)
            params.append(f"{param_type} {param.name}")
        
        return_type = self.type_mapper.map_type(signature.returns.type)
        
        class_template = f'''{imports_section}{json_include}
{using_section}{tree_node_def}class Solution {{
public:
    {return_type} {signature.function_name}({", ".join(params)}) {{
        // Write your logic here
        {self._get_default_return(signature.returns.type)}
    }}
}};

{self._generate_helper_functions(all_types)}

int main() {{
    // Do not edit below this line
    string input;
    string line;
    while (getline(cin, line)) {{
        input += line;
    }}
    
    json data = json::parse(input);
    Solution solution;
    
    {self._generate_parameter_extraction(signature)}
    
    {self._generate_function_call_and_output(signature)}
    
    return 0;
}}'''
        
        return class_template
    
    def _get_tree_node_definition(self) -> str:
        """Get TreeNode struct definition."""
        return '''// Definition for a binary tree node
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};'''
    
    def _get_default_return(self, return_type: str) -> str:
        """Get appropriate default return statement."""
        if 'Tree' in return_type:
            return "return nullptr;"
        elif return_type == 'Graph':
            return "return {};"
        elif 'vector' in return_type or 'List' in return_type:
            return "return {};"
        elif return_type in ['int', 'long long']:
            return "return 0;"
        elif return_type in ['float', 'double']:
            return "return 0.0;"
        elif return_type == 'bool':
            return "return false;"
        elif return_type == 'string':
            return 'return "";'
        else:
            return "return {};"
    
    def _generate_helper_functions(self, all_types: List[str]) -> str:
        """Generate helper functions if needed."""
        if any('Tree' in t for t in all_types):
            return '''TreeNode* deserializeTree(const json& data) {
    if (data.empty()) return nullptr;
    
    TreeNode* root = new TreeNode(data[0]);
    queue<TreeNode*> q;
    q.push(root);
    
    int i = 1;
    while (!q.empty() && i < data.size()) {
        TreeNode* node = q.front();
        q.pop();
        
        if (i < data.size() && !data[i].is_null()) {
            node->left = new TreeNode(data[i]);
            q.push(node->left);
        }
        i++;
        
        if (i < data.size() && !data[i].is_null()) {
            node->right = new TreeNode(data[i]);
            q.push(node->right);
        }
        i++;
    }
    
    return root;
}

json serializeTree(TreeNode* root) {
    json result = json::array();
    if (!root) return result;
    
    queue<TreeNode*> q;
    q.push(root);
    
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        
        if (node) {
            result.push_back(node->val);
            q.push(node->left);
            q.push(node->right);
        } else {
            result.push_back(nullptr);
        }
    }
    
    // Remove trailing nulls
    while (!result.empty() && result.back().is_null()) {
        result.erase(result.end() - 1);
    }
    
    return result;
}

'''
        return ""
    
    def _generate_parameter_extraction(self, signature: FunctionSignature) -> str:
        """Generate parameter extraction code."""
        lines = []
        for param in signature.parameters:
            if self._is_tree_type(param.type):
                lines.append(f'    TreeNode* {param.name} = deserializeTree(data["{param.name}"]);')
            elif param.type == 'Graph':
                lines.append(f'    auto {param.name} = data["{param.name}"].get<unordered_map<int, vector<int>>>();')
            else:
                cpp_type = self.type_mapper.map_type(param.type)
                lines.append(f'    auto {param.name} = data["{param.name}"].get<{cpp_type}>();')
        return "\n".join(lines)
    
    def _generate_function_call_and_output(self, signature: FunctionSignature) -> str:
        """Generate function call and output code."""
        param_names = [param.name for param in signature.parameters]
        function_call = f"solution.{signature.function_name}({', '.join(param_names)})"
        
        if self._is_tree_type(signature.returns.type):
            return f"    auto result = {function_call};\n    cout << serializeTree(result) << endl;"
        else:
            return f"    auto result = {function_call};\n    cout << json(result) << endl;"
    
    def _is_tree_type(self, dsl_type: str) -> bool:
        """Check if the type is a tree type."""
        return 'Tree' in dsl_type
