# YuktishaalaaAI FastAPI CRUD API

## Setup

Create a root `.env` file for the local app and PostgreSQL-backed endpoints:

```env
DATABASE_URL=sqlite:///./yuktishaalaa.db
FASTAPI_DATABASE_URL=postgresql+psycopg2://user:password@host/database
JWT_SECRET_KEY=replace-with-a-random-secret-at-least-32-characters-long
```

`DATABASE_URL` defaults to the local SQLite database. Products, test records, and JWT users use `FASTAPI_DATABASE_URL`. Generate a private JWT signing key locally and keep it out of source control. JWT login is available at `POST /auth/users/login`; protected user details are available at `GET /auth/users/me`.

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
- Products: `/products`
- Test records: `/test`
- JWT user registration/login: `/auth/users`

Each resource supports create, list, get-by-id, update, and delete operations.
