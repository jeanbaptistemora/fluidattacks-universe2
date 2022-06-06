from fa_purity import (
    Result,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from jsonschema import (
    ValidationError,
)
from tap_gitlab.api2.ids import (
    ProjectId,
)
from tap_gitlab.singer.members import (
    records,
    schemas,
)
from tap_gitlab.singer.members.core import (
    SingerStreams,
)
from tests.mock_data import (
    members as MOCK,
)


def test_issue_schema() -> None:
    assert schemas.members()


def _validate_record(record: SingerRecord) -> Result[None, ValidationError]:
    stream = SingerStreams(record.stream)
    if stream is SingerStreams.members:
        return schemas.members().schema.validate(record.record)
    raise Exception("Not valid stream")


def test_schema_record_compliance() -> None:
    mock_proj = ProjectId.from_name("TheProject")
    test_cases = (MOCK.mock_member,)
    data = from_flist(
        tuple(records.member_records(mock_proj, i) for i in test_cases)
    ).transform(lambda x: chain(x))
    results = data.map(
        lambda r: _validate_record(r).alt(raise_exception).unwrap()
    )
    for r in results:
        assert r is None
