from src.config.configType import ConfigSchema
from uuid import uuid4
import yaml
import os


def fetch_config() -> ConfigSchema | None:
    config = None
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "config.yml")

    try:
        with open(abs_file_path, "r") as stream:
            configData = yaml.safe_load(stream)
            # time to cast config to TypedDict
            try:
                validated = validate(ConfigSchema, configData)
                if validated is True:
                    config = configData
            except TypeError | IndexError as exc:
                print(exc)  # schema does not validate, don't overwrite corrupt config
                config = None  # avoid crashing API
    except OSError as exc:  # only rewrites config if it doesn't exist
        # file does not exist, or file is missing some fields
        print(exc)
        with open(abs_file_path, "w") as stream:
            defaultConfig = ConfigSchema(
                {
                    "server": {"host": "0.0.0.0", "port": 5000},
                    "secret_key": uuid4().int,
                }
            )
            yaml.dump(defaultConfig, stream)
            config = defaultConfig
    return config


def validate(typ: ConfigSchema, instance: ConfigSchema):
    for property_name, property_type in typ.__annotations__.items():
        value = instance.get(property_name, None)
        if value is None:
            # Check for missing keys
            raise IndexError(f"Missing key: {property_name}")
        elif property_type not in (int, float, bool, str):  # simple types
            # check if property_type is object (e.g. not a primitive)
            validate(property_type, value)
        elif not isinstance(value, property_type):
            # Check for type equality
            raise TypeError(
                f"Wrong type: {property_name}. Expected {property_type}, got {type(value)}"
            )
    return True
