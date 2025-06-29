# Vanniyar Manamalai Backend

This is the backend application for the Vanniyar Manamalai Matrimony platform. It is built using FastAPI, SQLAlchemy, and uses a SQL database via pyodbc.

## Features
- RESTful API for matrimony operations
- Database integration with SQLAlchemy
- FastAPI for high-performance web APIs

## Setup Instructions

1. **Install dependencies:**
   ```sh
   pip install fastapi uvicorn sqlalchemy pyodbc
   ```

2. **Run the application:**
   ```sh
   uvicorn app.main:app --reload
   .\venv\Scripts\uvicorn app.main:app --reload
   ```

3. **Access the API:**
   - The API will be available at: http://127.0.0.1:8000
   - Interactive API docs: http://127.0.0.1:8000/docs

## Output
- All API responses and logs will be shown in the terminal where you run the `uvicorn` command.
- You can interact with the API using the Swagger UI at `/docs`.
