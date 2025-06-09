from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from src.application.task.task_handler import TaskHandler
from src.main import app
import pytest

from src.router.dependencies.dependencies import Dependencies
from test.infrastructure.clients.mock_client import MockTaskClient
from test.infrastructure.repository.task import MockTaskRepository



@pytest.fixture(scope='module')
def mock_task_repository():
    return MockTaskRepository()

@pytest.fixture(scope='module')
def mock_task_client():
    return MockTaskClient(success=True)

@pytest.fixture(scope='module')
def mock_engine():
    return create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

@pytest.fixture(scope='module')
def mock_task_handler(mock_engine, mock_task_repository, mock_task_client):
    return TaskHandler(engine=mock_engine, task_repo=mock_task_repository, task_client=mock_task_client)

async def override_dependency(mock_test_handler):
    return mock_test_handler


app.dependency_overrides[Dependencies.task_handler] = override_dependency
client = TestClient(app)


def test_start_job_should_return_200_status_code(mock_task_repository):
    response = client.post("jobs", data={"job_id":mock_task_repository.some_job_id})
    print(response.json())
    assert response.status_code == 200

def test_start_job_with_wrong_id_should_return_404_status_code(mock_task_repository):
    response = client.post("jobs", data={"job_id":mock_task_repository.not_found})
    assert response.status_code == 404

def test_start_job_with_wrong_id_type_should_return_400_status_code(mock_task_repository):
    response = client.post("jobs", data={"job_id": 123})
    assert response.status_code == 400

def test_stop_job_should_return_200_status_code(mock_task_repository):
    response = client.put("jobs/stop", data={"job_id":mock_task_repository.some_job_id})
    assert response.status_code == 200

def test_stop_job_with_wrong_id_should_return_404_status_code(mock_task_repository):
    response = client.put("jobs/stop", data={"job_id":mock_task_repository.not_found})
    assert response.status_code == 404

def test_stop_job_with_wrong_id_type_should_return_400_status_code(mock_task_repository):
    response = client.put("jobs/stop", data={"job_id":12})
    assert response.status_code == 400