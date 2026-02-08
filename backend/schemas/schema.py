from sqlmodel import SQLModel
from typing import List, Optional
from datetime import datetime


class ProductRatingCreate(SQLModel):
    product_uid: str
    rating: float
    comment: str


class ProductListItem(SQLModel):
    id: int
    name: str
    uid: str

class ProductRatingRead(SQLModel):
    id: int
    rating: float
    comment: str
    created_on: datetime

class ProductDetail(SQLModel):
    id: int
    name: str
    uid: str
    created_on: datetime
    ratings: List[ProductRatingRead]