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
from db_model.forces.types import (
    ForcesExecution,
)


async def generate_one(group: str) -> ForcesReport:
    executions: tuple[
        ForcesExecution, ...
    ] = await utils.get_all_time_forces_executions(group)

    return ForcesReport(fontSizeRatio=0.5, text=str(len(executions)))


async def generate_all() -> None:
    text: str = "Service usage"
    async for group in utils.iterate_groups():
        document = await generate_one(group)
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(header=text, value=document["text"]),
        )


if __name__ == "__main__":
    run(generate_all())
