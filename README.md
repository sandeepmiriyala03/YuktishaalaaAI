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

## Endpoint Samples

Route-by-route JSON request examples are in `tests/samples/`:

- `tests/samples/app/route.json`: root, docs, favicon, service worker, and static manifest.
- `tests/samples/department/route.json`: department list/create/get/update/delete.
- `tests/samples/employee/route.json`: employee list, stored-procedure route, and CRUD.
- `tests/samples/users/route.json`: legacy SQLite user CRUD.
- `tests/samples/products/route.json`: PostgreSQL product CRUD.
- `tests/samples/test/route.json`: PostgreSQL test-record create/list/get.
- `tests/samples/auth/route.json`: JWT registration, login, and protected current-user route.

Each `route.json` contains the HTTP method, path, expected status, and `request_body` when the endpoint accepts one. `description` and `note` fields explain usage; they are used instead of comments because JSON does not allow comment syntax. Replace path IDs with IDs returned by create/list requests. For bearer-authenticated requests, register and log in first, then use the returned `access_token` in the `Authorization: Bearer <token>` header. Samples are references and are not automatically executed. Use test data only; the legacy SQLite user API stores its password as plain text.

For interactive requests, start the app and open `http://localhost:8000/docs`.
