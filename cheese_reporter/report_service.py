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
producer_config = dict(config_parser["kafka_client"])
consumer_config = dict(config_parser["kafka_client"])
consumer_config.update(config_parser["consumer"])

cheeses = {}
cheese_topic = "pizza-with-cheese"


def start_consumer():
    cheese_consumer = Consumer(consumer_config)
    cheese_consumer.subscribe([cheese_topic])
    while True:
        event = cheese_consumer.poll(1.0)
        if event is None:
            pass
        elif event.error():
            print(f"ERROR - {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_cheese_count(pizza["cheese"])


def add_cheese_count(cheese):
    if cheese in cheeses:
        cheeses[cheese] = cheeses[cheese] + 1
    else:
        cheeses[cheese] = 1


def generate_report():
    return json.dumps(cheeses, indent=4)
