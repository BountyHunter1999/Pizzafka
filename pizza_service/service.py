import json
import os

# from pizza import Pizza, PizzaOrder
from configparser import ConfigParser, BasicInterpolation
from confluent_kafka import Producer, Consumer


# %(home) will be returned as it is w/o substituting the home value
# config_parser = ConfigParser(interpolation=None)


class EnvInterpolation(BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


config_parser = ConfigParser(interpolation=EnvInterpolation())


def check_parser_value(config_parser: ConfigParser):
    # Create a dictionary to store all the values
    all_values = {}

    # Get all sections in the configuration file
    sections = config_parser.sections()

    # Loop through each section and get the key-value pairs
    for section in sections:
        all_values[section] = {}
        for key, value in config_parser.items(section):
            all_values[section][key] = value

    print(all_values)


with open("pizza_service/config.properties", "r") as conf:
    config_parser.read_file(conf)

# check_parser_value(config_parser)

producer_config = dict(config_parser["kafka_client"])
consumer_config = dict(config_parser["kafka_client"])
consumer_config.update(config_parser["consumer"])

pizza_producer = Producer(producer_config)

pizza_warmer = {}


def order_pizzas(count):
    order = PizzaOrder(count)
    # stasb tbe order, while they are in process
    pizza_warmer[order.id] = order
    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        pizza_producer.produce("pizza", key=order.id, value=new_pizza.toJSON())
    # make sure all the pizzas events have been sent
    pizza_producer.flush()
    return order.id

def get_order(order_id):
    order = pizza_warmer[order_id]
    if order == None:
        return "Order not found, perhaps it's not ready yet."
    else:
        return order.toJSON()