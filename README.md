# Universal Code Template Generator API

A production-ready HTTP API that generates executable code templates for coding interview problems, similar to LeetCode, HackerRank, or CodeSignal starter code.

## Features

- **Multi-language support**: Java 17, Python 3.12, C++20, JavaScript (Node 20)
- **Type-safe DSL**: Language-agnostic type system for function signatures
- **Complete I/O handling**: Generated templates handle JSON parsing and output formatting
- **Production-ready**: Built with FastAPI, includes comprehensive error handling and validation
- **Extensible**: Easy to add support for new languages

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Universal_code_template
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

```bash
# Development server
python -m src.main

# Or with uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Usage

### Generate Template

**POST** `/api/v1/template`

Generate a code template for a specific problem and language.

#### Request Body

```json
{
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
```

#### Response

```json
{
  "language": "python",
  "template": "from typing import List\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        # Write your logic here\n        pass\n\nif __name__ == \"__main__\":\n    # Do not edit below this line\n    import sys\n    import json\n    \n    data = json.loads(sys.stdin.read())\n    solution = Solution()\n    \n    nums = data['nums']\n    target = data['target']\n    \n    result = solution.twoSum(nums, target)\n    print(json.dumps(result))"
}
```

### Supported Languages

**GET** `/api/v1/languages`

Returns list of supported programming languages.

### Supported Types

**GET** `/api/v1/types`

Returns information about the DSL type system.

## Type System (DSL)

The API uses a language-agnostic DSL for type specifications:

| DSL Type | Description | Python | Java | C++ | JavaScript |
|----------|-------------|--------|------|-----|------------|
| `int` | 32-bit signed integer | `int` | `int` | `int` | `number` |
| `long` | 64-bit signed integer | `int` | `long` | `long long` | `number` |
| `float` | 32-bit float | `float` | `float` | `float` | `number` |
| `double` | 64-bit float | `float` | `double` | `double` | `number` |
| `bool` | Boolean | `bool` | `boolean` | `bool` | `boolean` |
| `string` | UTF-8 string | `str` | `String` | `string` | `string` |
| `T[]` | Dynamic array | `List[T]` | `T[]` | `vector<T>` | `T[]` |
| `List<T>` | List/Vector | `List[T]` | `List<T>` | `vector<T>` | `T[]` |
| `Tree<T>` | Binary tree node | `Optional[TreeNode[T]]` | `TreeNode<T>` | `TreeNode<T>*` | `TreeNode` |
| `Graph` | Adjacency list | `Dict[int, List[int]]` | `Map<Integer, List<Integer>>` | `unordered_map<int, vector<int>>` | `Map<number, number[]>` |

## Examples

### Example 1: Simple Function (Fibonacci)

```json
{
  "question_id": "fibonacci",
  "title": "Fibonacci Number",
  "description": "Calculate the nth Fibonacci number",
  "signature": {
    "function_name": "fibonacci",
    "parameters": [{"name": "n", "type": "int"}],
    "returns": {"type": "int"}
  },
  "language": "python"
}
```

### Example 2: Array Processing (Two Sum)

```json
{
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
  },
  "language": "java"
}
```

### Example 3: Tree Problem

```json
{
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
```

### Example 4: Graph Problem

```json
{
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
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

## Project Structure

```
Universal_code_template/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models.py              # Pydantic models
│   ├── service.py             # Business logic
│   ├── type_mappers.py        # DSL to language type mapping
│   └── generators/
│       ├── __init__.py
│       ├── factory.py         # Generator factory
│       ├── python_generator.py
│       ├── java_generator.py
│       ├── cpp_generator.py
│       └── javascript_generator.py
├── tests/
│   ├── test_main.py           # API integration tests
│   ├── test_type_mappers.py   # Type mapper unit tests
│   └── test_generators.py     # Generator unit tests
├── requirements.txt
└── README.md
```

## Error Handling

The API provides detailed error responses for various scenarios:

### 400 Bad Request - Validation Error

```json
{
  "error": "Validation failed",
  "details": {
    "signature.function_name": "Field required",
    "language": "Input should be 'python', 'java', 'cpp', or 'javascript'"
  }
}
```

### 400 Bad Request - Business Logic Error

```json
{
  "error": "Unsupported language: ruby",
  "details": null
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error", 
  "details": null
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License
