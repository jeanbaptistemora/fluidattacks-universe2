# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)
from datetime import datetime, timedelta

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_access_token')
async def test_admin(populate: bool):
    assert populate
    expiration_time: Any = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time: int = int(expiration_time.timestamp())
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        expiration_time=ts_expiration_time,
    )
    assert 'errors' not in result
    assert result['data']['updateAccessToken']['success']


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_access_token')
async def test_analyst(populate: bool):
    assert populate
    expiration_time: Any = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time: int = int(expiration_time.timestamp())
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        expiration_time=ts_expiration_time,
    )
    assert 'errors' not in result
    assert result['data']['updateAccessToken']['success']
