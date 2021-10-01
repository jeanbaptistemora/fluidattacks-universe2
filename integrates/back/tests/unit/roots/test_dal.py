from _pytest.monkeypatch import (
    MonkeyPatch,
)
from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import pytest
from roots import (
    dal as roots_dal,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("state", "treatment", "status", "expected_result"),
    (
        ("open", "NEW", None, True),
        ("closed", "IN_PROGRESS", None, False),
        ("DELETED", "NEW", None, False),
        ("open", "ACCEPTED_UNDEFINED", None, False),
        ("open", "NEW", "CONFIRMED", False),
    ),
)
async def test_has_open_vulns(
    monkeypatch: MonkeyPatch,
    state: str,
    treatment: str,
    status: str,
    expected_result: bool,
) -> None:
    async def mocked_query(*_) -> List[Dict[str, Any]]:  # type: ignore
        return [
            {
                "finding_id": "",
                "repo_nickname": "product",
                "UUID": "123",
                "historic_state": [{"state": state}],
                "historic_treatment": [{"treatment": treatment}],
                "historic_zero_risk": [{"status": status}],
            }
        ]

    monkeypatch.setattr(dynamodb_ops, "query", mocked_query)

    class MockedDraftsLoader(DataLoader):
        async def batch_load_fn(*_: Any) -> List[List[Finding]]:
            return [[]]

    class MockedContext(NamedTuple):
        group_drafts: MockedDraftsLoader

    result = await roots_dal.has_open_vulns(
        nickname="product",
        context=MockedContext(group_drafts=MockedDraftsLoader()),
        group_name="",
    )
    assert result == expected_result


@pytest.mark.asyncio
async def test_has_open_draft_vulns(monkeypatch: MonkeyPatch) -> None:
    async def mocked_query(*_) -> List[Dict[str, Any]]:  # type: ignore
        return [
            {
                "finding_id": "123",
                "repo_nickname": "product",
                "UUID": "123",
                "historic_state": [{"state": "OPEN"}],
                "historic_treatment": [{"treatment": "NEW"}],
            }
        ]

    monkeypatch.setattr(dynamodb_ops, "query", mocked_query)

    class MockedDraftsLoader(DataLoader):
        async def batch_load_fn(*_: Any) -> List[List[Finding]]:
            return [[{"id": "123"}]]

    class MockedContext(NamedTuple):
        group_drafts: MockedDraftsLoader

    result = await roots_dal.has_open_vulns(
        nickname="product",
        context=MockedContext(group_drafts=MockedDraftsLoader()),
        group_name="",
    )
    assert not result
