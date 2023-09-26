import json

def get_config():
    config_file = open("config.json")
    data = json.load(config_file)
    config_file.close()

    return data


def get_config_item(key):
    return get_config()[key]
