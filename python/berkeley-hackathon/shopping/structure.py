from typing import List, Optional
from pydantic import BaseModel, Field

class Media(BaseModel):
    images: Optional[List[str]] = Field(
        None,
        description="List of image URLs related to the product."
    )

class ProductInfo(BaseModel):
    url: Optional[str] = Field(
        None,
        description="The product's URL."
    )
    title: Optional[str] = Field(
        None,
        description="The product's title or name."
    )
    description: Optional[str] = Field(
        None,
        description="A brief summary or short description of the product."
    )
    price: Optional[str] = Field(
        None,
        description="The current price of the product."
    )
    media: Optional[Media] = Field(
        None,
        description="Media-related information, including images."
    )

class SearchResult(BaseModel):
    products: Optional[List[ProductInfo]] = Field(
        None,
        description="A list of structured product search result items."
    )
