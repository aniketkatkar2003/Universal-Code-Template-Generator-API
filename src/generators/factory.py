from .python_generator import PythonGenerator
from .java_generator import JavaGenerator
from .cpp_generator import CppGenerator
from .javascript_generator import JavaScriptGenerator
from . import TemplateGenerator


class GeneratorFactory:
    """Factory class for creating template generators."""
    
    _generators = {
        'python': PythonGenerator,
        'java': JavaGenerator,
        'cpp': CppGenerator,
        'javascript': JavaScriptGenerator
    }
    
    @classmethod
    def get_generator(cls, language: str) -> TemplateGenerator:
        """Get the appropriate template generator for the language."""
        if language not in cls._generators:
            raise ValueError(f"Unsupported language: {language}")
        
        return cls._generators[language]()
