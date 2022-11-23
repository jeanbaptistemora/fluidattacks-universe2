"""Log manager.

Linters:
    prospector:
        Used always.
        $ prospector --strictness veryhigh [path]
    mypy:
        Used always.
        $ python3 -m mypy --ignore-missing-imports [path]
"""

import json
from typing import (
    Any,
)

# Type aliases that improve clarity
JSON = Any

DOMAIN = "./logs/__tap_formstack."


def stdout_json_obj(json_obj: JSON) -> None:
    """Print a JSON obj to stdout."""
    print(json.dumps(json_obj))


def log_json_obj(file_name: str, json_obj: JSON) -> None:
    """Print a json_obj to the given file in append mode."""
    with open(
        f"{DOMAIN}{file_name}.jsonstream", "a", encoding="UTF-8"
    ) as file:
        file.write(json.dumps(json_obj))
        file.write("\n")


def log_error(error: str) -> None:
    """Standard log to register handled errors ocurred in runtime."""
    with open(f"{DOMAIN}errors.log", "a", encoding="UTF-8") as file:
        file.write(f"{error}\n")


def log_conversions(conversion: str) -> None:
    """Standard log to register conversions done in runtime."""
    with open(f"{DOMAIN}conversions.log", "a", encoding="UTF-8") as file:
        file.write(f"{conversion}\n")
