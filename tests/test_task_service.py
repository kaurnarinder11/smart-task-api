import pytest
from fastapi import HTTPException
from app.services.task_service import (
    create_task_logic,
    get_all_tasks_logic,
    get_task_by_id_logic,
    update_task_logic,
    delete_task_logic,
    mark_complete_logic,
)
from app.schemas.task import TaskCreate, TaskUpdate

TEST_USER_ID = 999


# ============ CREATE TASK TESTS ============

def test_create_task_success(db_session):
    task_data = TaskCreate(title="Test Task", completed=False)
    result = create_task_logic(task_data, TEST_USER_ID, db_session)
    assert result.title == "Test Task"
    assert result.completed == False
    assert result.user_id == TEST_USER_ID
    assert result.id is not None


def test_create_task_with_completed_true(db_session):
    task_data = TaskCreate(title="Completed Task", completed=True)
    result = create_task_logic(task_data, TEST_USER_ID, db_session)
    assert result.completed == True


# ============ UPDATE TASK TESTS ============

def test_update_task_success(db_session):
    task = create_task_logic(TaskCreate(title="Original Title", completed=False), TEST_USER_ID, db_session)
    result = update_task_logic(task.id, TaskUpdate(title="New Title", completed=True), TEST_USER_ID, db_session)
    assert result.title == "New Title"
    assert result.completed == True


def test_cannot_update_completed_task(db_session):
    task = create_task_logic(TaskCreate(title="Done Task", completed=True), TEST_USER_ID, db_session)
    with pytest.raises(HTTPException) as exc_info:
        update_task_logic(task.id, TaskUpdate(title="Try to Change", completed=False), TEST_USER_ID, db_session)
    assert exc_info.value.status_code == 400


def test_cannot_update_task_with_empty_title(db_session):
    with pytest.raises(Exception):
        TaskUpdate(title="")  # Pydantic rejects min_length=1 violation


def test_update_nonexistent_task(db_session):
    with pytest.raises(HTTPException) as exc_info:
        update_task_logic(99999, TaskUpdate(title="New"), TEST_USER_ID, db_session)
    assert exc_info.value.status_code == 404


# ============ MARK COMPLETE TESTS ============

def test_mark_complete_success(db_session):
    task = create_task_logic(TaskCreate(title="To Complete", completed=False), TEST_USER_ID, db_session)
    result = mark_complete_logic(task.id, TEST_USER_ID, db_session)
    assert result.completed == True


def test_cannot_mark_already_completed_task(db_session):
    task = create_task_logic(TaskCreate(title="Already Done", completed=True), TEST_USER_ID, db_session)
    with pytest.raises(HTTPException) as exc_info:
        mark_complete_logic(task.id, TEST_USER_ID, db_session)
    assert exc_info.value.status_code == 400


def test_mark_complete_nonexistent_task(db_session):
    with pytest.raises(HTTPException) as exc_info:
        mark_complete_logic(99999, TEST_USER_ID, db_session)
    assert exc_info.value.status_code == 404


# ============ DELETE TASK TESTS ============

def test_delete_task_success(db_session):
    task = create_task_logic(TaskCreate(title="To Delete", completed=False), TEST_USER_ID, db_session)
    result = delete_task_logic(task.id, TEST_USER_ID, db_session)
    assert result == {"message": "Task deleted successfully"}

    with pytest.raises(HTTPException) as exc_info:
        get_task_by_id_logic(task.id, TEST_USER_ID, db_session)
    assert exc_info.value.status_code == 404


def test_delete_nonexistent_task(db_session):
    with pytest.raises(HTTPException) as exc_info:
        delete_task_logic(99999, TEST_USER_ID, db_session)
    assert exc_info.value.status_code == 404


# ============ GET TASKS TESTS ============

def test_get_all_tasks_returns_user_tasks_only(db_session):
    create_task_logic(TaskCreate(title="User 999 Task", completed=False), TEST_USER_ID, db_session)
    create_task_logic(TaskCreate(title="User 888 Task", completed=False), 888, db_session)

    result = get_all_tasks_logic(TEST_USER_ID, db_session, page=1, limit=10)
    for task in result["tasks"]:
        assert task.user_id == TEST_USER_ID


def test_get_all_tasks_pagination(db_session):
    for i in range(5):
        create_task_logic(TaskCreate(title=f"Pagination Task {i}", completed=False), TEST_USER_ID, db_session)

    result = get_all_tasks_logic(TEST_USER_ID, db_session, page=1, limit=2)
    assert len(result["tasks"]) <= 2
    assert result["limit"] == 2
    assert "total" in result
    assert "pages" in result


def test_get_task_by_id_success(db_session):
    created = create_task_logic(TaskCreate(title="Find Me", completed=False), TEST_USER_ID, db_session)
    found = get_task_by_id_logic(created.id, TEST_USER_ID, db_session)
    assert found.id == created.id
    assert found.title == "Find Me"


def test_get_task_by_id_wrong_user(db_session):
    task = create_task_logic(TaskCreate(title="Secret Task", completed=False), TEST_USER_ID, db_session)
    with pytest.raises(HTTPException) as exc_info:
        get_task_by_id_logic(task.id, 888, db_session)
    assert exc_info.value.status_code == 404
