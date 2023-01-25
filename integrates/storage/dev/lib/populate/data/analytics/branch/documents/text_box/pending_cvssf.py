from aioextensions import (
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from charts.generators.text_box.utils import (
    format_csv_data,
)
from charts.utils import (
    format_cvssf,
    iterate_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
)
from decimal import (
    Decimal,
)

PENDING: Decimal = Decimal("6850.95")
TARGET: Decimal = Decimal("7.24")
ADJUSTMENT: Decimal = Decimal("0.32")
LINES_ADJUSTMENT: Decimal = Decimal("1000.0")


@alru_cache(maxsize=None, typed=True)
async def generate_one(
    group_name: str, loaders: Dataloaders
) -> PortfoliosGroupsInfo:
    group: Group = await loaders.group.load(group_name)
    toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(
            group_name=group_name,
        )
    )
    toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(
            group_name=group_name,
        )
    )
    tested_lines: Decimal = Decimal(
        sum([line.attacked_lines for line in toe_lines if line.attacked_at])
    )
    tested_inputs: Decimal = Decimal(
        sum([1 for input in toe_inputs if input.attacked_at])
    )
    target_tested: Decimal = (tested_lines / LINES_ADJUSTMENT) + tested_inputs
    if group.state.has_squad:
        return PortfoliosGroupsInfo(
            group_name=group_name,
            value=format_cvssf(PENDING + (target_tested * TARGET)),
        )

    return PortfoliosGroupsInfo(
        group_name=group_name,
        value=format_cvssf((PENDING + (target_tested * TARGET)) / ADJUSTMENT),
    )


def format_data(mean_time: PortfoliosGroupsInfo) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": mean_time.value,
    }


async def generate_all() -> None:
    loaders = get_new_context()
    text: str = "Pending CVSSF"
    async for group in iterate_groups():
        document = format_data(mean_time=await generate_one(group, loaders))
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header=text, value=str(document["text"])
            ),
        )


if __name__ == "__main__":
    run(generate_all())
