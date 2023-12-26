from typing import Union
from fastapi import FastAPI
from app.db import get_database
from app.api import auth
app = FastAPI(
    title="snapfotoAPI",
    description="Nơi tình yêu của bạn được chia sẻ qua từng bức ảnh.",
    summary="Dev by Steve.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Steve",
        "url": "https://fb.com/huuhieu2001",
        "email": "huuhieu1711@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    })


# router
app.include_router(auth.router)

async def startup_db_client():
    app.mongodb = get_database() 

async def shutdown_db_client():
    app.mongodb

app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)

@app.get("/")
def hello_world():
    return {"hello": "world"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}