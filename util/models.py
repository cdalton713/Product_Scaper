from pydantic import BaseModel, validator
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


class WooVariant(BaseModel):
    @validator("*", pre=True, always=True)
    def replace_empty_string_with_none(cls, v):
        if v == "":
            return None
        return v

    attributes: Dict[str, str]
    availability_html = str
    backorders_allowed: bool
    dimensions: Dict[str, str]
    dimensions_html: str
    display_regular_price: float

    # TODO - not relevant right now
    image: Dict
    image_id: int
    is_downloadable: bool
    is_in_stock: bool
    is_purchasable: bool
    is_sold_individually: str
    is_virtual: bool
    max_qty: Optional[int]
    min_qty: int
    price_html: Optional[str] = None
    sku: str
    variation_description: Optional[str] = None
    variation_id: int
    variation_is_active: bool
    variation_is_visible: bool
    weight: str
    weight_html: str


class WooProduct(BaseModel):
    handle: str
    title: str
    variants: List[WooVariant]
