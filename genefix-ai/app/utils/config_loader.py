# Placeholder for config loader utility
import yaml
import json

class ConfigLoader:
    @staticmethod
    def load_yaml(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_json(path):
        with open(path, 'r') as f:
            return json.load(f)
