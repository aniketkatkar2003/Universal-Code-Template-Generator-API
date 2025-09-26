from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import traceback

from .models import TemplateRequest, TemplateResponse, ErrorResponse
from .service import TemplateService

app = FastAPI(
    title="Universal Code Template Generator API",
    description="Generate executable code templates for coding interview problems",
    version="1.0.0"
)

# Initialize the template service
template_service = TemplateService()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Universal Code Template Generator API", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "template-generator"}


@app.post(
    "/api/v1/template",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def generate_template(request: TemplateRequest):
    """
    Generate a code template for the specified programming language and problem signature.
    
    This endpoint accepts a JSON payload describing the coding problem, its function signature,
    and the target programming language, then returns a compilable/runnable template that hides
    all I/O and boilerplate from the end user.
    
    Supported languages: Java 17, Python 3.12, C++20, JavaScript (Node 20)
    """
    try:
        # Validate the request
        template_service.validate_request(request)
        
        # Generate the template
        response = template_service.generate_template(request)
        
        return response
        
    except ValidationError as e:
        error_details = {}
        for error in e.errors():
            field = ".".join(str(x) for x in error["loc"])
            error_details[field] = error["msg"]
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Validation failed",
                "details": error_details
            }
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": str(e),
                "details": None
            }
        )
    
    except Exception as e:
        # Log the error (in production, you'd use proper logging)
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "details": None
            }
        )


@app.get("/api/v1/languages")
async def get_supported_languages():
    """Get the list of supported programming languages."""
    return {
        "languages": [
            {"name": "python", "display_name": "Python 3.12"},
            {"name": "java", "display_name": "Java 17"},
            {"name": "cpp", "display_name": "C++20"},
            {"name": "javascript", "display_name": "JavaScript (Node 20)"}
        ]
    }


@app.get("/api/v1/types")
async def get_supported_types():
    """Get the list of supported DSL types."""
    return {
        "types": {
            "primitives": ["int", "long", "float", "double", "bool", "string"],
            "collections": ["T[]", "List<T>"],
            "special": ["Tree<T>", "Tree", "Graph"]
        },
        "examples": {
            "int[]": "Array of integers",
            "List<int>": "List of integers", 
            "Tree<int>": "Binary tree with integer values",
            "Graph": "Adjacency list representation"
        }
    }


# Custom exception handler for validation errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    error_details = {}
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"])
        error_details[field] = error["msg"]
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation failed",
            "details": error_details
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
