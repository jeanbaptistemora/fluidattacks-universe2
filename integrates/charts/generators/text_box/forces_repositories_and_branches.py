from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.common.utils import (
    get_all_time_forces_executions,
)
from charts.generators.text_box.utils import (
    ForcesReport,
    format_csv_data,
)


async def generate_one(group: str) -> ForcesReport:
    executions = await get_all_time_forces_executions(group)
    unique_executions = set(
        f"{execution.repo}{execution.branch}" for execution in executions
    )

    return ForcesReport(fontSizeRatio=0.5, text=str(len(unique_executions)))


async def generate_all() -> None:
    document: ForcesReport
    async for group in utils.iterate_groups():
        document = await generate_one(group)
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header="Repositories and branches", value=document["text"]
            ),
        )


if __name__ == "__main__":
    run(generate_all())
