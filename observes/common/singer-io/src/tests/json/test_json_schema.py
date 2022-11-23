from jsonschema.exceptions import (
    SchemaError,
)
from os.path import (
    dirname,
    join,
)
import pytest
from singer_io.singer2.json import (
    DictFactory,
)
from singer_io.singer2.json_schema import (
    JsonSchemaFactory,
)
from typing import (
    Any,
    Dict,
)

data_dir = join(dirname(dirname(__file__)), "mock_data")


def open_data_file(file_name: str) -> Dict[str, Any]:
    with open(join(data_dir, file_name), encoding="UTF-8") as file:
        return DictFactory.load(file)


def test_valid_schema() -> None:
    JsonSchemaFactory.from_dict(open_data_file("valid_schema.json"))


def test_invalid_schema() -> None:
    with pytest.raises(SchemaError):
        JsonSchemaFactory.from_dict(open_data_file("invalid_schema.json"))
