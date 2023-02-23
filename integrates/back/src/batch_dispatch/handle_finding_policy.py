from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    OrgFindingPolicyNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
)
import logging
import logging.config
from newutils import (
    groups as groups_utils,
)
from organizations.utils import (
    get_organization,
)
from organizations_finding_policies.domain import (
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
    loaders: Dataloaders = get_new_context()
    finding_policy: (
        OrgFindingPolicy | None
    ) = await loaders.organization_finding_policy.load(
        OrgFindingPolicyRequest(
            organization_name=organization_name, policy_id=item.entity
        )
    )
    if not finding_policy:
        raise OrgFindingPolicyNotFound()
    if finding_policy.state.status in {
        PolicyStateStatus.APPROVED,
        PolicyStateStatus.INACTIVE,
    }:
        organization = await get_organization(loaders, organization_name)
        organization_id: str = organization.id
        groups: list[Group] = await loaders.organization_groups.load(
            organization_id
        )
        active_groups = groups_utils.filter_active_groups(tuple(groups))
        active_group_names = [group.name for group in active_groups]
        finding_name: str = finding_policy.name.lower()
        (
            updated_finding_ids,
            updated_vuln_ids,
        ) = await update_finding_policy_in_groups(
            loaders=loaders,
            email=item.subject,
            finding_name=finding_name,
            group_names=active_group_names,
            status=finding_policy.state.status,
            tags=set(finding_policy.tags),
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
