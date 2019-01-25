"""Logs manager.

Linters:
    pylint:
        Used always.
        $ python3 -m pylint [path]
    flake8:
        Used always except where it contradicts pylint.
        $ python3 -m flake8 [path]
    mypy:
        Used always.
        $ python3 -m mypy --ignore-missing-imports [path]
"""

import json

from typing import Any

# Type aliases that improve clarity
JSON = Any

DOMAIN = "/logs/__tap_awsdynamodb."


def stdout_json_obj(json_obj: JSON) -> None:
    """Prints a JSON obj to stdout
    """
    print(json.dumps(json_obj))


def log_json_obj(file_name: str, json_obj: JSON) -> None:
    """ print a json_obj to the given file in append mode """
    with open(f"{DOMAIN}{file_name}.jsonstream", "a") as file:
        file.write(json.dumps(json_obj))
        file.write("\n")


def log_error(error: str) -> None:
    """ standard log to register handled errors ocurred in runtime """
    with open(f"{DOMAIN}errors.log", "a") as file:
        file.write(f"{error}\n")


def log_conversions(conversion: str) -> None:
    """ standard log to register conversions done in runtime """
    with open(f"{DOMAIN}conversions.log", "a") as file:
        file.write(f"{conversion}\n")
