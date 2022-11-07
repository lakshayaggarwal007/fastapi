from fastapi import FastAPI


app  = FastAPI()


@app.get('/')
def index():
    return {'data':'sadad'}

@app.get('/about/{id}')
def about(id:int):
    return {'data':id}