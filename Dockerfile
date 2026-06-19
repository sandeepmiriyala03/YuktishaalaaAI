<<<<<<< HEAD
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

=======
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

>>>>>>> ff5f1698bc4abbd524308419bb31533fdf2471c4
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]