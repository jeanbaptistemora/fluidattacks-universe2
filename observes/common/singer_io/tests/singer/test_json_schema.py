import json
from jsonschema.exceptions import (
    SchemaError,
)
import os
import pytest
from singer_io.singer2.json_schema import (
    jschema_from_raw,
)
from typing import (
    Any,
    Dict,
)

self_dir_path = os.path.dirname(__file__)


def open_data_file(file_name: str) -> Dict[str, Any]:
    with open(os.path.join(self_dir_path, file_name)) as file:
        return json.load(file)


def test_valid_schema() -> None:
    jschema_from_raw(open_data_file("valid_schema.json"))


def test_invalid_schema() -> None:
    with pytest.raises(SchemaError):
        jschema_from_raw(open_data_file("invalid_schema.json"))
