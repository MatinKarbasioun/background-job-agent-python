import pytest


@pytest.fixture
def mock_successful_task_response(task_id: int):
    yield {
        "status_code": 200,
        "task_id": task_id,
        "is_success":True,
        "error": None
    }


@pytest.fixture
def mock_unsuccessful_task_response(task_id: int):
    yield {
        "status_code": 500,
        "task_id": task_id,
        "is_success":False,
        "error": None
    }