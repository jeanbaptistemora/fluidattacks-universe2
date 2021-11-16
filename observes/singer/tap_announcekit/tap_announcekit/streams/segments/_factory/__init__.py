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
    ApiClient,
    Query,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.objs.segment import (
    SegmentField,
    SegmentProfile,
)
from tap_announcekit.streams.segments._factory import (
    _from_raw,
    _queries,
)


def _get_segments_query(proj: ProjectId) -> Query[FrozenList[SegmentField]]:
    return _queries.SegmentFieldQuery(
        Transform(_from_raw.to_segment),
        proj,
    ).query


def _get_segment_profs(proj: ProjectId) -> Query[FrozenList[SegmentProfile]]:
    return _queries.SegmentProfileQuery(
        Transform(_from_raw.to_segment_prof),
        proj,
    ).query


@dataclass(frozen=True)
class SegmentFactory:
    _client: ApiClient

    def get_segments(self, proj: ProjectId) -> IO[FrozenList[SegmentField]]:
        query = _get_segments_query(proj)
        return self._client.get(query)

    def get_profiles(self, proj: ProjectId) -> IO[FrozenList[SegmentProfile]]:
        query = _get_segment_profs(proj)
        return self._client.get(query)
