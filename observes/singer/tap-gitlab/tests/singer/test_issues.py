from tap_gitlab.singer.issues import (
    schemas,
)


def test_issue_assignees_schema() -> None:
    assert schemas.issue_assignees()


def test_issue_labels_schema() -> None:
    assert schemas.issue_labels()


def test_issue_schema() -> None:
    assert schemas.issue()
