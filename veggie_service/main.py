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


veggies_producer = Producer(client_config)

meats_consumer = Consumer(client_config)
meats_consumer.subscribe(["pizza-with-meats"])


def start_service():
    while True:
        msg = meats_consumer.poll(0.1)
        if msg is None:
            pass
        elif msg.error():
            pass
        else:
            pizza = json.loads(msg.value())
            add_veggies(msg.key(), pizza)


def add_veggies(order_id, pizza):
    pizza["veggies"] = calc_veggies()
    veggies_producer.produce(
        "pizza-with-veggies", key=order_id, value=json.dumps(pizza)
    )


def calc_veggies():
    i = random.randint(0, 4)
    veggies = [
        "tomato",
        "olives",
        "onions",
        "peppers",
        "pineapple",
        "mushrooms",
        "tomato",
        "olives",
        "onions",
        "peppers",
        "pineapple",
        "mushrooms",
    ]
    selection = []
    if i == 0:
        return "none"
    else:
        for n in range(i):
            selection.append(veggies[random.randint(0, 11)])
    return " & ".join(set(selection))


if __name__ == "__main__":
    start_service()
