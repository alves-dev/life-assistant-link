FROM python:3.12-slim

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 3001

CMD gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:3001