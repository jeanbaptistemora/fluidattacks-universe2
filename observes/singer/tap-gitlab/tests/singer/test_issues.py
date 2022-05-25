from tap_gitlab.singer.issues import (
    schemas,
)


def test_issue_assignees_schema() -> None:
    assert schemas.issue_assignees()
