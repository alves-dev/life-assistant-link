from threading import Thread
import pika
import json
from app.config.setting import setting

class RabbitMQ():
    def __init__(self, host=setting.BROKER_HOST, port=setting.BROKER_PORT, username=setting.BROKER_USERNAME,
                 password=setting.BROKER_PASSWORD, exchange=setting.BROKER_EXCHANGE, routing_key=setting.BROKER_ROUTING_KEY):
        self.host = host
        self.port = port
        self.exchange = exchange
        self.credentials = pika.PlainCredentials(username, password)
        self.routing_key = routing_key

    def send(self, message: dict):
        connection_parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials
        )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=json.dumps(message))
        connection.close()