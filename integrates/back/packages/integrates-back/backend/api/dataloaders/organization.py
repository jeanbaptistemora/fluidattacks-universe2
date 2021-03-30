# Standard libraries
from typing import (
    Dict,
    List,
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend.typing import Organization as OrganizationType
from organizations import domain as orgs_domain


async def _batch_load_fn(
    organization_ids: List[str]
) -> List[OrganizationType]:
    organizations: Dict[str, OrganizationType] = {}
    organizations_by_id = await collect([
        orgs_domain.get_by_id(organization_id)
        for organization_id in organization_ids
    ])

    for organization in organizations_by_id:
        organization_id = organization['id']
        organizations[organization_id] = dict(
            historic_max_number_acceptations=organization[
                'historic_max_number_acceptations'
            ],
            id=organization_id,
            max_acceptance_days=organization['max_acceptance_days'],
            max_number_acceptations=organization['max_number_acceptations'],
            max_acceptance_severity=organization['max_acceptance_severity'],
            min_acceptance_severity=organization['min_acceptance_severity'],
            name=organization['name'],
            pending_deletion_date=organization.get('pending_deletion_date'),
        )

    return [
        organizations.get(organization_id, {})
        for organization_id in organization_ids
    ]


# pylint: disable=too-few-public-methods
class OrganizationLoader(DataLoader):  # type: ignore
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        organization_ids: List[str]
    ) -> List[OrganizationType]:
        return await _batch_load_fn(organization_ids)
