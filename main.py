import json

from fastapi import FastAPI, Response
import hashlib
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()
app.counter = 0
app.patient_id = 1
app.registered = {}


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
    return json.dumps({'message': 'Hello World!'})


@app.get('/method', status_code=200)
def return_method_get():
    return json.dumps({'method': 'GET'})


@app.post('/method', status_code=201)
def return_method_post():
    return json.dumps({'method': 'POST'})


@app.delete('/method', status_code=200)
def return_method_delete():
    return json.dumps({'method': 'DELETE'})


@app.put('/method', status_code=200)
def return_method_put():
    return json.dumps({"method": "PUT"})


@app.options('/method', status_code=200)
def return_method_options():
    return json.dumps({'method': 'OPTIONS'})


@app.get('/auth/')
async def authorize(password: str, password_hash: str, response: Response):
    if hashlib.sha512(bytes(password, encoding='utf-8')).hexdigest() == password_hash:
        response.status_code = 204
    else:
        response.status_code = 401


class PatientRegistration(BaseModel):
    name: str
    surname: str


@app.post('/register/')
async def register_patient(patient: PatientRegistration, response: Response):
    response.status_code = 201
    vaccination_date = (datetime.today() + timedelta(len(patient.name) + len(patient.surname))).strftime('%Y-%m-%d')
    return_val = {
        "id": app.patient_id,
        "name": str(patient.name),
        "surname": str(patient.surname),
        "register_date": str(datetime.today().strftime('%Y-%m-%d')),
        "vaccination_date": str(vaccination_date)
    }
    app.registered[app.patient_id] = return_val
    app.patient_id += 1
    return json.dumps(return_val)


@app.get('/patient/{id}')
async def get_patient_info(id: int, response: Response):
    patient_info = app.registered.get(id, False)
    if not patient_info:
        if id < 1:
            response.status_code = 400
        else:
            response.status_code = 404
    else:
        response.status_code = 200
        return json.dumps(patient_info)







