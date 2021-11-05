from purity.v1 import (
    PrimitiveFactory,
    Transform,
)
from returns.curry import (
    partial,
)
from tap_announcekit.api.gql_schema import (
    ExternalUser as RawExternalUser,
    PageOfExternalUsers as RawExtUsersPage,
)
from tap_announcekit.objs.ext_user import (
    ExternalUser,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.utils import (
    CastUtils,
)

_to_primitive = PrimitiveFactory.to_primitive
_to_opt_primitive = PrimitiveFactory.to_opt_primitive


def to_user(raw: RawExternalUser) -> ExternalUser:
    return ExternalUser(
        CastUtils.to_datetime(raw.created_at),
        CastUtils.to_datetime(raw.seen_at),
        _to_opt_primitive(raw.name, str),
        _to_opt_primitive(raw.email, str),
        _to_primitive(raw.fields, str),
        _to_primitive(raw.is_anon, bool),
        _to_primitive(raw.is_following, bool),
        _to_primitive(raw.is_email_verified, bool),
        _to_opt_primitive(raw.avatar, str),
        _to_opt_primitive(raw.is_app, bool),
    )


def to_user_id(proj: ProjectId, raw: RawExternalUser) -> ExtUserId:
    return ExtUserId(proj, _to_primitive(raw.id, str))


def to_page(proj: ProjectId, raw: RawExtUsersPage) -> DataPage[ExtUserId]:
    return DataPage(
        _to_primitive(raw.page, int),
        _to_primitive(raw.pages, int),
        _to_primitive(raw.count, int),
        CastUtils.to_flist(raw.items, Transform(partial(to_user_id, proj))),
    )
