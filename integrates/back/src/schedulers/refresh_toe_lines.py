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
from batch.types import (
    PutActionResult,
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
    results: list[PutActionResult] = await collect(  # type: ignore
        put_action(
            action=Action.REFRESH_TOE_LINES,
            additional_info="*",
            entity=group_name,
            product_name=Product.INTEGRATES,
            subject="integrates@fluidattacks.com",
            queue="small",
        )
        for group_name in group_names
    )
    futures_rebase = [
        put_action(
            action=Action.REBASE,
            additional_info="*",
            entity=group_name,
            product_name=Product.INTEGRATES,
            subject="integrates@fluidattacks.com",
            queue="small",
            attempt_duration_seconds=14400,
            dependsOn=[
                {
                    "jobId": execution.batch_job_id,
                    "type": "SEQUENTIAL",
                },
            ],
        )
        for group_name, execution in zip(group_names, results)
    ]
    await collect(futures_rebase)
