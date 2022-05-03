from aioextensions import (
    collect,
)
from batch.dal import (
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from organizations import (
    domain as orgs_domain,
)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    await collect(
        put_action(
            action=Action.REFRESH_TOE_LINES,
            additional_info="*",
            entity=group_name,
            product_name=Product.INTEGRATES,
            subject="integrates@fluidattacks.com",
            queue="spot_later",
        )
        for group_name in group_names
    )
