from typing import Union
from enum import Enum

from fastapi import FastAPI, Request, HTTPException, Query, Path
from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing_extensions import Annotated

from uuid import UUID, uuid4

import json


# initiates new project
app = FastAPI()
#initiates template
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    id:Union[int, None]=None
    name: str = "product"
    price: float
    is_offer: Union[bool, None] = None
    q: Union[str, None] = None

class Task(BaseModel):
    id:Union[UUID, None]=None
    title: str
    description:str
    completed: bool = False

# task mock db
tasks=[]

#item mock db
items=[]


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Task Route
@app.get('/tasks/', response_model=list[Task] )
async def read_tasks():
    return tasks

@app.post('/tasks/', response_model=Task )
async def add_task(task:Task)->Task:
    task.id=uuid4()
    tasks.append(task)
    return task

@app.get('/tasks/{task_id}', response_model=Task)
async def read_task(task_id:UUID):
    for task in tasks:
        if task.id==task_id:
            return task       
    raise HTTPException(status_code=404, detail='No task found')

@app.put('/tasks/{task_id}', response_model=Task)
async def read_task(task_id:UUID, task_apdate:Task):
    for index, task in enumerate(tasks):
        if task.id==task_id:
            updated_task = task.copy(update=task_apdate.model_dump(exclude_unset=True))
            tasks[index]=updated_task
            return updated_task       
    raise HTTPException(status_code=404, detail='No task found')

@app.delete('/tasks/{task_id}', response_model=Task)
async def delete_task(task_id:UUID):
    for index, task in enumerate(tasks):
        if task.id==task_id:
            return tasks.pop(index)       
    raise HTTPException(status_code=404, detail='No task found')


# Items Route
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