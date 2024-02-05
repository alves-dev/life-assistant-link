FROM python:3.12-slim

COPY . /code
WORKDIR /code

# Set the timezone
ENV TZ=America/Sao_Paulo

# Update the package list and install any dependencies
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get clean

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 3001

CMD gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:3001