from abc import ABC, abstractmethod
from typing import List
from ..models import FunctionSignature
from ..type_mappers import get_type_mapper


class TemplateGenerator(ABC):
    """Abstract base class for template generators."""
    
    def __init__(self, language: str):
        self.language = language
        self.type_mapper = get_type_mapper(language)
    
    @abstractmethod
    def generate_template(self, signature: FunctionSignature) -> str:
        """Generate a complete code template."""
        pass
    
    def get_all_types(self, signature: FunctionSignature) -> List[str]:
        """Extract all DSL types from the signature."""
        types = [param.type for param in signature.parameters]
        types.append(signature.returns.type)
        return types
