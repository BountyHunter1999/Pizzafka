import configparser
import os


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        print("value are", value)
        return os.path.expandvars(value)


config = configparser.ConfigParser(interpolation=EnvInterpolation())
with open("pizza_service/config.properties") as f:
    config.read_file(f)
print(config["kafka_client"]["bootstrap.servers"])
