import authz
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    get_new_context,
)
import logging
import logging.config
from organizations import (
    domain as organizations_domain,
)
from organizations_finding_policies.domain import (
    get_finding_policy,
    update_treatment_in_org_groups,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


async def is_allowed(
    *, organization_id: str, status: str, user_email: str
) -> bool:
    enforcer = await authz.get_organization_level_enforcer(user_email)
    if status == "APPROVED":
        return enforcer(
            organization_id,
            "api_mutations_handle_finding_policy_acceptation_mutate",
        )
    if status == "INACTIVE":
        return enforcer(
            organization_id, "api_mutations_deactivate_finding_policy_mutate"
        )

    return False


async def handle_finding_policy(*, item: BatchProcessing) -> None:
    message = (
        f"Processing handle organization finding policy requested by "
        f"{item.subject} for organization {item.additional_info}"
    )
    LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]), **NOEXTRA)

    organization_id: str = await organizations_domain.get_id_by_name(
        item.additional_info
    )
    groups: List[str] = await organizations_domain.get_groups(organization_id)
    finding_policy = await get_finding_policy(
        org_name=item.additional_info, finding_policy_id=item.entity
    )

    if finding_policy.state.status in {
        "APPROVED",
        "INACTIVE",
    } and await is_allowed(
        organization_id=organization_id.lower(),
        status=finding_policy.state.status,
        user_email=item.subject,
    ):
        loader = get_new_context()
        finding_name: str = finding_policy.metadata.name.split(".")[0].lower()
        await update_treatment_in_org_groups(
            finding_name=finding_name,
            loaders=loader,
            groups=groups,
            status=finding_policy.state.status,
            user_email=item.subject,
        )

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
