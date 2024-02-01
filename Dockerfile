FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app/config /code
WORKDIR /code

#CMD uvicorn app.main:app --reload
CMD gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:3001 -e TIMEOUT="300"