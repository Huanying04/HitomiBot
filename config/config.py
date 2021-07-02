import json


def read_config():
    with open('config.json', encoding='utf-8') as f:
        return json.loads(f.read())
