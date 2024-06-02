import json

import pika

from app.config.setting import setting

connection_parameters = pika.ConnectionParameters(
    host=setting.BROKER_HOST,
    port=setting.BROKER_PORT,
    credentials=pika.PlainCredentials(setting.BROKER_USERNAME, setting.BROKER_PASSWORD)
)


class RabbitMQ:
    def __init__(self):
        self.exchange = setting.BROKER_EXCHANGE
        self.routing_key_tracking = setting.BROKER_ROUTING_KEY_TRACKING
        self.routing_key_food = setting.BROKER_ROUTING_KEY_FOOD
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

    def send_tracking(self, message: dict):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key_tracking,
                                   body=json.dumps(message))
        self.channel.close()

    def send_food(self, message: dict):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key_food, body=json.dumps(message))
        self.channel.close()
