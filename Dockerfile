FROM python:3.10-slim

COPY app/config /code
WORKDIR /code

CMD uvicorn app.main:app --reload