from fastapi import FastAPI,Depends
import schemas , models 

from database import engine,get_db
from sqlalchemy.orm import Session
app = FastAPI()


models.Base.metadata.create_all(engine)



@app.post('/blog')
def create(blog: schemas.Blog ,db: Session = Depends(get_db) ):
    return blog