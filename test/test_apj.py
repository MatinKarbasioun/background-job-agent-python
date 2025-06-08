from fastapi.testclient import TestClient
from src.main import app
import pytest


@pytest.fixture(scope='module')
def client():
    return TestClient(app)

@pytest.fixture(scope='module')
def preload_data():
    pass

@pytest.fixture()
def job_id():
    job_id = 'test'
    return job_id

def test_start_job_should_return_200_status_code(client, job_id):
    response = client.put("job/start", data={"job_id":job_id})
    assert response.status_code == 200

def test_start_job_with_wrong_id_should_return_404_status_code(client, job_id):
    response = client.put("job/start", data={"job_id":job_id})
    assert response.status_code == 404

def test_start_job_with_wrong_id_type_should_return_400_status_code(client, job_id):
    response = client.put("job/start", data={"job_id":job_id})
    assert response.status_code == 404

def test_stop_job_should_return_200_status_code(client, job_id):
    response = client.put("job/start", data={"job_id":job_id})
    assert response.status_code == 200

def test_stop_job_with_wrong_id_should_return_404_status_code(client, job_id):
    response = client.put("job/start", data={"job_id":job_id})
    assert response.status_code == 404

def test_stop_job_with_wrong_id_type_should_return_400_status_code(client, job_id):
    response = client.put("job/start", data={"job_id":job_id})
    assert response.status_code == 400