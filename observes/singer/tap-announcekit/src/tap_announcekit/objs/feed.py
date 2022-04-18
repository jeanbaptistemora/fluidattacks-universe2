from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.objs.id_objs import (
    FeedId,
    IndexedObj,
)
from typing import (
    Optional,
)

JsonStr = str


@dataclass(frozen=True)
class Feed:
    # pylint: disable=too-many-instance-attributes
    name: str
    slug: str
    created_at: datetime
    custom_host: Optional[str]
    website: Optional[str]
    color: str
    url: str
    is_unindexed: bool
    is_private: bool
    is_readmore: bool
    html_inject: Optional[str]
    metadata: JsonStr
    theme: JsonStr
    version: int


FeedObj = IndexedObj[FeedId, Feed]
