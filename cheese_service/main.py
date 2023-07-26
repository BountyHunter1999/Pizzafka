import json
import os
import random

# from pizza import Pizza, PizzaOrder
from configparser import ConfigParser, BasicInterpolation
from confluent_kafka import Producer, Consumer


class EnvInterpolation(BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


config_parser = ConfigParser(interpolation=EnvInterpolation())
with open("pizza_service/config.properties", "r") as conf:
    config_parser.read_file(conf)

client_config = dict(config_parser["kafka_client"])
cheese_producer = Producer(client_config)

sauce_consumer = Consumer(client_config)
sauce_consumer.subscribe(['pizza-with-sauce'])


def start_service():
    while True:
        msg = sauce_consumer.poll(0.1)
        if msg is None:
            pass
        elif msg.error():
            pass
        else:
            pizza = json.loads(msg.value())
            add_cheese(msg.key(), pizza)


def add_cheese(order_id, pizza):
    pizza['cheese'] = calc_cheese()
    cheese_producer.produce('pizza-with-cheese', key=order_id, value=json.dumps(pizza))


def calc_cheese():
    i = random.randint(0, 6)
    cheeses = ['extra', 'none', 'three cheese', 'goat cheese', 'extra', 'three cheese', 'goat cheese']
    return cheeses[i]


if __name__ == '__main__':
    start_service()