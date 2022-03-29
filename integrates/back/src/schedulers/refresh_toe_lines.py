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
from groups import (
    domain as groups_domain,
)


async def main() -> None:
    groups = await groups_domain.get_active_groups()
    await collect(
        put_action(
            action=Action.REFRESH_TOE_LINES,
            additional_info="*",
            entity=group,
            product_name=Product.INTEGRATES,
            subject="integrates@fluidattacks.com",
            queue="spot_later",
        )
        for group in groups
    )
