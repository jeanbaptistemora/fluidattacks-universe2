from datetime import (
    datetime,
)
import logging
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from singer_io.singer2.json import (
    InvalidType,
    to_opt_primitive,
    to_primitive,
)
from tap_announcekit.api.client import (
    ApiClient,
    Query,
)
from tap_announcekit.api.gql_schema import (
    Project as RawProject,
)
from tap_announcekit.stream import (
    StreamGetter,
)
from tap_announcekit.streams.project._objs import (
    _Project,
    Project,
    ProjectId,
)
from tap_announcekit.utils import (
    new_iter,
)
from typing import (
    Any,
    Iterator,
)

LOG = logging.getLogger(__name__)
JsonStr = str


def _to_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw
    raise InvalidType(f"{type(raw)} expected datetime")


def _to_proj(raw: RawProject) -> Project:
    draft = _Project(
        ProjectId(to_primitive(raw.id, str)),
        to_primitive(raw.encoded_id, str),
        to_primitive(raw.name, str),
        to_primitive(raw.slug, str),
        to_opt_primitive(raw.website, str),
        to_primitive(raw.is_authors_listed, bool),
        to_primitive(raw.is_whitelabel, bool),
        to_primitive(raw.is_subscribable, bool),
        to_primitive(raw.is_slack_subscribable, bool),
        to_primitive(raw.is_feedback_enabled, bool),
        to_primitive(raw.is_demo, bool),
        to_primitive(raw.is_readonly, bool),
        to_opt_primitive(raw.image_id, str),
        to_opt_primitive(raw.favicon_id, str),
        _to_datetime(raw.created_at),
        to_opt_primitive(raw.ga_property, str),
        to_primitive(raw.avatar, str),
        to_opt_primitive(raw.favicon, str),
        to_primitive(raw.locale, str),
        to_opt_primitive(raw.uses_new_feed_hostname, bool),
        to_primitive(raw.payment_gateway, str),
        _to_datetime(raw.trial_until) if raw.trial_until else None,
        to_primitive(raw.metadata, str),
    )
    return Project(draft)


def _select_proj_fields(proj_id: str, query: Query) -> IO[None]:
    proj = query.raw.project(project_id=proj_id)
    # select fields
    for attr, _ in _Project.__annotations__.items():
        _attr = "id" if attr == "proj_id" else attr
        getattr(proj, _attr)()
    return IO(None)


def _proj_query(proj_id: str) -> IO[Query]:
    query = ApiClient.new_query()
    query.bind(partial(_select_proj_fields, proj_id))
    return query


def _get_project(client: ApiClient, proj_id: ProjectId) -> IO[Project]:
    query = _proj_query(proj_id.proj_id)
    LOG.debug("query: %s", query)
    raw: IO[RawProject] = client.get(query).map(lambda q: q.project)
    return raw.map(_to_proj)


def _get_projs(
    client: ApiClient, projs: IO[Iterator[ProjectId]]
) -> IO[Iterator[Project]]:
    return projs.bind(
        lambda ids: new_iter(
            unsafe_perform_io(_get_project(client, proj)) for proj in ids
        )
    )


class ProjectGetters:
    # pylint: disable=too-few-public-methods
    @staticmethod
    def getter(client: ApiClient) -> StreamGetter[ProjectId, Project]:
        return StreamGetter(
            partial(_get_project, client), partial(_get_projs, client)
        )
