FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para ejecutar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]