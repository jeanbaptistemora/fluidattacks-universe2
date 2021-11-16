from purity.v1 import (
    PrimitiveFactory,
)
from tap_announcekit.api.gql_schema import (
    SegmentProfile as RawSegmentProfile,
    SegmentType as RawSegmentType,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
)

_to_primitive = PrimitiveFactory.to_primitive


def to_segment(raw: RawSegmentType) -> str:
    return _to_primitive(raw, str)


def to_segment_prof(raw: RawSegmentProfile) -> IndexedObj[str, str]:
    return IndexedObj(
        _to_primitive(raw.title, str),
        _to_primitive(raw.rules, str),
    )
