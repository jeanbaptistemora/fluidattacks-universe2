from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v1 import (
    JsonFactory,
)
from typing import (
    IO as FILE,
)


@dataclass(frozen=True)
class Creds:
    key_id: str
    key: str
    region: str

    @staticmethod
    def from_file(file: FILE[str]) -> Creds:
        data = JsonFactory.load(file)
        return Creds(
            data["AWS_ACCESS_KEY_ID"].to_primitive(str),
            data["AWS_SECRET_ACCESS_KEY"].to_primitive(str),
            data["AWS_DEFAULT_REGION"].to_primitive(str),
        )
