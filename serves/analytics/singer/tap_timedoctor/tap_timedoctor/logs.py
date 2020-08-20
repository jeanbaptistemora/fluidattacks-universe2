"""Logs manager."""

import json

from typing import Any

# Type aliases that improve clarity
JSON = Any

DOMAIN = "./logs/__tap_timedoctor."


def stdout_json_obj(json_obj: JSON) -> None:
    """Print a JSON obj to stdout"""
    print(json.dumps(json_obj))


def log_json_obj(file_name: str, json_obj: JSON) -> None:
    """Print a json_obj to the given file in append mode."""
    with open(f"{DOMAIN}{file_name}.jsonstream", "a") as file:
        file.write(json.dumps(json_obj))
        file.write("\n")
