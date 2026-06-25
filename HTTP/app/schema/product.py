from pydantic import BaseModel, Field, EmailStr,AnyUrl, field_validator,model_validator,computed_field
from typing import Optional,List,Literal
from uuid import UUID

class Seller(BaseModel):
    id: UUID
    name: str = Field(min_length=2,max_lenght=60)
    email: EmailStr
    website: AnyUrl

    @field_validator("email",mode="after")
    @classmethod
    def validate_seller_email_domain(cls,value:str):
        allowed__domains = ["mistore.in","hpworld.in"]
        domain = value.split("@")[-1].lower()
        if domain not in allowed__domains:
            raise ValueError(f"Seller email domain not allowed: {domain}")
        return value

class Dimensions(BaseModel):
    width: float
    hright: float
    lenght: float

class Product(BaseModel):
    id : UUID
    sku: str = Field(min_length=0,max_length=30,title="SKU")
    name: str = Field(max_length=200)
    category: str
    brand: str
    price: float =Field(gt=0)
    currency = Literal["INR"]
    discount: int = Field(ge=0)
    is_active: bool
    rating: float
    tags: Optional[List[str]] = Field(default=None,max_length=10)
    image_urls: List[AnyUrl] = Field(min_lenght=1)
    dimensions_cm: Dimensions
    seller: Seller


@field_validator("sku",mode="after")
@classmethod
def validate_sku_format(cls,value: str):
    if "-" not in value:
        raise ValueError("SKU must have -")
    last = value.split("-")[-1]
    if not (len(last)) == 3 and last.isdigit():
        raise ValueError("SKU must end with 3 digit sequence")
    return value

@model_validator(mode="after")
def validate_buisness_rules(self):
    if self.stock == 0 and self.is_active is True:
        raise ValueError("If stock is zero,active must be false")
    if self.discount > 0 and self.rating == 0:
        raise ValueError("Discounted product must have rating not 0")
    return self

@computed_field
@property
def final_price(self) -> float:
    return round(self.price * (1 - self.discount /100), 2)

@computed_field
@property
def volume(self) -> float:
    return round(self.dimensions_cm.length * self.dimensions_cm.width * self.dimensions_cm.height, 2)