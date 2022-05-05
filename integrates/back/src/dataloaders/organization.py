from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model.organization.types import (
    Organization,
)
from newutils.organizations import (
    format_organization,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    Dict,
    Iterable,
    List,
)


async def _batch_load_fn(
    organization_ids: List[str],
) -> List[Dict[str, Any]]:
    organizations: Dict[str, Dict[str, Any]] = {}
    organizations_by_id = await collect(
        [
            orgs_domain.get_by_id(organization_id)
            for organization_id in organization_ids
        ]
    )

    for organization in organizations_by_id:
        organization_id = organization["id"]
        organizations[organization_id] = dict(
            billing_customer=organization.get("billing_customer", None),
            historic_max_number_acceptations=get_key_or_fallback(
                organization,
                "historic_max_number_acceptances",
                "historic_max_number_acceptations",
            ),
            id=organization_id,
            max_acceptance_days=organization["max_acceptance_days"],
            max_acceptance_severity=organization["max_acceptance_severity"],
            max_number_acceptations=get_key_or_fallback(
                organization,
                "max_number_acceptances",
                "max_number_acceptations",
            ),
            min_acceptance_severity=organization["min_acceptance_severity"],
            name=organization["name"],
            pending_deletion_date=organization.get("pending_deletion_date"),
        )
    return [
        organizations.get(organization_id, {})
        for organization_id in organization_ids
    ]


class OrganizationLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_ids: List[str]
    ) -> List[Dict[str, Any]]:
        return await _batch_load_fn(organization_ids)


class OrganizationTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> tuple[Organization, ...]:
        organizations_by_id = await collect(
            [
                orgs_domain.get_by_id(organization_id)
                for organization_id in organization_ids
            ]
        )
        return tuple(
            format_organization(
                item=organization_id,
                organization_id=organization_id["id"],
            )
            for organization_id in organizations_by_id
        )
