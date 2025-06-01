from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page : int | None = Field(1, ge=1)
    perpage : int | None = Field(5, ge=1, le=10)

PaginationDep = Annotated[PaginationParams, Depends()]
