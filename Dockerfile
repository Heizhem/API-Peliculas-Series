FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN pip install numpy

RUN pip onstall pandas

COPY ./app /app
