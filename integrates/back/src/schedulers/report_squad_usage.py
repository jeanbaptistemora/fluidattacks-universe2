from aioextensions import (
    collect,
)
from billing import (
    domain as billing_domain,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from newutils import (
    bugsnag as bugsnag_utils,
)
from organizations import (
    domain as orgs_domain,
)

bugsnag_utils.start_scheduler_session()


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_groups_typed(loaders)
    squad_groups: tuple[Group, ...] = tuple(
        group for group in active_groups if group.state.tier == GroupTier.SQUAD
    )
    squad_orgs_ids: list[str] = [
        group.organization_id for group in squad_groups
    ]
    squad_orgs: list[
        Organization
    ] = await loaders.organization_typed.load_many(squad_orgs_ids)
    await collect(
        [
            billing_domain.report_subscription_usage(
                group_name=group.name,
                org_billing_customer=org.billing_customer,
            )
            for group, org in zip(squad_groups, squad_orgs)
            if org.billing_customer is not None
        ]
    )
