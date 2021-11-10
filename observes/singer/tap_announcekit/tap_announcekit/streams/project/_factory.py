from dataclasses import (
    dataclass,
)
from purity.v1 import (
    Transform,
)
from returns.io import (
    IO,
)
from singer_io.singer2.json import (
    to_opt_primitive,
    to_primitive,
)
from tap_announcekit.api.client import (
    ApiClient,
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    Project as RawProject,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    IndexedObj,
    ProjectId,
)
from tap_announcekit.objs.project import (
    Project,
    ProjectObj,
)
from tap_announcekit.utils import (
    CastUtils,
)
from typing import (
    cast,
)

JsonStr = str


def _to_proj(raw: RawProject) -> Project:
    raw_image_id = to_opt_primitive(raw.image_id, str)
    raw_favicon_id = to_opt_primitive(raw.favicon_id, str)
    return Project(
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
        ImageId(raw_image_id) if raw_image_id else None,
        ImageId(raw_favicon_id) if raw_favicon_id else None,
        CastUtils.to_datetime(raw.created_at),
        to_opt_primitive(raw.ga_property, str),
        to_primitive(raw.avatar, str),
        to_primitive(raw.locale, str),
        to_opt_primitive(raw.uses_new_feed_hostname, bool),
        to_primitive(raw.payment_gateway, str),
        CastUtils.to_datetime(raw.trial_until) if raw.trial_until else None,
        to_primitive(raw.metadata, str),
    )


@dataclass(frozen=True)
class ProjectQuery:
    proj_id: ProjectId

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.project(project_id=self.proj_id.id_str)
        for attr, _ in Project.__annotations__.items():
            getattr(proj, attr)()
        return IO(None)

    def query(self) -> Query[ProjectObj]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda q: IndexedObj(
                    self.proj_id, _to_proj(cast(RawProject, q.project))
                )
            ),
        )


@dataclass(frozen=True)
class ProjectFactory:
    client: ApiClient

    def get(self, proj: ProjectId) -> IO[ProjectObj]:
        query = ProjectQuery(proj).query()
        return self.client.get(query)
