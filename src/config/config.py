import src.config.utils as utils
from schema import Schema, Use
import yaml
import os


def fetch_config() -> utils.ConfigSchema | None:
    config = None
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "config.yml")

    try:
        with open(abs_file_path, "r") as stream:
            configData = yaml.safe_load(stream)
            # time to cast config to TypedDict
            schema = Schema(Use(utils.ConfigSchema))
            schema.validate(configData)
            config = configData
    except OSError as exc:
        # file does not exist
        print(exc)
        with open(abs_file_path, "w") as stream:
            yaml.dump(utils.defaultConfig, stream)
            config = utils.defaultConfig
    except Exception as exc:
        print(exc)  # yaml fails or schema does not validate
        config = None  # avoid crashing API
    return config
