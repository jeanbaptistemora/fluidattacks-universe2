# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.text_box.utils import (
    ForcesReport,
    format_csv_data,
)


async def generate_one() -> ForcesReport:
    # By default, Forces is enabled for all groups
    # https://gitlab.com/fluidattacks/universe/-/issues/4880
    return ForcesReport(fontSizeRatio=0.5, text="Active")


async def generate_all() -> None:
    title: str = "Service status"
    async for group in utils.iterate_groups():
        document = await generate_one()
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(header=title, value=document["text"]),
        )


if __name__ == "__main__":
    run(generate_all())
