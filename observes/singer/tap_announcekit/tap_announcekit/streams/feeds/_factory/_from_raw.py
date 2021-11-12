from purity.v1 import (
    PrimitiveFactory,
)
from tap_announcekit.api.gql_schema import (
    Feed as RawFeed,
)
from tap_announcekit.objs.feed import (
    Feed,
)
from tap_announcekit.objs.id_objs import (
    FeedId,
    ProjectId,
)
from tap_announcekit.utils import (
    CastUtils,
)

_to_primitive = PrimitiveFactory.to_primitive
_to_opt_primitive = PrimitiveFactory.to_opt_primitive


def to_id(proj: ProjectId, raw: RawFeed) -> FeedId:
    return FeedId(proj, _to_primitive(raw.id, str))


def to_obj(raw: RawFeed) -> Feed:
    return Feed(
        _to_primitive(raw.name, str),
        _to_primitive(raw.slug, str),
        CastUtils.to_datetime(raw.created_at),
        _to_opt_primitive(raw.custom_host, str),
        _to_opt_primitive(raw.website, str),
        _to_primitive(raw.color, str),
        _to_primitive(raw.url, str),
        _to_primitive(raw.is_unindexed, bool),
        _to_primitive(raw.is_private, bool),
        _to_primitive(raw.is_readmore, bool),
        _to_opt_primitive(raw.html_inject, str),
        _to_primitive(raw.metadata, str),
        _to_primitive(raw.theme, str),
        _to_primitive(raw.version, int),
    )
