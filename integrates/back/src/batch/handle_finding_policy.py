import authz
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
import logging
import logging.config
from newutils import (
    groups as groups_utils,
)
from organizations import (
    domain as organizations_domain,
)
from organizations_finding_policies.domain import (
    get_finding_policy,
    update_finding_policy_in_groups,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    List,
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
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
            "api_mutations_handle_finding_policy_acceptance_mutate",
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

    organization_name: str = item.additional_info
    organization_id: str = await organizations_domain.get_id_by_name(
        organization_name
    )
    organization_groups: List[str] = await organizations_domain.get_groups(
        organization_id
    )
    finding_policy = await get_finding_policy(
        org_name=organization_name, finding_policy_id=item.entity
    )

    if finding_policy.state.status in {
        "APPROVED",
        "INACTIVE",
    } and await is_allowed(
        organization_id=organization_id.lower(),
        status=finding_policy.state.status,
        user_email=item.subject,
    ):
        loaders: Dataloaders = get_new_context()
        groups: Tuple[Group, ...] = await loaders.group_typed.load_many(
            tuple((group, organization_id) for group in organization_groups)
        )
        groups_filtered = groups_utils.filter_active_groups(groups)
        group_names: List[str] = [group.name for group in groups_filtered]
        finding_name: str = finding_policy.metadata.name.lower()
        (
            updated_finding_ids,
            updated_vuln_ids,
        ) = await update_finding_policy_in_groups(
            finding_name=finding_name,
            loaders=loaders,
            groups=group_names,
            status=finding_policy.state.status,
            user_email=item.subject,
            tags=finding_policy.metadata.tags,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.handle_finding_policy,
            finding_ids=updated_finding_ids,
            vulnerability_ids=updated_vuln_ids,
        )

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
