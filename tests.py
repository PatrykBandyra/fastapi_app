import json
import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta

client = TestClient(app)


"""----------------------------------------------------Course--------------------------------------------------------"""





def test_hello_name():
    name = 'Kamila'
    response = client.get(f'/hello/{name}')
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'


def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == '"1"'
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == '"2"'


"""----------------------------------------------------Homework------------------------------------------------------"""


def test_get_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == json.dumps({'message': 'Hello World!'})


def test_get_method():
    response = client.get(f'/method')
    assert response.status_code == 200
    assert response.json() == json.dumps({'method': 'GET'})


def test_put_method():
    response = client.put(f'/method')
    assert response.status_code == 200
    assert response.json() == json.dumps({'method': 'PUT'})


def test_options_method():
    response = client.options(f'/method')
    assert response.status_code == 200
    assert response.json() == json.dumps({'method': 'OPTIONS'})


def test_delete_method():
    response = client.delete(f'/method')
    assert response.status_code == 200
    assert response.json() == json.dumps({'method': 'DELETE'})


def test_post_method():
    response = client.post(f'/method')
    assert response.status_code == 201
    assert response.json() == json.dumps({'method': 'POST'})


def test_authorize_good():
    response = client.get(f'/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215')
    assert response.status_code == 204


def test_authorize_bad():
    response = client.get(f'/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091')
    assert response.status_code == 401


def test_register_patient():
    id = 1
    name = 'Jan'
    surname = 'Kowalski'
    response = client.post(f'/register/', json={'name': name, 'surname': surname})
    assert response.status_code == 201

    today = datetime.today()
    correct_response_json = json.dumps({
        "id": id,
        "name": name,
        "surname": surname,
        "register_date": str(today.strftime('%Y-%m-%d')),
        "vaccination_date": str((today + timedelta(len(name)+len(surname))).strftime('%Y-%m-%d'))
    })
    assert response.json() == correct_response_json


def test_register_patient2():
    id = 2
    name = 'Janko'
    surname = 'Muzykant'
    response = client.post(f'/register/', json={'name': name, 'surname': surname})
    assert response.status_code == 201

    today = datetime.today()
    correct_response_json = json.dumps({
        "id": id,
        "name": name,
        "surname": surname,
        "register_date": str(today.strftime('%Y-%m-%d')),
        "vaccination_date": str((today + timedelta(len(name)+len(surname))).strftime('%Y-%m-%d'))
    })
    assert response.json() == correct_response_json


def test_patient_by_id_exists():
    id = 1
    name = 'Jan'
    surname = 'Kowalski'
    response = client.get(f'/patient/{id}')
    assert response.status_code == 200

    today = datetime.today()
    correct_response_json = json.dumps({
        "id": id,
        "name": name,
        "surname": surname,
        "register_date": str(today.strftime('%Y-%m-%d')),
        "vaccination_date": str((today + timedelta(len(name) + len(surname))).strftime('%Y-%m-%d'))
    })
    assert response.json() == correct_response_json


def test_patient_by_id_exists2():
    id = 2
    name = 'Janko'
    surname = 'Muzykant'
    response = client.get(f'/patient/{id}')
    assert response.status_code == 200

    today = datetime.today()
    correct_response_json = json.dumps({
        "id": id,
        "name": name,
        "surname": surname,
        "register_date": str(today.strftime('%Y-%m-%d')),
        "vaccination_date": str((today + timedelta(len(name) + len(surname))).strftime('%Y-%m-%d'))
    })
    assert response.json() == correct_response_json


def test_patient_by_id_wrong():
    id = 33
    response = client.get(f'/patient/{id}')
    assert response.status_code == 404


def test_patient_by_id_wrong2():
    id = -2
    response = client.get(f'/patient/{id}')
    assert response.status_code == 400
