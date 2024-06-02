import json
from datetime import datetime, timedelta

import pika
import pytest
from testcontainers.rabbitmq import RabbitMqContainer

from app.config.setting import setting
from app.domain.zone import zone_service as service
from app.domain.zone.event import PersonTrackingEvent, Action
from app.infrastructure import broker


class TestRabbitMQ:
    @pytest.fixture(scope="class")
    def rabbit(self):
        rabbit = RabbitMqContainer("rabbitmq:latest")
        rabbit.start()
        yield rabbit
        rabbit.stop()

    def test_publish_and_consume(self, rabbit):
        connection_params = pika.ConnectionParameters(host=rabbit.get_container_host_ip(),
                                                      port=rabbit.get_exposed_port(5672),
                                                      credentials=pika.PlainCredentials("guest", "guest"))

        broker.connection_parameters = connection_params

        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        channel.exchange_declare(exchange=setting.BROKER_EXCHANGE, exchange_type='direct', durable=True)
        queue_name = 'test_queue'
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=setting.BROKER_EXCHANGE, queue=queue_name,
                           routing_key=setting.BROKER_ROUTING_KEY_TRACKING)

        setting.PERSON_UUIDS = {"joao": "fecaa5bf-d219-4462-b528-3bf2ccae65b4"}

        date_a = datetime.today() - timedelta(hours=1)
        date_b = datetime.today()

        event_a = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date_a)
        event_b = PersonTrackingEvent(Action.WENT_OUT, 'house', 'joao', date_b)

        service.launch_event(event_a)
        service.launch_event(event_b)

        # Assert event a
        _, _, body = channel.basic_get(queue=queue_name, auto_ack=True)
        result = json.loads(body.decode('utf-8'))

        assert 'PERSON_TRACKING' == result['type']
        assert 'fecaa5bf-d219-4462-b528-3bf2ccae65b4' == result['person_id']
        assert service._transform_date(date_a) == result['datetime']
        assert 'CAME_IN' == result['action']
        assert 'house' == result['local']
        assert 'Home assistant' == result['origin']

        # Assert event b
        _, _, body = channel.basic_get(queue=queue_name, auto_ack=True)
        result = json.loads(body.decode('utf-8'))

        assert 'PERSON_TRACKING' == result['type']
        assert 'fecaa5bf-d219-4462-b528-3bf2ccae65b4' == result['person_id']
        assert service._transform_date(date_b) == result['datetime']
        assert 'WENT_OUT' == result['action']
        assert 'house' == result['local']
        assert 'Home assistant' == result['origin']

        # Assert event REMAINED
        _, _, body = channel.basic_get(queue=queue_name, auto_ack=True)
        result = json.loads(body.decode('utf-8'))

        assert 'PERSON_TRACKING' == result['type']
        assert 'fecaa5bf-d219-4462-b528-3bf2ccae65b4' == result['person_id']
        assert service._transform_date(date_a) == result['datetime']
        assert 'REMAINED' == result['action']
        assert 'house' == result['local']
        assert 60 == result['minutes']
        assert 'Home assistant' == result['origin']

        connection.close()
