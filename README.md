[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen.svg)](https://pytest.org)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success.svg)](https://smart-task-api-b89q.onrender.com/docs)

# 📋 Smart Task API

A **production-ready** Task Management REST API built with FastAPI, SQLAlchemy, JWT authentication, Docker, and Alembic migrations.

## ✨ Features

- 🔐 **JWT Authentication** - Signup, login, protected routes
- 📝 **Full CRUD Operations** - Create, read, update, delete tasks
- ✅ **Task Completion** - Mark tasks as complete/incomplete
- 📊 **Reports** - Generate task analytics
- 🎲 **External API Integration** - Random joke endpoint
- 🐳 **Docker Support** - Containerized for easy deployment
- 🗄️ **Database Migrations** - Alembic for schema version control
- 🧪 **Unit Tests** - Pytest with coverage
- 🛡️ **Global Error Handling** - Production-grade error responses
- ☁️ **Cloud-Ready** - Storage abstraction pattern

## 🚀 Live Demo

**API Documentation (Swagger UI):** [https://smart-task-api-b89q.onrender.com/docs](https://smart-task-api-b89q.onrender.com/docs)

Click the link above to test all endpoints live!

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Framework | FastAPI |
| Database | SQLite with SQLAlchemy ORM |
| Auth | JWT (python-jose, passlib) |
| Migrations | Alembic |
| Testing | Pytest |
| Container | Docker |
| Deployment | Render.com |

## 📦 Local Setup

### Option 1: Standard Python

```bash
# Clone the repo
git clone https://github.com/kaurnarinder11/smart-task-api.git
cd smart-task-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
