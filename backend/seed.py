from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from models.models import Product, ProductRating
from sqlmodel import SQLModel, Session, create_engine, select
from db.database import engine

product_names = [
    "The Minimalist Entrepreneur",
    "Travel Buddy",
    "Resume Builder",
    "100hour Work Week",
    "Travel Buddy",
]

def seed_data():
    with Session(engine) as session:

        products = []

        for i in range(0, 5):  # 5 products
            product = Product(
                name=product_names[i],
                is_deleted=False,
            )

            session.add(product)
            session.commit()
            session.refresh(product)

            # 5 ratings per product
            ratings = [
                ProductRating(
                    product_id=product.id,
                    rating=4.3,              # decimal
                    comment="Very good product"
                ),
                ProductRating(
                    product_id=product.id,
                    rating=3.8,              # decimal
                    comment="Good, but can improve"
                ),
                ProductRating(
                    product_id=product.id,
                    rating=5.0,
                    comment="Excellent!"
                ),
                ProductRating(
                    product_id=product.id,
                    rating=4.0,
                    comment="Worth the price"
                ),
                ProductRating(
                    product_id=product.id,
                    rating=2.4,
                    comment="Average experience"
                ),
            ]

            session.add_all(ratings)
            session.commit()

            products.append(product)

        print("✅ Seed data inserted successfully")


if __name__ == "__main__":
    seed_data()