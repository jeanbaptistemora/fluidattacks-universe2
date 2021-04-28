# Standard libraries
from typing import (
    Optional,
    Tuple,
)
from uuid import uuid4

# Local libraries
from custom_exceptions import (
    InvalidFindingNamePolicy,
    RepeatedFindingNamePolicy,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
)
from .dal import (
    add_org_finding_policy,
    get_org_finding_policies,
)


async def get_finding_policies(
    *,
    org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await get_org_finding_policies(org_name=org_name)


def validate_finding_name(name: str) -> None:
    if not findings_utils.is_valid_finding_title(name):
        raise InvalidFindingNamePolicy()


async def get_finding_policy_by_name(
    *,
    org_name: str,
    finding_name: str
) -> Optional[OrgFindingPolicyItem]:
    return next(
        (
            fin_policy
            for fin_policy in await get_finding_policies(org_name=org_name)
            if fin_policy.metadata.name.split('.')[0].lower() == finding_name
        ),
        None
    )


async def add_finding_policy(
    *,
    finding_name: str,
    org_name: str,
    user_email: str,
) -> None:
    validate_finding_name(finding_name)
    finding_policy = await get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.split('.')[0].lower(),
    )
    if finding_policy:
        raise RepeatedFindingNamePolicy()

    new_finding_policy = OrgFindingPolicyItem(
        org_name=org_name,
        id=str(uuid4()),
        metadata=OrgFindingPolicyMetadata(
            name=finding_name
        ),
        state=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status='SUBMITTED'
        )
    )
    await add_org_finding_policy(finding_policy=new_finding_policy)
