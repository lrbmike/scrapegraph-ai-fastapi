FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--port", "80"]