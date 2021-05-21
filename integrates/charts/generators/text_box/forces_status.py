# Standard library

# Third party libraries
from aioextensions import run

# Local libraries
from charts import utils
from charts.types import ForcesReport
from dataloaders import get_new_context


async def generate_one(group: str) -> ForcesReport:
    context = get_new_context()
    group_loader = context.group_all
    group_data = await group_loader.load(group)

    has_forces = group_data["has_forces"]

    return ForcesReport(
        fontSizeRatio=0.5, text="Active" if has_forces else "Inactive"
    )


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
