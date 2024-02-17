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
            validated = validate(ConfigSchema, configData)
            if validated is True:
                config = configData
            else:  # sets config to None to prevent issues
                raise TypeError("config doesn't match schema")
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
    except Exception as exc:
        print(exc)  # yaml fails or schema does not validate
        config = None  # avoid crashing API
    return config


def validate(typ: ConfigSchema, instance: ConfigSchema) -> bool:
    for property_name, property_type in typ.__annotations__.items():
        value = instance.get(property_name, None)
        if value is None:
            # Check for missing keys
            print(f"Missing key: {property_name}")
            return False
        elif property_type not in (int, float, bool, str):  # simple types
            # check if property_type is object (e.g. not a primitive)
            result = validate(property_type, value)
            if result is False:  # fall through to check other properties
                return False
        elif not isinstance(value, property_type):
            # Check for type equality
            print(
                f"Wrong type: {property_name}. Expected {property_type}, got {type(value)}"
            )
            return False
    return True
