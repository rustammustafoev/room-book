from typing import Generic, Optional, TypeVar, List

from pydantic.generics import GenericModel
from pydantic import Field, AnyHttpUrl


M = TypeVar('M')


class PaginatedPerPageResponse(GenericModel, Generic[M]):
    count: int = Field(description='Number of total items')
    next_page: Optional[AnyHttpUrl] = Field(None, description='url of the next page if it exists')
    previous_page: Optional[AnyHttpUrl] = Field(None, description='url of the previous page if it exists')
    items: List[M] = Field(description='List of items returned in a paginated response')


class PaginatedResponse(GenericModel, Generic[M]):
    page: int
    count: int
    page_size: int
    results: List[M]
