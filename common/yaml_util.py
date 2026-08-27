import yaml
import os

def read_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")
    return read_yaml(config_path)["test"]
