from pydantic import BaseModel, validator
from typing import List, Optional
import pendulum


class Request(BaseModel):
    date: pendulum.Date = pendulum.today(pendulum.tz.UTC).date()

    @validator("date", each_item=True, always=True)
    def date_val(cls, v):
        return pendulum.from_format(str(v), "YYYY-MM-DD")

    class Config:
        arbitrary_types_allowed = True


class Condition(BaseModel):
    uuid: str
    display_name: str


class Category(BaseModel):
    uuid: str
    full_name: str


class Price(BaseModel):
    amount: float
    currency: str
    symbol: Optional[str]


class ReverbListing(BaseModel):
    id: int
    make: str
    model: str
    finish: Optional[str]
    year: Optional[str]
    title: str
    created_at: pendulum.DateTime
    published_at: Optional[pendulum.DateTime]
    shop_name: str
    price: Price
    categories: Optional[List[Category]]
    condition: Optional[Condition]

    class Config:
        arbitrary_types_allowed = True

    @validator('created_at', 'published_at', pre=True, always=True)
    def set_dates(cls, v: str):
        parsed = pendulum.parse(v)
        return pendulum.parse(parsed.strftime("%Y-%m-%dT00:00:00-00:00"))


class ReverbListings(BaseModel):
    listings: List[ReverbListing]

