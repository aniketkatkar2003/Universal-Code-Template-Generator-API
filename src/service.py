from .models import TemplateRequest, TemplateResponse
from .generators.factory import GeneratorFactory


class TemplateService:
    """Service class for generating code templates."""
    
    def __init__(self):
        self.generator_factory = GeneratorFactory()
    
    def generate_template(self, request: TemplateRequest) -> TemplateResponse:
        """Generate a code template based on the request."""
        try:
            # Get the appropriate generator
            generator = self.generator_factory.get_generator(request.language)
            
            # Generate the template
            template_code = generator.generate_template(request.signature)
            
            return TemplateResponse(
                language=request.language,
                template=template_code
            )
            
        except Exception as e:
            raise ValueError(f"Failed to generate template: {str(e)}")
    
    def validate_request(self, request: TemplateRequest) -> bool:
        """Validate the template request."""
        # Check if language is supported
        supported_languages = ['python', 'java', 'cpp', 'javascript']
        if request.language not in supported_languages:
            raise ValueError(f"Unsupported language: {request.language}")
        
        # Check if function name is valid
        if not request.signature.function_name:
            raise ValueError("Function name cannot be empty")
        
        # Check if parameters are valid
        for param in request.signature.parameters:
            if not param.name:
                raise ValueError("Parameter name cannot be empty")
            if not param.type:
                raise ValueError("Parameter type cannot be empty")
        
        # Check if return type is valid
        if not request.signature.returns.type:
            raise ValueError("Return type cannot be empty")
        
        return True
