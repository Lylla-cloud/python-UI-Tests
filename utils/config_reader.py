import yaml
import os

class ConfigReader:
    _config = None

    @classmethod
    def get_config(cls):
        if cls._config is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config.yaml"
            )
            with open(config_path, "r") as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, key, default=None):
        return cls.get_config().get(key, default)

    @classmethod
    def get_nested(cls, *keys, default=None):
        data = cls.get_config()
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return default
        return data if data is not None else default