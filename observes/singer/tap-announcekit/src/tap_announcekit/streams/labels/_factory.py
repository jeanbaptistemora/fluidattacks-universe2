from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    PrimitiveFactory,
    Transform,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    Label as RawLabel,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    LabelId,
    ProjectId,
)
from tap_announcekit.objs.label import (
    Label,
    LabelObj,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
)
from typing import (
    cast,
    List,
)

_to_primitive = PrimitiveFactory.to_primitive


def to_obj(raw: RawLabel) -> Label:
    return Label(
        _to_primitive(raw.name, str),
        _to_primitive(raw.color, str),
    )


@dataclass(frozen=True)
class LabelsQuery:
    _to_obj: Transform[RawLabel, Label]
    proj: ProjectId

    def _select_fields(self, operation: Operation) -> IO[None]:
        item = operation.labels(project_id=self.proj.id_str)
        item.id()
        return select_fields(item, frozenset(Label.__annotations__))

    def to_label_obj(self, raw: RawLabel) -> LabelObj:
        return IndexedObj(
            LabelId(self.proj, _to_primitive(raw.id, str)), self._to_obj(raw)
        )

    @property
    def query(self) -> Query[FrozenList[LabelObj]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: tuple(
                    map(
                        self.to_label_obj,
                        tuple(cast(List[RawLabel], p.labels)),
                    )
                )
            ),
        )


@dataclass(frozen=True)
class LabelFactory:
    _client: ApiClient

    @staticmethod
    def _get_query(proj: ProjectId) -> Query[FrozenList[LabelObj]]:
        return LabelsQuery(Transform(to_obj), proj).query

    def get(self, proj: ProjectId) -> IO[FrozenList[LabelObj]]:
        query = self._get_query(proj)
        return self._client.get(query)
