from threading import Thread
import pika
import json
from app.config.setting import setting

connection_parameters = pika.ConnectionParameters(
            host=setting.BROKER_HOST,
            port=setting.BROKER_PORT,
            credentials=pika.PlainCredentials(setting.BROKER_USERNAME, setting.BROKER_PASSWORD)
        )
connection = pika.BlockingConnection(connection_parameters)


class RabbitMQ():
    def __init__(self):
        self.exchange = setting.BROKER_EXCHANGE
        self.routing_key = setting.BROKER_ROUTING_KEY
        self.channel = connection.channel()

    def send(self, message: dict):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=json.dumps(message))
        self.channel.close()