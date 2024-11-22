from fastapi.testclient import TestClient
from app.main import *
from app.db.data import users
from app.utils.current_time import current_time

client = TestClient(app)

test_user = {
  "user": {
    "account_name": "string",
    "account_number": 10,
    "bank_name": "string",
    "account_type": "string",
    "Id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "username": "string",
    "email": "string",
    "address": {
      "AddressLine": [
        "string"
      ],
      "City": "string",
      "postal_code": "string"
    },
    "password": "string",
    "created_at": {}
  },
  "confirm_password": "string",
  "is_active": True
}

test_new_user = {
    "account_name": "string",
    "account_number": 10,
    "bank_name": "string",
    "account_type": "string"
  }
alee = {"Alee": {
    "username": "Alee",
    "email": "ta@ta.com",
    "password": "mypass",
    "job": "Software Engineer",
    "age": 28,
    "city": "Lagos",
    "salary": 70000,
    "experience": 4,
    "department": "IT",
    "gender": "Male"
  }}

def test_get_users():
    response = client.get("/v1/users", params={})
    assert response.status_code == 200
    assert response.json() == users


def test_create_user():
    response = client.post("/v1/signup", json=test_user)
    assert response.status_code == 201
    assert response.json() == {"message":"Account Created Successfully", "data":test_new_user}


update_user = {
  "username": "new_string",
  "email": "string@email.com",
#   "updated_at": {}
}

def test_update_user():
    response = client.put("/v1/users/Alee", json=update_user)
    assert response.status_code == 201
    assert response.json() == {"message":"Account Updated Successfully", "success":True}

def test_delete_user():
    response = client.delete("/v1/users/Alee")
    assert response.status_code == 204