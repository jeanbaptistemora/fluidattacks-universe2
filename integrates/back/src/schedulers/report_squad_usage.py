from aioextensions import (
    collect,
    run,
)
from billing import (
    domain as billing_domain,
)
from custom_types import (
    Group,
    Organization,
)
from dataloaders import (
    get_new_context,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    bugsnag as bugsnag_utils,
)
from typing import (
    Dict,
    List,
)

bugsnag_utils.start_scheduler_session()


async def main() -> None:
    loader = get_new_context()
    active_groups: List[str] = await groups_domain.get_active_groups()
    groups: List[Group] = [
        group
        for group in await loader.group.load_many(active_groups)
        if group["tier"] == "squad"
    ]
    group_orgs: Dict[str, Organization] = dict(
        zip(
            [group["name"] for group in groups],
            await loader.organization.load_many(
                [group["organization"] for group in groups]
            ),
        )
    )

    await collect(
        [
            billing_domain.report_subscription_usage(
                group_name=group_name,
                org_billing_customer=org["billing_customer"],
            )
            for group_name, org in group_orgs.items()
        ]
    )
