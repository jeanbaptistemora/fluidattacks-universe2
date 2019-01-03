"""
logs manager
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import json

DOMAIN = "/logs/__tap_timedoctor."

def log_open(name):
    """ open a file in append mode, and creates it if not exists """
    try:
        file = open(name, "a")
    except FileNotFoundError:
        file = open(name, "w")
    return file

def log_json_obj(file_name, json_obj):
    """ print a json_obj to the given file in append mode """
    file = log_open(DOMAIN + file_name + ".json")
    file.write(json.dumps(json_obj))
    file.write("\n")

    file_pretty = log_open(DOMAIN + file_name + ".pretty.json")
    file_pretty.write(json.dumps(json_obj, indent=2))
    file_pretty.write("\n")

def log_error(error):
    """ standard log to register handled errors ocurred in runtime """
    file = log_open(DOMAIN + "errors.log")
    file.write(error + "\n")

def log_conversions(conversion):
    """ standard log to register conversions done in runtime """
    file = log_open(DOMAIN + "conversions.log")
    file.write(conversion + "\n")
