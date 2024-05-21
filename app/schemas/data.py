from pydantic import BaseModel, Field
from typing import Annotated


class DataModel(BaseModel):
    phone: Annotated[str, Field(..., pattern=r"^[78]\d{10}$")]
    address: Annotated[str, Field(..., min_length=1)]


class RequestData(BaseModel):
    phone: Annotated[str, Field(..., pattern=r"^[78]\d{10}$")]


class ResponseCheckData(BaseModel):
    address: Annotated[str, Field()]
