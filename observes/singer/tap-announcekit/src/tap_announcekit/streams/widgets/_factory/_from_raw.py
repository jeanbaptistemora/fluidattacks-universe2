from purity.v1 import (
    PrimitiveFactory,
)
from tap_announcekit.api.gql_schema import (
    Widget as RawWidget,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
    WidgetId,
)
from tap_announcekit.objs.widget import (
    Widget,
)
from tap_announcekit.utils import (
    CastUtils,
)

_to_primitive = PrimitiveFactory.to_primitive


def to_id(proj: ProjectId, raw: RawWidget) -> WidgetId:
    return WidgetId(proj, _to_primitive(raw.id, str))


def to_obj(raw: RawWidget) -> Widget:
    return Widget(
        CastUtils.to_datetime(raw.created_at),
        _to_primitive(raw.name, str),
        _to_primitive(raw.mode, str),
        _to_primitive(raw.action, str),
        _to_primitive(raw.slug, str),
        _to_primitive(raw.options, str),
        _to_primitive(raw.theme, str),
        _to_primitive(raw.version, int),
    )
