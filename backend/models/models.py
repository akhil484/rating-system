from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import secrets
import string

ALPHABET = string.ascii_uppercase + string.digits

def generate_uid():
    return "".join(secrets.choice(ALPHABET) for _ in range(8))

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    uid: str = Field(default_factory=generate_uid,unique=True, index=True, nullable=False)
    ratings: List["ProductRating"] = Relationship(back_populates="product")
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = Field(default=False)


class ProductRating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="ratings")
    rating: float = Field()
    comment: str = Field()
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
