from os.path import (
    dirname,
    join,
)
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

data_dir = join(dirname(dirname(__file__)), "mock_data")


def open_data_file(file_name: str) -> Dict[str, Any]:
    with open(join(data_dir, file_name), encoding="UTF-8") as file:
        return DictFactory.load(file)


def test_inverse() -> None:
    json_obj = JsonFactory.from_dict(open_data_file("valid_schema.json"))
    with tempfile.TemporaryFile(mode="w+") as temp:
        emitter = JsonEmitter(temp)
        emitter.emit(json_obj)
        temp.seek(0)
        json_obj_2 = JsonFactory.load(temp)
        assert json_obj == json_obj_2
