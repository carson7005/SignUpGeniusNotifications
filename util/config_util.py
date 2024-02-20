import json #imports the library to access JSON dictionaries

def get_config(): #Function to open and load the file into an object named data; which is then returned
    config_file = open("config.json")
    data = json.load(config_file)
    config_file.close()

    return data


def get_config_item(key): #Given a key, the function returns the value from the dictionary given a key
    return get_config()[key]
