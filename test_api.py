#!/usr/bin/env python3

import requests
import json
import sys

def test_api():
    """Test the Universal Code Template Generator API."""
    base_url = "http://localhost:8000"
    
    print("Testing Universal Code Template Generator API")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print("✗ Health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure it's running on localhost:8000")
        return False
    
    # Test supported languages
    response = requests.get(f"{base_url}/api/v1/languages")
    if response.status_code == 200:
        print("✓ Languages endpoint works")
        languages = response.json()["languages"]
        print(f"  Supported languages: {[lang['name'] for lang in languages]}")
    else:
        print("✗ Languages endpoint failed")
    
    # Test template generation - Python TwoSum
    print("\n" + "=" * 50)
    print("Testing Template Generation")
    
    test_cases = [
        {
            "name": "Python TwoSum",
            "request": {
                "question_id": "two-sum",
                "title": "Two Sum",
                "description": "Given an integer array nums and an integer target, return indices of the two numbers such that they add up to target.",
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
        },
        {
            "name": "Java Fibonacci",
            "request": {
                "question_id": "fibonacci",
                "title": "Fibonacci Number",
                "description": "Calculate the nth Fibonacci number",
                "signature": {
                    "function_name": "fibonacci",
                    "parameters": [{"name": "n", "type": "int"}],
                    "returns": {"type": "int"}
                },
                "language": "java"
            }
        },
        {
            "name": "C++ Tree Problem",
            "request": {
                "question_id": "inorder-traversal",
                "title": "Binary Tree Inorder Traversal",
                "description": "Return the inorder traversal of a binary tree",
                "signature": {
                    "function_name": "inorderTraversal",
                    "parameters": [{"name": "root", "type": "Tree<int>"}],
                    "returns": {"type": "int[]"}
                },
                "language": "cpp"
            }
        },
        {
            "name": "JavaScript Graph Problem",
            "request": {
                "question_id": "detect-cycle",
                "title": "Detect Cycle in Graph",
                "description": "Detect if there is a cycle in the directed graph",
                "signature": {
                    "function_name": "detectCycle",
                    "parameters": [{"name": "graph", "type": "Graph"}],
                    "returns": {"type": "bool"}
                },
                "language": "javascript"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        response = requests.post(
            f"{base_url}/api/v1/template",
            json=test_case["request"],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print(f"✓ {test_case['name']} template generated successfully")
            result = response.json()
            print(f"  Language: {result['language']}")
            print("  Template preview:")
            # Show first few lines of the template
            template_lines = result['template'].split('\n')
            for i, line in enumerate(template_lines[:5]):
                print(f"    {line}")
            if len(template_lines) > 5:
                print(f"    ... ({len(template_lines) - 5} more lines)")
        else:
            print(f"✗ {test_case['name']} template generation failed")
            print(f"  Status: {response.status_code}")
            print(f"  Error: {response.text}")
    
    # Test error handling
    print(f"\n" + "=" * 50)
    print("Testing Error Handling")
    
    # Test unsupported language (should be caught by Pydantic validation)
    invalid_request = {
        "question_id": "test",
        "title": "Test",
        "description": "Test description",
        "signature": {
            "function_name": "test",
            "parameters": [{"name": "x", "type": "int"}],
            "returns": {"type": "int"}
        },
        "language": "ruby"  # Unsupported
    }
    
    response = requests.post(
        f"{base_url}/api/v1/template",
        json=invalid_request,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 422:  # Pydantic validation error
        print("✓ Unsupported language properly rejected")
    else:
        print(f"✗ Expected 422, got {response.status_code}")
    
    print("\nAPI testing complete!")
    return True

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
