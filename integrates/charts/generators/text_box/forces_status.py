from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.text_box.utils import (
    ForcesReport,
)


async def generate_one() -> ForcesReport:
    # By default, Forces is enabled for all groups
    # https://gitlab.com/fluidattacks/product/-/issues/4880
    return ForcesReport(fontSizeRatio=0.5, text="Active")


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
