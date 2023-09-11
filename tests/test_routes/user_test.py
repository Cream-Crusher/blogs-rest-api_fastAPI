import uuid

from fastapi.testclient import TestClient

from application.main import app

client = TestClient(app)

user_id = str(uuid.uuid4())


def test_read_main():
    response = client.get(f"/users")
    response_json = response.json()[0]

    assert response.status_code == 200
    assert response_json['username'] == 'test_user'
    assert response_json['email'] == 'test_email'
