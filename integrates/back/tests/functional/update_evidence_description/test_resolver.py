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
async def test_admin(populate: bool):
    assert populate
    draft_id: str = '475041513'
    draft_description: str = 'this is a test description'
    evidence_name: str = 'EVIDENCE1'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        description=draft_description,
        draft=draft_id,
        evidence=evidence_name
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence_description')
async def test_analyst(populate: bool):
    assert populate
    draft_id: str = '475041513'
    draft_description: str = 'this is a test description'
    evidence_name: str = 'EVIDENCE2'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        description=draft_description,
        draft=draft_id,
        evidence=evidence_name
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_evidence_description')
async def test_closer(populate: bool):
    assert populate
    draft_id: str = '475041513'
    draft_description: str = 'this is a test description'
    evidence_name: str = 'EVIDENCE3'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        description=draft_description,
        draft=draft_id,
        evidence=evidence_name
    )
    assert 'errors' not in result
    assert 'success' in result['data']['updateEvidenceDescription']
    assert result['data']['updateEvidenceDescription']['success']
