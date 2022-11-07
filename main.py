from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app  = FastAPI()


@app.get('/about')
def index(limit=10,published :bool = True,sort : Optional[str] = None):
    if published:
        return {'data':f'{limit} published blogs from db'}
    else:
        return{'data':f'{limit} blogs from db'}

@app.get('/about')
def index():
    return {'data':'sadad'}

@app.get('/about/{id}')
def about(id:int):
    return {'data':id}

class Blog(BaseModel):
    title:str
    body:str
    published : Optional[bool]


@app.post('blog')
def create_blog(blog: Blog):
    return {'data':f'Blog is created with title as{blog.title}'}