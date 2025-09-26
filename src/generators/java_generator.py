from typing import List
from ..models import FunctionSignature
from . import TemplateGenerator


class JavaGenerator(TemplateGenerator):
    """Template generator for Java."""
    
    def __init__(self):
        super().__init__('java')
    
    def generate_template(self, signature: FunctionSignature) -> str:
        """Generate Java template."""
        # Get all types for imports
        all_types = self.get_all_types(signature)
        imports = self.type_mapper.get_imports(all_types)
        
        # Build imports section
        imports_section = ""
        if imports:
            imports_section = "\n".join(imports) + "\n"
        
        # Add TreeNode definition if needed
        tree_node_def = ""
        if any('Tree' in t for t in all_types):
            tree_node_def = "\n" + self._get_tree_node_definition() + "\n"
        
        # Generate function signature
        params = []
        for param in signature.parameters:
            param_type = self.type_mapper.map_type(param.type)
            params.append(f"{param_type} {param.name}")
        
        return_type = self.type_mapper.map_type(signature.returns.type)
        
        class_template = f'''{imports_section}
import com.google.gson.*;
import java.util.*;
import java.io.*;

public class Solution {{
    public {return_type} {signature.function_name}({", ".join(params)}) {{
        // Write your logic here
        return null;
    }}
    
    public static void main(String[] args) throws IOException {{
        // Do not edit below this line
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {{
            sb.append(line);
        }}
        
        Gson gson = new Gson();
        JsonObject data = gson.fromJson(sb.toString(), JsonObject.class);
        
        Solution solution = new Solution();
        {self._generate_parameter_extraction(signature)}
        
        {self._generate_function_call(signature)}
        
        System.out.println(gson.toJson(result));
    }}
    
    {self._generate_helper_methods(all_types)}
}}{tree_node_def}'''
        
        return class_template
    
    def _get_tree_node_definition(self) -> str:
        """Get TreeNode class definition."""
        return '''// Definition for a binary tree node
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}'''
    
    def _generate_parameter_extraction(self, signature: FunctionSignature) -> str:
        """Generate parameter extraction code."""
        lines = []
        for param in signature.parameters:
            if self._is_tree_type(param.type):
                lines.append(f"        TreeNode {param.name} = deserializeTree(data.getAsJsonArray(\"{param.name}\"));")
            elif param.type == 'Graph':
                lines.append(f"        Map<Integer, List<Integer>> {param.name} = gson.fromJson(data.get(\"{param.name}\"), new TypeToken<Map<Integer, List<Integer>>>(){{}}.getType());")
            else:
                java_type = self.type_mapper.map_type(param.type)
                lines.append(f"        {java_type} {param.name} = gson.fromJson(data.get(\"{param.name}\"), {self._get_type_token(param.type)});")
        return "\n".join(lines)
    
    def _generate_function_call(self, signature: FunctionSignature) -> str:
        """Generate function call code."""
        param_names = [param.name for param in signature.parameters]
        return_type = self.type_mapper.map_type(signature.returns.type)
        
        if self._is_tree_type(signature.returns.type):
            return f"        {return_type} result = solution.{signature.function_name}({', '.join(param_names)});\n        JsonArray serialized = serializeTree(result);\n        result = serialized;"
        else:
            return f"        {return_type} result = solution.{signature.function_name}({', '.join(param_names)});"
    
    def _generate_helper_methods(self, all_types: List[str]) -> str:
        """Generate helper methods if needed."""
        if any('Tree' in t for t in all_types):
            return '''
    private static TreeNode deserializeTree(JsonArray data) {
        if (data == null || data.size() == 0) return null;
        
        TreeNode root = new TreeNode(data.get(0).getAsInt());
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        int i = 1;
        while (!queue.isEmpty() && i < data.size()) {
            TreeNode node = queue.poll();
            
            if (i < data.size() && !data.get(i).isJsonNull()) {
                node.left = new TreeNode(data.get(i).getAsInt());
                queue.offer(node.left);
            }
            i++;
            
            if (i < data.size() && !data.get(i).isJsonNull()) {
                node.right = new TreeNode(data.get(i).getAsInt());
                queue.offer(node.right);
            }
            i++;
        }
        
        return root;
    }
    
    private static JsonArray serializeTree(TreeNode root) {
        JsonArray result = new JsonArray();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            if (node != null) {
                result.add(node.val);
                queue.offer(node.left);
                queue.offer(node.right);
            } else {
                result.add((Integer) null);
            }
        }
        
        // Remove trailing nulls
        while (result.size() > 0 && result.get(result.size() - 1).isJsonNull()) {
            result.remove(result.size() - 1);
        }
        
        return result;
    }'''
        return ""
    
    def _get_type_token(self, dsl_type: str) -> str:
        """Get TypeToken for Gson deserialization."""
        java_type = self.type_mapper.map_type(dsl_type)
        return f"{java_type}.class"
    
    def _is_tree_type(self, dsl_type: str) -> bool:
        """Check if the type is a tree type."""
        return 'Tree' in dsl_type
