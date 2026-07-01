import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_con_nombre(client):
    response = client.get('/hello?name=Vicente')
    assert response.status_code == 200
    assert b'Vicente' in response.data

def test_hello_sin_nombre(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert b'mundo' in response.data

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
