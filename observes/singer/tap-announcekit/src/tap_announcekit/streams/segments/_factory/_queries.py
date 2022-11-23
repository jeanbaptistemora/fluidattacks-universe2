from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    Transform,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    SegmentProfile as RawSegmentProfile,
    SegmentType as RawSegmentType,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    ProjectId,
)
from tap_announcekit.objs.segment import (
    SegmentField,
    SegmentProfile,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
)
from typing import (
    cast,
    List,
)


@dataclass(frozen=True)
class SegmentFieldQuery:
    _to_obj: Transform[RawSegmentType, str]
    proj: ProjectId

    def _select_fields(self, operation: Operation) -> IO[None]:
        operation.segments(project_id=self.proj.id_str)
        return IO(None)

    @property
    def query(self) -> Query[FrozenList[SegmentField]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: tuple(
                    SegmentField(self.proj, self._to_obj(f))
                    for f in cast(List[RawSegmentType], p.segments)
                )
            ),
        )


@dataclass(frozen=True)
class SegmentProfileQuery:
    _to_obj: Transform[RawSegmentProfile, IndexedObj[str, str]]
    proj: ProjectId

    def _select_fields(self, operation: Operation) -> IO[None]:
        selection = operation.segment_profiles(project_id=self.proj.id_str)
        return select_fields(
            selection,
            frozenset(SegmentProfile.__annotations__) - frozenset(["proj"]),
        )

    def to_segment_prof(self, raw: RawSegmentProfile) -> SegmentProfile:
        _obj = self._to_obj(raw)
        return SegmentProfile(self.proj, _obj.id_obj, _obj.obj)

    @property
    def query(self) -> Query[FrozenList[SegmentProfile]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: tuple(
                    self.to_segment_prof(r)
                    for r in cast(List[RawSegmentType], p.segment_profiles)
                )
            ),
        )
