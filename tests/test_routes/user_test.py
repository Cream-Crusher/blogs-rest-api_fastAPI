import uuid

from fastapi.testclient import TestClient
from fastapi import status

from application.main import app

client = TestClient(app)

user_id = str(uuid.uuid4())


def test_root():
    response = client.get('/api/healthchecker')
    assert response.status_code == 200
    assert response.json() == {'message': 'The API is LIVE!!'}


def test_read_main():
    response = client.get(f"/users")
    response_json = response.json()[0]

    assert response.status_code == 200
    assert response_json['username'] == 'test_user'
    assert response_json['email'] == 'test_email'


# def test_create_user():
#     user = {
#         "username": "test_user",
#         "email": "test@example.com",
#         "password": "test_password"
#     }
#     response = client.post('/user', json=user)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json() == user
