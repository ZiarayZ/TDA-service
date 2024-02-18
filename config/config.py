from config.configType import ConfigSchema, fetch_default
from typing import TypedDict, Any
import yaml
import os


def fetch_config() -> ConfigSchema | None:
    config = None
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "config.yml")

    try:
        validated = tValidRet(altered=False, valid=False, data=config)
        with open(abs_file_path, "r") as stream:
            configData = yaml.safe_load(stream)
            # time to cast config to TypedDict
            validated = validate(ConfigSchema, configData)
        if validated["valid"] is True:
            config = validated["data"]
            if validated["altered"] is True:  # overwrite config
                with open(abs_file_path, "w") as file:
                    yaml.dump(config, file)
        # need to verify config
    except OSError as exc:  # only rewrites config if it doesn't exist
        # file does not exist, or file is missing some fields
        print("config does not exist")
        with open(abs_file_path, "w") as stream:
            defaultConfig = fetch_default("configschema")
            yaml.dump(defaultConfig, stream)
            config = defaultConfig
    except Exception as exc:
        print(exc)
        return None
    return config


class tValidRet(TypedDict):
    data: Any | None
    valid: bool
    altered: bool


def validate(typ, instance) -> tValidRet:
    altered = False
    try:
        for property_name, property_type in typ.__annotations__.items():
            value = instance.get(property_name, None)
            if value is None:
                # Check for missing keys
                instance[property_name] = fetch_default(property_name)
                altered = True
            elif property_type not in (int, float, bool, str):  # simple types
                # check if property_type is object (e.g. not a primitive)
                validate(property_type, value)
            elif not isinstance(value, property_type):
                # Check for type equality
                raise TypeError(
                    f"Wrong type: {property_name}. Expected {property_type}, got {type(value)}"
                )
    except TypeError | IndexError as exc:
        print(exc)  # schema does not validate, don't overwrite corrupt config
        return {"data": None, "valid": False, "altered": False}  # avoid crashing API
    return {"data": instance, "valid": True, "altered": altered}
