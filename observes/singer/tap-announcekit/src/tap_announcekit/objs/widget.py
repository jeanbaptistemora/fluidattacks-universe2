from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    WidgetId,
)

JsonStr = str


@dataclass(frozen=True)
class Widget:
    # pylint: disable=too-many-instance-attributes
    created_at: datetime
    name: str
    mode: str
    action: str
    slug: str
    options: JsonStr
    theme: JsonStr
    version: int


WidgetObj = IndexedObj[WidgetId, Widget]
