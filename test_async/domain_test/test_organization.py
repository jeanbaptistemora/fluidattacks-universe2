import pytest
from decimal import Decimal

import backend.domain.organization as org_domain
from backend.exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidNumberAcceptations
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]

async def test_get_id_for_group():
    group_name = 'unittesting'
    org_id = await org_domain.get_id_for_group(group_name)
    assert org_id == 'ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3'


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


async def test_validate_negative_values():
    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_max_acceptance_severity(Decimal('-1'))

    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_min_acceptance_severity(Decimal('-1'))

    with pytest.raises(InvalidAcceptanceDays):
        org_domain.validate_max_acceptance_days(-1)

    with pytest.raises(InvalidNumberAcceptations):
        org_domain.validate_max_number_acceptations(-1)


async def test_validate_severity_range():
    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_max_acceptance_severity(Decimal('10.1'))

    with pytest.raises(InvalidAcceptanceSeverity):
        org_domain.validate_min_acceptance_severity(Decimal('10.1'))

    with pytest.raises(InvalidAcceptanceSeverityRange):
        org_domain.validate_acceptance_severity_range(
            Decimal('8.0'),
            Decimal('5.0')
        )
