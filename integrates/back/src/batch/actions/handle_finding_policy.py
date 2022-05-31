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
from db_model.organizations.types import (
    Organization,
)
import logging
import logging.config
from newutils import (
    groups as groups_utils,
)
from organizations_finding_policies.domain import (
    get_finding_policy,
    update_finding_policy_in_groups,
)
from settings import (
    LOGGING,
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


async def handle_finding_policy(*, item: BatchProcessing) -> None:
    message = (
        f"Processing handle organization finding policy requested by "
        f"{item.subject} for organization {item.additional_info}"
    )
    LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]))

    organization_name = item.additional_info
    finding_policy = await get_finding_policy(
        org_name=organization_name, finding_policy_id=item.entity
    )

    if finding_policy.state.status in {
        "APPROVED",
        "INACTIVE",
    }:
        loaders: Dataloaders = get_new_context()
        organization: Organization = await loaders.organization.load(
            organization_name
        )
        organization_id: str = organization.id
        groups: tuple[Group, ...] = await loaders.organization_groups.load(
            organization_id
        )
        active_groups = groups_utils.filter_active_groups(groups)
        active_group_names = [group.name for group in active_groups]
        finding_name: str = finding_policy.metadata.name.lower()
        (
            updated_finding_ids,
            updated_vuln_ids,
        ) = await update_finding_policy_in_groups(
            loaders=loaders,
            finding_name=finding_name,
            group_names=active_group_names,
            status=finding_policy.state.status,
            user_email=item.subject,
            tags=set(finding_policy.metadata.tags),
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
