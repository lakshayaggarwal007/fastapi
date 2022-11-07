from fastapi import FastAPI
import schemas 
app = FastAPI()






@app.post('/blog')
def create(blog: schemas.Blog):
    return blog