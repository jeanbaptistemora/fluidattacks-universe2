from .types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
)
from .utils import (
    format_organization_finding_policy,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
    Optional,
)


async def _get_organization_finding_policy(
    *,
    requests: tuple[OrgFindingPolicyRequest, ...],
) -> Optional[tuple[OrgFindingPolicy, ...]]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["org_finding_policy_metadata"],
            values={
                "name": request.organization_name,
                "uuid": request.policy_id,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    if len(items) == len(requests):
        response = {
            OrgFindingPolicyRequest(
                organization_name=policy.organization_name,
                policy_id=policy.id,
            ): policy
            for policy in tuple(
                format_organization_finding_policy(item) for item in items
            )
        }
        return tuple(response[request] for request in requests)

    return None


async def _get_organization_finding_policies(
    *,
    policy_dataloader: DataLoader,
    organization_name: str,
) -> tuple[OrgFindingPolicy, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={
            "name": organization_name,
        },
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["org_finding_policy_metadata"],),
        table=TABLE,
        index=index,
    )

    policies_list: list[OrgFindingPolicy] = []
    for item in response.items:
        policy = format_organization_finding_policy(item)
        policies_list.append(policy)
        policy_dataloader.prime(
            OrgFindingPolicyRequest(
                organization_name=organization_name, policy_id=policy.id
            ),
            policy,
        )

    return tuple(policies_list)


class OrganizationFindingPolicyLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[OrgFindingPolicyRequest]
    ) -> Optional[tuple[OrgFindingPolicy, ...]]:
        return await _get_organization_finding_policy(requests=tuple(requests))


class OrganizationFindingPoliciesLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> tuple[tuple[OrgFindingPolicy, ...], ...]:
        return await collect(
            tuple(
                _get_organization_finding_policies(
                    policy_dataloader=self.dataloader,
                    organization_name=organization_name,
                )
                for organization_name in organization_names
            )
        )
