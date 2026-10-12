
from typing import Dict, List, Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[List[Dict[str, str]]] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail