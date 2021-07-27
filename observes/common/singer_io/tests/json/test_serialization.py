import os
from singer_io.singer2.json import (
    DictFactory,
    JsonEmitter,
    JsonFactory,
)
import tempfile
from typing import (
    Any,
    Dict,
)

self_dir_path = os.path.dirname(__file__)


def open_data_file(file_name: str) -> Dict[str, Any]:
    with open(os.path.join(self_dir_path, file_name)) as file:
        return DictFactory.load(file)


def test_inverse() -> None:
    json_obj = JsonFactory.from_dict(open_data_file("valid_schema.json"))
    with tempfile.TemporaryFile(mode="w+") as temp:
        emitter = JsonEmitter(temp)
        emitter.emit(json_obj)
        temp.seek(0)
        json_obj_2 = JsonFactory.load(temp)
        assert json_obj == json_obj_2
