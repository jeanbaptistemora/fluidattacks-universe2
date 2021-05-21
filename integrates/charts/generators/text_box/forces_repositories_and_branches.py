# Standard library

# Third party libraries
from aioextensions import run

# Local libraries
from charts import utils
from charts.types import ForcesReport


async def generate_one(group: str) -> ForcesReport:
    executions = await utils.get_all_time_forces_executions(group)
    unique_executions = set(
        f'{execution["git_repo"]}{execution["git_branch"]}'
        for execution in executions
    )

    return ForcesReport(fontSizeRatio=0.5, text=str(len(unique_executions)))


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
