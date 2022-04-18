from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity.json.factory import (
    load,
)
from fa_purity.json.value.core import (
    JsonValue,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from typing import (
    IO,
)


@dataclass(frozen=True)
class Creds:
    key_id: str
    key: str
    region: str

    @staticmethod
    def from_file(file: IO[str]) -> Creds:
        jval = JsonValue(load(file).unwrap())
        data = Unfolder(jval).to_dict_of(str).unwrap()
        return Creds(
            data["AWS_ACCESS_KEY_ID"],
            data["AWS_SECRET_ACCESS_KEY"],
            data["AWS_DEFAULT_REGION"],
        )
