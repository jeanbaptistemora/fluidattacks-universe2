from os.path import (
    dirname,
    join,
)
from singer_io.singer2.deserializer import (
    SingerDeserializer,
)
from singer_io.singer2.emitter import (
    SingerEmitter,
)
from singer_io.singer2.json import (
    JsonEmitter,
)
import tempfile
from typing import (
    List,
)

data_dir = join(dirname(__file__), "mock_data")


def open_singer_file(file_name: str) -> List[str]:
    with open(join(data_dir, file_name), encoding="UTF-8") as file:
        return file.readlines()


def test_inverse() -> None:
    with open(join(data_dir, "test.singer"), encoding="UTF-8") as file:
        singers = list(SingerDeserializer.from_file(file))
    with tempfile.TemporaryFile(mode="w+") as temp:
        emitter = SingerEmitter(JsonEmitter(temp))
        for singer in singers:
            emitter.emit(singer)
        temp.seek(0)
        singers_2 = list(map(SingerDeserializer.deserialize, temp.readlines()))
        assert singers == singers_2
