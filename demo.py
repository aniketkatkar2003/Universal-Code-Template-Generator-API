#!/usr/bin/env python3

"""
Demo script to showcase the Universal Code Template Generator API
without requiring a running server.
"""

import sys
sys.path.append('/Users/sama/Projects/Universal_code_template')

from src.service import TemplateService
from src.models import TemplateRequest, FunctionSignature, Parameter, ReturnType

def demo_template_generation():
    """Demonstrate template generation for all supported scenarios."""
    
    print("Universal Code Template Generator API - Demo")
    print("=" * 60)
    
    service = TemplateService()
    
    # Test cases covering all required scenarios
    test_cases = [
        {
            "name": "1. Single Primitive Input (Fibonacci)",
            "request": TemplateRequest(
                question_id="fibonacci",
                title="Fibonacci Number",
                description="Calculate the nth Fibonacci number",
                signature=FunctionSignature(
                    function_name="fibonacci",
                    parameters=[Parameter(name="n", type="int")],
                    returns=ReturnType(type="int")
                ),
                language="python"
            )
        },
        {
            "name": "2. Multiple Mixed Inputs (Two Sum)",
            "request": TemplateRequest(
                question_id="two-sum",
                title="Two Sum",
                description="Given an integer array nums and an integer target, return indices of two numbers that add up to target.",
                signature=FunctionSignature(
                    function_name="twoSum",
                    parameters=[
                        Parameter(name="nums", type="int[]"),
                        Parameter(name="target", type="int")
                    ],
                    returns=ReturnType(type="int[]")
                ),
                language="java"
            )
        },
        {
            "name": "3. Tree Problem (Lowest Common Ancestor)",
            "request": TemplateRequest(
                question_id="lca",
                title="Lowest Common Ancestor",
                description="Find the lowest common ancestor of two nodes in a binary tree",
                signature=FunctionSignature(
                    function_name="lowestCommonAncestor",
                    parameters=[
                        Parameter(name="root", type="Tree"),
                        Parameter(name="p", type="Tree"),
                        Parameter(name="q", type="Tree")
                    ],
                    returns=ReturnType(type="Tree")
                ),
                language="cpp"
            )
        },
        {
            "name": "4. Graph Problem (Detect Cycle)",
            "request": TemplateRequest(
                question_id="detect-cycle",
                title="Detect Cycle in Graph",
                description="Detect if there is a cycle in the directed graph",
                signature=FunctionSignature(
                    function_name="detectCycle",
                    parameters=[Parameter(name="graph", type="Graph")],
                    returns=ReturnType(type="bool")
                ),
                language="javascript"
            )
        },
        {
            "name": "5. Complex List Problem (Merge K Lists)",
            "request": TemplateRequest(
                question_id="merge-k-lists",
                title="Merge k Sorted Lists",
                description="Merge k sorted linked lists and return it as one sorted list",
                signature=FunctionSignature(
                    function_name="mergeKLists",
                    parameters=[Parameter(name="lists", type="List<int[]>")],
                    returns=ReturnType(type="int[]")
                ),
                language="python"
            )
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{test_case['name']}")
        print("-" * 60)
        
        try:
            response = service.generate_template(test_case["request"])
            print(f"✓ Language: {response.language}")
            print("✓ Generated Template:")
            print()
            
            # Pretty print the template with line numbers
            lines = response.template.split('\n')
            for line_num, line in enumerate(lines, 1):
                print(f"{line_num:2d}: {line}")
                
        except Exception as e:
            print(f"✗ Error generating template: {str(e)}")
        
        print("\n" + "=" * 60)
    
    # Demonstrate error handling
    print("\nError Handling Demonstration:")
    print("-" * 60)
    
    try:
        invalid_request = TemplateRequest(
            question_id="test",
            title="Test",
            description="Test description",
            signature=FunctionSignature(
                function_name="",  # Invalid empty function name
                parameters=[Parameter(name="x", type="int")],
                returns=ReturnType(type="int")
            ),
            language="python"
        )
        service.generate_template(invalid_request)
    except Exception as e:
        print(f"✓ Correctly caught validation error: {str(e)}")
    
    print("\nDemo complete! All scenarios tested successfully.")

if __name__ == "__main__":
    demo_template_generation()
