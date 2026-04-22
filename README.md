# Smart Task API

A task management REST API built with FastAPI, SQLAlchemy, and SQLite.

## Setup

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the app

```bash
uvicorn app.main:app --reload
```

API docs available at http://localhost:8000/docs

## Running tests

```bash
pytest tests/ -v
```

## Database migrations (Alembic)

**First time setup** (already done):
```bash
alembic upgrade head
```

**After changing a model** (e.g. added a column):
```bash
alembic revision --autogenerate -m "describe what you changed"
alembic upgrade head
```

**Roll back the last migration:**
```bash
alembic downgrade -1
```

**Check current database version:**
```bash
alembic current
```

**View migration history:**
```bash
alembic history
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/signup | No | Register a new user |
| POST | /auth/login | No | Login and get JWT token |
| GET | /tasks/ | Yes | List your tasks (paginated) |
| POST | /tasks/ | Yes | Create a task |
| GET | /tasks/{id} | Yes | Get a task |
| PUT | /tasks/{id} | Yes | Update a task |
| DELETE | /tasks/{id} | Yes | Delete a task |
| PATCH | /tasks/{id}/complete | Yes | Mark task as complete |
| GET | /reports/tasks | Yes | Generate task report |
| GET | /joke/random | No | Get a random joke |
