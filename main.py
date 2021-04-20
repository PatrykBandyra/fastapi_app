from fastapi import FastAPI, Response
from starlette.requests import Request
import hashlib

app = FastAPI()
app.counter = 0


"""----------------------------------------------------Course--------------------------------------------------------"""


@app.get('/hello/{name}')
def hello_name_view(name: str):
    return f'Hello {name}'


@app.get('/counter')
def counter():
    app.counter += 1
    return str(app.counter)


"""----------------------------------------------------Homework------------------------------------------------------"""


@app.get('/', status_code=200)
def root():
    return {'message': 'Hello World'}


@app.get('/method', status_code=200)
def return_method_get():
    return {'method': 'GET'}


@app.post('/method', status_code=201)
def return_method_post():
    return {'method': 'POST'}


@app.delete('/method', status_code=200)
def return_method_delete():
    return {'method': 'DELETE'}


@app.put('/method', status_code=200)
def return_method_put():
    return {"method": "PUT"}


@app.options('/method', status_code=200)
def return_method_options():
    return {'method': 'OPTIONS'}


@app.get('/auth/')
async def authorize(password: str, password_hash: str, response: Response):
    if hashlib.sha512(bytes(password, encoding='utf-8')).hexdigest() == password_hash:
        response.status_code = 204
    else:
        response.status_code = 401






