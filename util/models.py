from pydantic import BaseModel
from datetime import datetime
from typing import List, Union, Dict, Optional


class ShopifyVariant(BaseModel):
    id: int
    title: str
    option1: Union[str, None]
    option2: Union[str, None]
    option3: Union[str, None]
    sku: str
    requires_shipping: bool
    taxable: bool

    # TODO - ShopifyFeaturedImage. Not relevant for this part project.
    featured_image: Optional[Dict] = None

    available: bool
    price: float
    grams: float
    compare_at_price: Optional[float] = None
    position: int
    product_id: int
    created_at: datetime
    updated_at: datetime


class ShopifyOption(BaseModel):
    name: str
    position: int
    values: Optional[List[str]] = None


class ShopifyProduct(BaseModel):
    id: int
    title: str
    handle: str
    body_html: str
    published_at: datetime
    created_at: datetime
    uploaded_at: Optional[datetime] = None
    vendor: str
    product_type: str

    tags: List[str]
    variants: List[ShopifyVariant]
    options: List[ShopifyOption]
