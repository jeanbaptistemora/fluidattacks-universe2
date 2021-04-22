# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence_description')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_update_evidence_description(populate: bool, email: str):
    assert populate
    draft_id: str = '475041513'
    draft_description: str = 'this is a test description'
    evidence_name: str = 'EVIDENCE1'
    result: Dict[str, Any] = await query(
        user=email,
        description=draft_description,
        draft=draft_id,
        evidence=evidence_name
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']
