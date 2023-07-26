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
meats_producer = Producer(client_config)

cheese_consumer = Consumer(client_config)
cheese_consumer.subscribe(["pizza-with-cheese"])


def start_service():
    while True:
        msg = cheese_consumer.poll(0.1)
        if msg is None:
            pass
        elif msg.error():
            pass
        else:
            pizza = json.loads(msg.value())
            add_meats(msg.key(), pizza)


def add_meats(order_id, pizza):
    pizza["meats"] = calc_meats()
    meats_producer.produce("pizza-with-meats", key=order_id, value=json.dumps(pizza))


def calc_meats():
    i = random.randint(0, 4)
    meats = [
        "pepperoni",
        "sausage",
        "ham",
        "anchovies",
        "salami",
        "bacon",
        "pepperoni",
        "sausage",
        "ham",
        "anchovies",
        "salami",
        "bacon",
    ]
    selection = []
    if i == 0:
        return "none"
    else:
        for _ in range(i):
            selection.append(meats[random.randint(0, 11)])
    return " & ".join(set(selection))


if __name__ == "__main__":
    start_service()
