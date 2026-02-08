from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated, Dict
import json
from backend.models.models import Product, ProductRating
from sqlmodel import SQLModel, Session, create_engine, select
from backend.db.database import create_tables, get_session
from backend.schemas.schema import ProductListItem, ProductDetail, ProductRatingCreate, ProductRatingRead

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(
    title="Product Rating",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_tables()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, product_uid: str, websocket: WebSocket):
        await websocket.accept()
        if product_uid not in self.active_connections:
            self.active_connections[product_uid] = []
        self.active_connections[product_uid].append(websocket)

    def disconnect(self, product_uid: str, websocket: WebSocket):
        if product_uid in self.active_connections:
            self.active_connections[product_uid].remove(websocket)
            if not self.active_connections[product_uid]:
                del self.active_connections[product_uid]

    async def broadcast(self, product_uid: str, message: dict):
        if product_uid in self.active_connections:
            connections = self.active_connections[product_uid].copy()
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error sending to websocket: {e}")
                    self.disconnect(product_uid, connection)

manager = ConnectionManager()

@app.get("/api/get-products", response_model=List[ProductListItem])
def get_products(session: SessionDep):
    stmt = select(Product).where(Product.is_deleted == False)
    return session.exec(stmt).all()

@app.get("/api/get-product/{product_uid}", response_model=ProductDetail)
def get_product_by_uid(product_uid: str, session: SessionDep):
    stmt = select(Product).where(Product.uid == product_uid)
    product = session.exec(stmt).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/submit-review/", response_model=ProductRatingRead)
async def submit_review(rating_data: ProductRatingCreate, session: SessionDep):
    stmt = select(Product).where(Product.uid == rating_data.product_uid)
    product = session.exec(stmt).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    rating = ProductRating(
        product_id=product.id,
        rating=rating_data.rating,
        comment=rating_data.comment
    )
    session.add(rating)
    session.commit()
    session.refresh(rating)

    await manager.broadcast(
        product_uid=rating_data.product_uid,
        message={
            "type": "rating_update",
            "product_uid": rating_data.product_uid,
            "latest_review": {
                "id": rating.id,
                "rating": rating.rating,
                "comment": rating.comment,
                "created_on": str(rating.created_on) if rating.created_on else None
            }
        }
    )
    return rating

@app.websocket("/ws/product/{product_uid}")
async def broadcast_review(websocket: WebSocket, product_uid: str):
    await manager.connect(product_uid, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except Exception as e:
        print(e)
    finally:
        manager.disconnect(product_uid, websocket)