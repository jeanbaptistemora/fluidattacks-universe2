# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('organization')
@pytest.mark.parametrize(
    ['email'],
    [
        ['admin@gmail.com'],
    ]
)
async def test_get_organization_ver_1(populate: bool, email: str):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    org_name: str = 'orgtest'
    org_stakeholders: List[str] = [
        'admin@gmail.com',
        'analyst@gmail.com',
        'closer@gmail.com',
        'customer@gmail.com',
        'customeradmin@gmail.com',
        'executive@gmail.com',
        'resourcer@gmail.com',
        'reviewer@gmail.com',
    ]
    result: Dict[str, Any] = await query(
        user=email,
        org=org_id
    )
    groups: List[str] = [group['name'] for group in result['data']['organization']['projects']]
    stakeholders: List[str] = [stakeholder['email'] for stakeholder in result['data']['organization']['stakeholders']]
    assert 'errors' not in result
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == 90
    assert result['data']['organization']['maxAcceptanceSeverity'] == 7
    assert result['data']['organization']['maxNumberAcceptations'] == 4
    assert result['data']['organization']['minAcceptanceSeverity'] == 3
    assert result['data']['organization']['name'] == org_name.lower()
    assert sorted(groups) == []
    assert sorted(stakeholders) == org_stakeholders



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('organization')
@pytest.mark.parametrize(
    ['email'],
    [
        ['analyst@gmail.com'],
        ['closer@gmail.com'],
    ]
)
async def test_get_organization_ver_e(populate: bool, email: str):
    assert populate
    org_id: str = 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db'
    org_name: str = 'orgtest'
    org_groups: List[str] = [
        'group1',
    ]
    result: Dict[str, Any] = await query(
        user=email,
        org=org_id
    )
    groups: List[str] = [group['name'] for group in result['data']['organization']['projects']]
    assert result['data']['organization']['id'] == org_id
    assert result['data']['organization']['maxAcceptanceDays'] == 90
    assert result['data']['organization']['maxAcceptanceSeverity'] == 7
    assert result['data']['organization']['maxNumberAcceptations'] == 4
    assert result['data']['organization']['minAcceptanceSeverity'] == 3
    assert result['data']['organization']['name'] == org_name.lower()
    assert sorted(groups) == org_groups
