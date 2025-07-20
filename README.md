# PGA Backend

This is a small FastAPI application for parking garage availability. It exposes a handful of API endpoints and HTML dashboards. The project can be run locally with SQLite or against a database provided via `DATABASE_URL`.

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the database connection. By default the application expects a `DATABASE_URL` environment variable. For quick local testing you can instead set:

```bash
export USE_SQLITE=true
```

This will create a local SQLite file `test.db` in the project directory.
If you don't set `DATABASE_URL`, the application defaults to the production
database used by the hosted instance. To override it, export your own
connection string:
```bash
export DATABASE_URL="postgresql://pgabackend_user:SD9jd5JEZPLt16kZIswcunk2MTCME5Qn@dpg-d188l0ogjchc73dtbti0-a.oregon-postgres.render.com/pgabackend"
```

## Running the server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The dashboard is available at `http://localhost:8000/dashboard` once data has been loaded.

## Resetting the database

A helper script `reset_db.py` is included to drop all tables and recreate them. **Use this with caution** as it removes all existing data.

```bash
python3 reset_db.py
```

The script uses the same database configuration as the application (`DATABASE_URL` or `USE_SQLITE`). After running, a fresh set of tables will be created based on the models defined in `models.py`.


