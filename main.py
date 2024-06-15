from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item, q:Union[str, None]=None):
    message = q
    return {"item_name": item.name, "item_id": item_id, "is_offer":item.is_offer, "message":message}

@app.get("/items/{item_id}/page", response_class=HTMLResponse)
async def read_index(request: Request, item_id: int, item: Item, q:Union[str, None]=None):
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