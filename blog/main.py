from fastapi import FastAPI,Depends,status,Response,HTTPException,Request
import schemas , models 
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from hashing import Hash

app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/login',tags=['Authentication'])
def login():
    return 'login'



@app.post('/user',response_model=schemas.ShowUser,tags=['Users'])
def create_user(request:schemas.User, db:Session = Depends(get_db)):
    
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@app.get('/user/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowUser,tags=['Users'])
def get_user(id:int,db:Session = Depends(get_db)):
    User = db.query(models.User).filter(models.User.id==id).first()
    if not User:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the id {id} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'details':f'blog with the id {id} not available'}
    return User




@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def create(blog: schemas.Blog ,db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title,body =blog.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def destroy(id,db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with the id {id} not found')
    
    blog.delete(synchronize_session=False) 
    db.commit()
    return 'the blog is deleted from the database'


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['Blogs'])
def update(id,request: schemas.Blog , db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with the id {id} not found')
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'
    
    
    
@app.get('/blog',response_model=List[schemas.showBlog],tags=['Blogs'])
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.showBlog,tags=['Blogs'])
def show(id,response : Response ,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with the id {id} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'details':f'blog with the id {id} not available'}
    return blog