import pytest
from decimal import Decimal

import backend.domain.organization as org_domain

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_max_acceptance_days():
    org_with_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    days = await org_domain.get_max_acceptance_days(org_with_data)
    assert days == Decimal('60')

    org_without_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    days = await org_domain.get_max_acceptance_days(org_without_data)
    assert days is None


async def test_get_max_acceptance_severity():
    org_with_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    max_severity = await org_domain.get_max_acceptance_severity(org_with_data)
    assert max_severity == Decimal('6.9')

    org_without_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    max_severity = await org_domain.get_max_acceptance_severity(org_without_data)
    assert max_severity == Decimal('10.0')


async def test_get_max_number_acceptations():
    org_with_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    max_acceptations = await org_domain.get_max_number_acceptations(org_with_data)
    assert max_acceptations == Decimal('2')

    org_without_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    max_acceptations = await org_domain.get_max_number_acceptations(org_without_data)
    assert max_acceptations is None


async def test_get_min_acceptance_severity():
    org_with_data = 'ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86'
    min_severity = await org_domain.get_min_acceptance_severity(org_with_data)
    assert min_severity == Decimal('3.4')

    org_without_data = 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'
    min_severity = await org_domain.get_min_acceptance_severity(org_without_data)
    assert min_severity == Decimal('0.0')
