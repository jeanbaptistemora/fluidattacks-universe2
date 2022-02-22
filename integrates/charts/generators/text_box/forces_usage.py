from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.text_box.utils import (
    ForcesReport,
)


async def generate_one(group: str) -> ForcesReport:
    executions = await utils.get_all_time_forces_executions(group)

    return ForcesReport(fontSizeRatio=0.5, text=str(len(executions)))


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
