# Standard
from typing import Dict, List

# Third party
import pytest
from _pytest.monkeypatch import MonkeyPatch

# Local
from dynamodb import operations_legacy as dynamodb_ops
from roots import dal as roots_dal


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('state', 'treatment', 'status', 'expected_result'),
    (
        ('open', 'NEW', None, True),
        ('closed', 'IN_PROGRESS', None, False),
        ('DELETED', 'NEW', None, False),
        ('open', 'ACCEPTED_UNDEFINED', None, False),
        ('open', 'NEW', 'CONFIRMED', False)
    )
)
async def test_has_open_vulns(
    monkeypatch: MonkeyPatch,
    state: str,
    treatment: str,
    status: str,
    expected_result: bool
) -> None:
    async def mocked_query(*_) -> List[Dict[str, str]]:
        return [
            {
                'repo_nickname': 'product',
                'UUID': '123',
                'historic_state': [{'state': state}],
                'historic_treatment': [{'treatment': treatment}],
                'historic_zero_risk': [{'status': status}]
            }
        ]
    monkeypatch.setattr(dynamodb_ops, 'query', mocked_query)

    result = await roots_dal.has_open_vulns(nickname='product')
    assert result == expected_result
