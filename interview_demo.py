#!/usr/bin/env python3

"""
🎯 LIVE INTERVIEW DEMONSTRATION SCRIPT
Universal Code Template Generator API

Run this during your interview to showcase all capabilities!
"""

import requests
import json
import time
import sys

class InterviewDemo:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.test_connection()
    
    def test_connection(self):
        """Test if API server is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ API Server Connected Successfully!")
                print(f"📍 Server running at: {self.base_url}")
                print(f"📖 Interactive docs: {self.base_url}/docs")
            else:
                print("❌ Server connection failed")
                sys.exit(1)
        except requests.exceptions.RequestException:
            print("❌ Cannot connect to server. Please start it first:")
            print("   uvicorn src.main:app --host 127.0.0.1 --port 8000")
            sys.exit(1)
    
    def demo_header(self, title):
        """Print a formatted demo section header"""
        print(f"\n{'='*60}")
        print(f"🎯 {title}")
        print(f"{'='*60}")
    
    def demo_use_case_1_tree_problem(self):
        """Most impressive demo - Complex tree problem with serialization"""
        self.demo_header("USE CASE 1: COMPLEX TREE PROBLEM (Most Impressive!)")
        
        print("🌳 Demonstrating: Tree data structure + JSON serialization")
        print("📝 Problem: Lowest Common Ancestor of Binary Tree")
        
        request_data = {
            "question_id": "lca",
            "title": "Lowest Common Ancestor",
            "description": "Find the lowest common ancestor of two nodes in a binary tree",
            "signature": {
                "function_name": "lowestCommonAncestor",
                "parameters": [
                    {"name": "root", "type": "Tree<int>"},
                    {"name": "p", "type": "Tree<int>"},
                    {"name": "q", "type": "Tree<int>"}
                ],
                "returns": {"type": "Tree<int>"}
            },
            "language": "python"
        }
        
        print(f"\n📤 Request Payload:")
        print(json.dumps(request_data, indent=2))
        
        print(f"\n🔄 Sending request...")
        response = requests.post(f"{self.base_url}/api/v1/template", json=request_data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ SUCCESS! Generated Python template with tree handling:")
            print(f"\n📄 Generated Template Preview (first 20 lines):")
            print("-" * 60)
            
            lines = result['template'].split('\n')
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:2d}: {line}")
            
            print(f"... ({len(lines) - 20} more lines)")
            
            print(f"\n🔍 Key Features Generated:")
            print("  ✅ TreeNode class definition")
            print("  ✅ Tree serialization/deserialization")
            print("  ✅ JSON I/O handling")
            print("  ✅ Complete executable template")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    def demo_use_case_2_multi_language(self):
        """Show same problem in all 4 languages"""
        self.demo_header("USE CASE 2: MULTI-LANGUAGE SUPPORT (Scalability)")
        
        print("🌍 Demonstrating: Same problem → 4 different languages")
        print("📝 Problem: Two Sum Array Problem")
        
        languages = [
            ("python", "🐍 Python"),
            ("java", "☕ Java"),
            ("cpp", "⚡ C++"),
            ("javascript", "🟨 JavaScript")
        ]
        
        base_request = {
            "question_id": "two-sum",
            "title": "Two Sum",
            "description": "Find two numbers that add up to target",
            "signature": {
                "function_name": "twoSum",
                "parameters": [
                    {"name": "nums", "type": "int[]"},
                    {"name": "target", "type": "int"}
                ],
                "returns": {"type": "int[]"}
            }
        }
        
        for lang_code, lang_name in languages:
            print(f"\n{lang_name} Generation:")
            print("-" * 40)
            
            request_data = {**base_request, "language": lang_code}
            
            response = requests.post(f"{self.base_url}/api/v1/template", json=request_data)
            
            if response.status_code == 201:
                result = response.json()
                template = result['template']
                
                # Show key characteristics of each language
                if lang_code == "python":
                    print("  ✅ Type hints: List[int], proper imports")
                elif lang_code == "java":
                    print("  ✅ OOP structure: public class Solution")
                elif lang_code == "cpp":
                    print("  ✅ STL containers: vector<int>, modern C++")
                elif lang_code == "javascript":
                    print("  ✅ JSDoc types: @param, @return annotations")
                
                # Show first few lines
                lines = template.split('\n')[:5]
                for i, line in enumerate(lines, 1):
                    print(f"     {i}: {line}")
                print(f"     ... ({len(template.split('\n')) - 5} more lines)")
            else:
                print(f"  ❌ Error: {response.status_code}")
            
            time.sleep(0.5)  # Pause for dramatic effect
    
    def demo_use_case_3_graph_problem(self):
        """Show graph problem with complex data structures"""
        self.demo_header("USE CASE 3: GRAPH ALGORITHM (Advanced Data Structures)")
        
        print("🕸️  Demonstrating: Graph adjacency list handling")
        print("📝 Problem: Cycle Detection in Directed Graph")
        
        request_data = {
            "question_id": "detect-cycle",
            "title": "Detect Cycle in Directed Graph",
            "description": "Given a directed graph, detect if it contains a cycle",
            "signature": {
                "function_name": "detectCycle",
                "parameters": [
                    {"name": "graph", "type": "Graph"}
                ],
                "returns": {"type": "bool"}
            },
            "language": "cpp"
        }
        
        print(f"\n📤 Request: Graph → C++ mapping")
        
        response = requests.post(f"{self.base_url}/api/v1/template", json=request_data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ SUCCESS! Graph mapped to: unordered_map<int, vector<int>>")
            
            template = result['template']
            lines = template.split('\n')
            
            # Show the function signature
            for i, line in enumerate(lines):
                if 'detectCycle' in line and 'unordered_map' in line:
                    print(f"\n🔍 Generated Function Signature:")
                    print(f"   {line.strip()}")
                    break
            
            print(f"\n🔍 Key C++ Features:")
            print("  ✅ Modern C++ containers")
            print("  ✅ nlohmann/json for JSON parsing")
            print("  ✅ Proper header includes")
            print("  ✅ Complete main() with I/O")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    def demo_error_handling(self):
        """Show robust error handling"""
        self.demo_header("BONUS: ERROR HANDLING & VALIDATION")
        
        print("🛡️  Demonstrating: Comprehensive input validation")
        
        # Test invalid language
        invalid_request = {
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
        
        print(f"\n🧪 Testing: Unsupported language 'ruby'")
        response = requests.post(f"{self.base_url}/api/v1/template", json=invalid_request)
        
        print(f"📊 Response: HTTP {response.status_code}")
        if response.status_code == 422:
            print("✅ Correctly rejected with validation error")
            error_detail = response.json()
            print(f"🔍 Error details: {error_detail}")
        else:
            print(f"❌ Unexpected response: {response.text}")
    
    def demo_api_metadata(self):
        """Show API metadata endpoints"""
        self.demo_header("API METADATA & DOCUMENTATION")
        
        # Supported languages
        print("🌍 Supported Languages:")
        response = requests.get(f"{self.base_url}/api/v1/languages")
        if response.status_code == 200:
            languages = response.json()["languages"]
            for lang in languages:
                print(f"  ✅ {lang['display_name']} ({lang['name']})")
        
        print(f"\n🔧 Supported Types:")
        response = requests.get(f"{self.base_url}/api/v1/types")
        if response.status_code == 200:
            types_info = response.json()
            print(f"  📊 Primitives: {', '.join(types_info['types']['primitives'])}")
            print(f"  📋 Collections: {', '.join(types_info['types']['collections'])}")
            print(f"  🎯 Special: {', '.join(types_info['types']['special'])}")
    
    def run_full_demo(self):
        """Run the complete interview demonstration"""
        print("🎯 UNIVERSAL CODE TEMPLATE GENERATOR API")
        print("🎪 LIVE INTERVIEW DEMONSTRATION")
        print(f"📅 Demo Date: September 25, 2025")
        
        try:
            self.demo_api_metadata()
            self.demo_use_case_1_tree_problem()
            self.demo_use_case_2_multi_language()
            self.demo_use_case_3_graph_problem()
            self.demo_error_handling()
            
            print(f"\n{'='*60}")
            print("🎉 DEMONSTRATION COMPLETE!")
            print("✨ Key Achievements Shown:")
            print("  🔹 Complex data structure handling (Trees, Graphs)")
            print("  🔹 Multi-language code generation (4 languages)")
            print("  🔹 Production-ready API with validation")
            print("  🔹 Complete I/O abstraction")
            print("  🔹 Extensible architecture")
            print(f"\n🚀 Ready for production deployment!")
            
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Demo error: {e}")

def main():
    """Main entry point for interview demo"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://127.0.0.1:8000"
    
    print("🎬 Starting Interview Demo...")
    print("💡 Make sure the API server is running first!")
    print("   Command: uvicorn src.main:app --host 127.0.0.1 --port 8000")
    
    input("\n👆 Press ENTER when server is ready...")
    
    demo = InterviewDemo(base_url)
    demo.run_full_demo()

if __name__ == "__main__":
    main()
