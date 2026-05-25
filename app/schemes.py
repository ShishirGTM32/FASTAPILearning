from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, List

from sqlalchemy import Boolean

T = TypeVar("T")

class SuccessResponse(GenericModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)
    success: bool = True
    message: str
    data : T


class ErrorResponse(GenericModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    success: bool = False
    error: str

class PaginatedResponse(GenericModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    data: list[T]
    total: int
    page: int
    size: int

class TokenPayload(GenericModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    
    
    
