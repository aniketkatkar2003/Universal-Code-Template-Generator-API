# Universal Code Template Generator API - Design Document

## Architecture Overview

The Universal Code Template Generator API is a production-ready HTTP service built using FastAPI that generates executable code templates for coding interview problems across multiple programming languages.

### High-Level Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   FastAPI App   │────▶│ Template Service │────▶│ Generator Layer │
│   (HTTP Layer)  │     │ (Business Logic)│     │   (Templates)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Pydantic Models │     │ Validation Logic│     │  Type Mappers   │
│ (Data Validation│     │                 │     │  (DSL→Language) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Core Components

#### 1. HTTP API Layer (`src/main.py`)
- **FastAPI Application**: Handles HTTP requests and responses
- **Endpoint Management**: RESTful API endpoints with proper HTTP status codes
- **Error Handling**: Comprehensive error handling with detailed error responses
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

#### 2. Business Logic Layer (`src/service.py`)
- **TemplateService**: Core business logic for template generation
- **Request Validation**: Business rule validation beyond schema validation
- **Error Management**: Converts technical errors to user-friendly messages

#### 3. Data Models (`src/models.py`)
- **Pydantic Models**: Strong typing and automatic validation
- **Request/Response DTOs**: Clear contracts for API communication
- **Enum Constraints**: Type-safe language selection

#### 4. Type System (`src/type_mappers.py`)
- **DSL Abstraction**: Language-agnostic type specification
- **Type Mapping**: DSL to language-specific type conversion
- **Import Management**: Automatic import statement generation

#### 5. Template Generation (`src/generators/`)
- **Abstract Generator**: Base class defining the template generation contract
- **Language-Specific Generators**: Concrete implementations for each supported language
- **Factory Pattern**: Clean generator instantiation and management

## Template Generation Strategy

### DSL (Domain-Specific Language)
The API uses a custom DSL for type specification that abstracts away language-specific details:

- **Primitives**: `int`, `long`, `float`, `double`, `bool`, `string`
- **Collections**: `T[]` (arrays), `List<T>` (lists/vectors)
- **Special Types**: `Tree<T>` (binary trees), `Graph` (adjacency lists)

### Type Mapping Strategy
Each language has a dedicated type mapper that converts DSL types to idiomatic language types:

```python
# Example: DSL "int[]" mapping
Python:    List[int]
Java:      int[]
C++:       vector<int>
JavaScript: number[]
```

### Template Structure
Each generated template follows a consistent structure:

1. **Imports/Includes**: Language-specific dependencies
2. **Helper Classes**: TreeNode, utility functions when needed
3. **Solution Class/Function**: User's implementation area
4. **I/O Handling**: JSON parsing and output formatting
5. **Main Entry Point**: Program execution logic

### I/O Strategy
All templates use JSON for input/output to ensure consistency:

- **Input**: JSON object with parameter names as keys
- **Processing**: Automatic deserialization of complex types (trees, graphs)
- **Output**: JSON-serialized results

## Language-Specific Implementations

### Python Generator
- **Class-based**: Uses `Solution` class pattern
- **Type Hints**: Full type annotation support
- **JSON Handling**: Native `json` module
- **Tree Serialization**: Custom TreeHelper class

### Java Generator
- **OOP Structure**: Public class with main method
- **Dependencies**: Gson for JSON, utility imports
- **Type Safety**: Proper generic type handling
- **Exception Handling**: IOException management

### C++ Generator
- **Modern C++**: C++20 features and STL
- **JSON Library**: nlohmann/json for JSON parsing
- **Memory Management**: Proper pointer handling for trees
- **Performance**: Optimized data structures

### JavaScript Generator
- **Function-based**: Simple function declarations
- **Node.js**: readline interface for input
- **Dynamic Types**: JSDoc comments for type documentation
- **Async I/O**: Event-driven input processing

## Extensibility Design

### Adding New Languages

1. **Create Type Mapper**: Implement `TypeMapper` interface
2. **Create Generator**: Extend `TemplateGenerator` base class
3. **Update Factory**: Add mapping in `GeneratorFactory`
4. **Update Models**: Add language to `SupportedLanguage` enum

### Adding New DSL Types

1. **Update Type Mappers**: Add mapping rules for all languages
2. **Update Generators**: Handle special serialization if needed
3. **Add Tests**: Ensure all language generators handle the new type
4. **Update Documentation**: Document the new type in API docs

### Template Customization
The modular design allows for easy customization:

- **I/O Format**: Change serialization strategy
- **Code Style**: Modify language-specific formatting
- **Helper Functions**: Add language-specific utilities
- **Validation Rules**: Extend business logic validation

## Future Extensibility

### Planned Enhancements

1. **Additional Languages**: 
   - Go, Rust, Kotlin, Swift
   - Language-specific package managers

2. **Advanced Type System**:
   - Generic constraints
   - Custom data structures
   - Interface definitions

3. **Template Customization**:
   - User-defined code style preferences
   - Framework-specific templates (React, Spring Boot)
   - Testing framework integration

4. **Performance Optimizations**:
   - Template caching
   - Parallel generation
   - CDN distribution

### Scalability Considerations

- **Stateless Design**: No server-side state for easy horizontal scaling
- **Caching Layer**: Redis integration for frequently requested templates
- **Rate Limiting**: API throttling for production deployment
- **Monitoring**: Metrics and logging for observability

## Quality Assurance

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Snapshot Testing**: Template output verification
- **Error Handling Tests**: Comprehensive error scenario coverage

### Code Quality
- **Type Safety**: Strong typing with Pydantic and type hints
- **Code Coverage**: >80% test coverage requirement
- **Linting**: Automated code style enforcement
- **Documentation**: Comprehensive API documentation

This design ensures the system is maintainable, extensible, and production-ready while meeting all functional requirements specified in the original specification.
