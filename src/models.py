from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class SupportedLanguage(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    JAVASCRIPT = "javascript"


class Parameter(BaseModel):
    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type in DSL format")


class ReturnType(BaseModel):
    type: str = Field(..., description="Return type in DSL format")


class FunctionSignature(BaseModel):
    function_name: str = Field(..., description="Name of the function")
    parameters: List[Parameter] = Field(..., description="List of function parameters")
    returns: ReturnType = Field(..., description="Return type specification")


class TemplateRequest(BaseModel):
    question_id: str = Field(..., description="Unique identifier for the question")
    title: str = Field(..., description="Human-readable title")
    description: str = Field(..., description="Problem description")
    signature: FunctionSignature = Field(..., description="Function signature specification")
    language: SupportedLanguage = Field(..., description="Target programming language")


class TemplateResponse(BaseModel):
    language: str = Field(..., description="Programming language")
    template: str = Field(..., description="Generated code template")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
