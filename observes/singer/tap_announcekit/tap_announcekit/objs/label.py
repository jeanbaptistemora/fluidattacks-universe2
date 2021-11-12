from dataclasses import (
    dataclass,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    LabelId,
)

JsonStr = str


@dataclass(frozen=True)
class Label:
    name: str
    color: str


LabelObj = IndexedObj[LabelId, Label]
