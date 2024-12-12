from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Media(BaseModel):
    images: Optional[List[str]] = Field(
        None,
        description="List of image URLs related to the product."
    )
    videos: Optional[List[str]] = Field(
        None,
        description="List of video URLs related to the product."
    )

class ReviewBreakdown(BaseModel):
    positive: Optional[int] = Field(
        None,
        description="Number of positive reviews."
    )
    neutral: Optional[int] = Field(
        None,
        description="Number of neutral reviews."
    )
    negative: Optional[int] = Field(
        None,
        description="Number of negative reviews."
    )

class HtmlSearchTextChunk(BaseModel):
    url: Optional[str] = Field(
        None,
        description="The product or item's URL."
    )
    product_id: Optional[str] = Field(
        None,
        description="A unique identifier for the product."
    )
    sku: Optional[str] = Field(
        None,
        description="The Stock Keeping Unit (SKU) for the product."
    )
    model: Optional[str] = Field(
        None,
        description="The model name or number of the product."
    )
    title: Optional[str] = Field(
        None,
        description="The product's title or name."
    )
    description: Optional[str] = Field(
        None,
        description="A detailed description of the product."
    )
    short_description: Optional[str] = Field(
        None,
        description="A brief summary or short description of the product."
    )
    brand: Optional[str] = Field(
        None,
        description="The brand name of the product."
    )
    category: Optional[str] = Field(
        None,
        description="The category under which the product is listed."
    )
    category_hierarchy: Optional[List[str]] = Field(
        None,
        description="A hierarchical list representing the category path, e.g., ['Electronics','Phones','Smartphones']."
    )
    price: Optional[float] = Field(
        None,
        description="The current price of the product."
    )
    currency: Optional[str] = Field(
        None,
        description="The currency code for the product's price, e.g., 'USD', 'CNY'."
    )
    original_price: Optional[float] = Field(
        None,
        description="The original or list price before any discounts."
    )
    discount_info: Optional[str] = Field(
        None,
        description="Information about any discounts or promotions available."
    )
    availability: Optional[str] = Field(
        None,
        description="The stock or availability status of the product."
    )
    rating: Optional[float] = Field(
        None,
        description="The average rating of the product, typically on a scale like 1-5."
    )
    reviews_count: Optional[int] = Field(
        None,
        description="The total number of reviews received by the product."
    )
    reviews_breakdown: Optional[ReviewBreakdown] = Field(
        None,
        description="A breakdown of reviews into positive, neutral, and negative counts."
    )
    seller_info: Optional[str] = Field(
        None,
        description="Information about the seller or vendor offering the product."
    )
    attributes: Optional[Dict[str, str]] = Field(
        None,
        description="Additional attributes of the product, e.g. {'Color':'Black','Storage':'128GB'}."
    )
    specifications: Optional[Dict[str, str]] = Field(
        None,
        description="Technical or detailed specifications of the product, e.g. {'Screen Size':'6.5 inches','Battery':'4000mAh'}."
    )
    media: Optional[Media] = Field(
        None,
        description="Media-related information, including images and videos."
    )
    shipping_info: Optional[str] = Field(
        None,
        description="Information related to shipping, e.g., 'Free shipping' or delivery time estimates."
    )
    warranty_info: Optional[str] = Field(
        None,
        description="Warranty details provided with the product."
    )
    tags: Optional[List[str]] = Field(
        None,
        description="List of tags or keywords associated with the product."
    )

class HtmlSearchText(BaseModel):
    chunks: Optional[List[HtmlSearchTextChunk]] = Field(
        None,
        description="A list of structured product search result items."
    )
