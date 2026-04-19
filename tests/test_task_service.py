# tests/test_task_service.py

import pytest
from app.services.task_service import (
    create_task_logic,
    get_all_tasks_logic,
    get_task_by_id_logic,
    update_task_logic,
    delete_task_logic,
    mark_complete_logic,
)
from app.schemas.task import TaskCreate
from app.models.task import Task


# ============ HELPER: Create a test user ID ============
TEST_USER_ID = 999  # Use a user ID that doesn't conflict with real data


# ============ CREATE TASK TESTS ============

def test_create_task_success(db_session):
    """Should create a task successfully"""
    # ARRANGE
    task_data = TaskCreate(title="Test Task", completed=False)
    
    # ACT
    result = create_task_logic(task_data, TEST_USER_ID)
    
    # ASSERT
    assert result is not None
    assert result.title == "Test Task"
    assert result.completed == False
    assert result.user_id == TEST_USER_ID
    assert result.id is not None


def test_create_task_with_completed_true(db_session):
    """Should create a task that is already completed"""
    # ARRANGE
    task_data = TaskCreate(title="Completed Task", completed=True)
    
    # ACT
    result = create_task_logic(task_data, TEST_USER_ID)
    
    # ASSERT
    assert result.completed == True


# ============ UPDATE TASK TESTS (BUSINESS RULES) ============

def test_update_task_success(db_session):
    """Should update a valid incomplete task"""
    # ARRANGE - First create a task
    task_data = TaskCreate(title="Original Title", completed=False)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT - Update the task
    updated_data = TaskCreate(title="New Title", completed=True)
    result = update_task_logic(task.id, updated_data, TEST_USER_ID)
    
    # ASSERT
    assert result is not None
    assert result.title == "New Title"
    assert result.completed == True
    assert result.id == task.id


def test_cannot_update_completed_task(db_session):
    """BUSINESS RULE: Cannot update a completed task"""
    # ARRANGE - Create and complete a task
    task_data = TaskCreate(title="Done Task", completed=True)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT - Try to update the completed task
    updated_data = TaskCreate(title="Try to Change", completed=False)
    result = update_task_logic(task.id, updated_data, TEST_USER_ID)
    
    # ASSERT - Should return error, not the task
    assert result == {"error": "completed_task_cannot_be_updated"}


def test_cannot_update_task_with_empty_title(db_session):
    """BUSINESS RULE: Title cannot be empty"""
    # ARRANGE - Create a task
    task_data = TaskCreate(title="Valid Title", completed=False)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT - Try to update with empty title
    updated_data = TaskCreate(title="", completed=False)
    result = update_task_logic(task.id, updated_data, TEST_USER_ID)
    
    # ASSERT
    assert result == {"error": "title_cannot_be_empty"}


def test_cannot_update_task_with_only_spaces(db_session):
    """BUSINESS RULE: Title with only spaces is invalid"""
    # ARRANGE
    task_data = TaskCreate(title="Valid Title", completed=False)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT - Try to update with spaces only
    updated_data = TaskCreate(title="   ", completed=False)
    result = update_task_logic(task.id, updated_data, TEST_USER_ID)
    
    # ASSERT
    assert result == {"error": "title_cannot_be_empty"}


def test_update_nonexistent_task(db_session):
    """Should return None when task doesn't exist"""
    # ACT - Try to update a task that doesn't exist
    updated_data = TaskCreate(title="New", completed=False)
    result = update_task_logic(99999, updated_data, TEST_USER_ID)
    
    # ASSERT
    assert result is None


# ============ MARK COMPLETE TESTS ============

def test_mark_complete_success(db_session):
    """Should mark an incomplete task as complete"""
    # ARRANGE - Create incomplete task
    task_data = TaskCreate(title="To Complete", completed=False)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT
    result = mark_complete_logic(task.id, TEST_USER_ID)
    
    # ASSERT
    assert result is not None
    assert result.completed == True
    assert result.title == "To Complete"


def test_cannot_mark_already_completed_task(db_session):
    """BUSINESS RULE: Cannot mark an already completed task"""
    # ARRANGE - Create completed task
    task_data = TaskCreate(title="Already Done", completed=True)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT
    result = mark_complete_logic(task.id, TEST_USER_ID)
    
    # ASSERT
    assert result == {"error": "task_already_completed"}


def test_mark_complete_nonexistent_task(db_session):
    """Should return None when task doesn't exist"""
    # ACT
    result = mark_complete_logic(99999, TEST_USER_ID)
    
    # ASSERT
    assert result is None


# ============ DELETE TASK TESTS ============

def test_delete_task_success(db_session):
    """Should delete an existing task"""
    # ARRANGE - Create a task
    task_data = TaskCreate(title="To Delete", completed=False)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT
    result = delete_task_logic(task.id, TEST_USER_ID)
    
    # ASSERT
    assert result == True
    
    # Verify task is gone
    deleted_task = get_task_by_id_logic(task.id, TEST_USER_ID)
    assert deleted_task is None


def test_delete_nonexistent_task(db_session):
    """Should return False when task doesn't exist"""
    # ACT
    result = delete_task_logic(99999, TEST_USER_ID)
    
    # ASSERT
    assert result == False


# ============ GET TASKS TESTS ============

def test_get_all_tasks_returns_user_tasks_only(db_session):
    """Should only return tasks belonging to the user"""
    # ARRANGE - Create tasks for different users
    task_data = TaskCreate(title="User 999 Task", completed=False)
    create_task_logic(task_data, TEST_USER_ID)
    
    task_data2 = TaskCreate(title="User 888 Task", completed=False)
    create_task_logic(task_data2, 888)  # Different user
    
    # ACT - Get tasks for TEST_USER_ID
    tasks = get_all_tasks_logic(TEST_USER_ID, page=1, limit=10)
    
    # ASSERT
    assert len(tasks) >= 1
    for task in tasks:
        assert task.user_id == TEST_USER_ID


def test_get_all_tasks_pagination(db_session):
    """Should respect page and limit parameters"""
    # ARRANGE - Create 5 tasks
    for i in range(5):
        task_data = TaskCreate(title=f"Task {i}", completed=False)
        create_task_logic(task_data, TEST_USER_ID)
    
    # ACT - Get first page with limit 2
    tasks_page_1 = get_all_tasks_logic(TEST_USER_ID, page=1, limit=2)
    
    # ASSERT
    assert len(tasks_page_1) <= 2


def test_get_task_by_id_success(db_session):
    """Should return the correct task by ID"""
    # ARRANGE
    task_data = TaskCreate(title="Find Me", completed=False)
    created = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT
    found = get_task_by_id_logic(created.id, TEST_USER_ID)
    
    # ASSERT
    assert found is not None
    assert found.id == created.id
    assert found.title == "Find Me"


def test_get_task_by_id_wrong_user(db_session):
    """Should NOT return task if user_id doesn't match"""
    # ARRANGE - Create task for TEST_USER_ID
    task_data = TaskCreate(title="Secret Task", completed=False)
    task = create_task_logic(task_data, TEST_USER_ID)
    
    # ACT - Try to get with different user
    found = get_task_by_id_logic(task.id, 888)  # Different user
    
    # ASSERT
    assert found is None