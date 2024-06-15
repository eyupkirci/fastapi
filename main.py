from typing import Union
from enum import Enum

from fastapi import FastAPI, Request
from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing_extensions import Annotated

import json


# initiates new project
app = FastAPI()
#initiates template
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str = "product"
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None)->dict:
    return {"item_id": item_id, "q": q}

@app.post("/items/{item_id}")
def update_item(item_id: int, item: Annotated[Item, 'It is an Item class instance' ], q:Union[str, None]=None) -> dict:
    message = q
    return {"item_name": item.name, "item_id": item_id, "is_offer":item.is_offer, "message":message}

@app.get("/items/{item_id}/new")
def read_item(item_id: int, q1: Union[str, None] = None, q2: Union[str, None] = None,)->dict:
    return {"item_id": item_id, "query1": q1, "query2": q2, }

@app.get("/items/{item_id}/page", response_class=HTMLResponse)
async def read_index(request: Request, item_id: int, item: Item, q: str | None = None):
    requestBody = await request.body()
    json_data = json.loads(requestBody)
    print(json_data)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "item_id": item_id,
        "item": item,
        "message":q
    })

app.mount("/static", StaticFiles(directory="static"), name="static")