FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
COPY ./app /app