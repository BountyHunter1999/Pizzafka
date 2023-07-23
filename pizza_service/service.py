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

# config_parser.read("config.properties")

check_parser_value(config_parser)

print(config_parser.get("kafka_client", "sasl.username", vars=os.environ))
producer_config = dict(config_parser["kafka_client"])
consumer_config = dict(config_parser["kafka_client"])
consumer_config.update(config_parser["consumer"])

pizza_producer = Producer(producer_config)
print(config_parser)
