# Standard
from typing import Dict, List

# Third party
import pytest
from _pytest.monkeypatch import MonkeyPatch

# Local
from backend.dal.helpers import dynamodb
from roots import dal as roots_dal


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('state', 'expected_result'),
    (
        ('open', True),
        ('closed', False),
        ('DELETED', False)
    )
)
async def test_has_open_vulns(
    monkeypatch: MonkeyPatch,
    state: str,
    expected_result: bool
) -> None:
    async def mocked_async_query(*_) -> List[Dict[str, str]]:
        return [
            {
                'repo_nickname': 'product',
                'UUID': '123',
                'historic_state': [{'state': state}]
            }
        ]
    monkeypatch.setattr(dynamodb, 'async_query', mocked_async_query)

    result = await roots_dal.has_open_vulns(nickname='product')
    assert result == expected_result
