import json
import os
import random

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

sauce_producer = Producer(client_config)
pizza_consumer = Consumer(client_config)
pizza_consumer.subscribe(["pizza"])


def start_service():
    while True:
        msg = pizza_consumer.poll(1.0)
        if msg is None:
            pass
        elif err := msg.error():
            print(f"ERROR! {err}")
            pass
        else:
            pizza = json.loads(msg.value())
            add_sauce(msg.key(), pizza)


def add_sauce(order_id, pizza):
    pizza["sauce"] = calc_sauce()
    sauce_producer.produce("pizza-with-sauce", key=order_id, value=json.dumps(pizza))


def calc_sauce():
    i = random.randint(0, 8)
    sauces = [
        "regular",
        "light",
        "extra",
        "none",
        "alfredo",
        "regular",
        "light",
        "extra",
        "alfredo",
    ]
    return sauces[i]


if __name__ == "__main__":
    start_service()
