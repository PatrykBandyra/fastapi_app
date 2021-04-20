from fastapi import FastAPI

app = FastAPI()
app.counter = 0


@app.get('/', status_code=200)
def root():
    return {'message': 'Hello World'}


@app.get('/method')
def return_request_method():
    pass



@app.get('/hello/{name}')
def hello_name_view(name: str):
    return f'Hello {name}'


@app.get('/counter')
def counter():
    app.counter += 1
    return str(app.counter)