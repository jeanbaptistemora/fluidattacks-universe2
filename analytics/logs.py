"""
Fluid ETL script
"""

## pyhton3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import os
import json

def initialize_log(file_name):
    """ pretty print a json_obj to the given file in append mode """
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass

    file = open("./logs/" + file_name, "w")
    file.write("")


def log_json_obj(file_name, json_obj, pretty):
    """ pretty print a json_obj to the given file in append mode """
    file = open("./logs/" + file_name, "a")
    if pretty:
        file.write(json.dumps(json_obj, indent=2))
    else:
        file.write(json.dumps(json_obj))
    file.write("\n")
