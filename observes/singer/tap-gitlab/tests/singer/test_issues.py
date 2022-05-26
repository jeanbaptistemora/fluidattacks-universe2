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
from tap_gitlab.singer.issues import (
    records,
    schemas,
)
from tap_gitlab.singer.issues.core import (
    SingerStreams,
)
from tests.mock_data import (
    issues as MOCK,
)


def test_issue_assignees_schema() -> None:
    assert schemas.issue_assignees()


def test_issue_labels_schema() -> None:
    assert schemas.issue_labels()


def test_issue_schema() -> None:
    assert schemas.issue()


def _validate_record(record: SingerRecord) -> Result[None, ValidationError]:
    stream = SingerStreams(record.stream)
    if stream is SingerStreams.issue:
        return schemas.issue().schema.validate(record.record)
    if stream is SingerStreams.issue_assignees:
        return schemas.issue_assignees().schema.validate(record.record)
    if stream is SingerStreams.issue_labels:
        return schemas.issue_labels().schema.validate(record.record)
    raise Exception("Not valid stream")


def test_schema_record_compliance() -> None:
    test_cases = (MOCK.mock_issue_all_empty, MOCK.mock_issue_full)
    data = from_flist(
        tuple(records.issue_records(i) for i in test_cases)
    ).transform(lambda x: chain(x))
    results = data.map(
        lambda r: _validate_record(r).alt(raise_exception).unwrap()
    )
    for r in results:
        assert r is None
