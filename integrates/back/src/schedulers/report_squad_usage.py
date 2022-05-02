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
from groups import (
    domain as groups_domain,
)
from newutils import (
    bugsnag as bugsnag_utils,
)
from typing import (
    Any,
)

bugsnag_utils.start_scheduler_session()


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups_names: tuple[str, ...] = tuple(
        await groups_domain.get_active_groups()
    )
    active_groups: tuple[Group, ...] = await loaders.group_typed.load_many(
        active_groups_names
    )
    squad_groups: tuple[Group, ...] = tuple(
        group for group in active_groups if group.state.tier == GroupTier.SQUAD
    )
    squad_orgs_ids: list[str] = [
        group.organization_id for group in squad_groups
    ]
    squad_orgs: list[dict[str, Any]] = await loaders.organization.load_many(
        squad_orgs_ids
    )
    await collect(
        [
            billing_domain.report_subscription_usage(
                group_name=group.name,
                org_billing_customer=org["billing_customer"],
            )
            for group, org in zip(squad_groups, squad_orgs)
        ]
    )
