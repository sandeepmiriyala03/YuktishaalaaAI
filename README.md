# YuktishaalaaAI FastAPI CRUD API

## Setup

Create a `.env` file with the database connection string before running CRUD requests:

```env
DATABASE_URL=postgresql+psycopg2://user:password@host/database?sslmode=require
```

Install dependencies and start the API:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open `http://localhost:8000/docs` for the interactive CRUD API.

## Resources

- Employees: `/employee`
- Departments: `/department`
- Users: `/users`

Each resource supports create, list, get-by-id, update, and delete operations.
