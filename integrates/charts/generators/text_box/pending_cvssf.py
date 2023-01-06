from aioextensions import (
    collect,
    run,
)
from aiohttp import (
    ClientConnectorError,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
    ServerTimeoutError,
)
from async_lru import (
    alru_cache,
)
from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
    HTTPClientError,
    ReadTimeoutError,
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
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_inputs.types import (
    RootToeInputsRequest,
    ToeInput,
)
from db_model.toe_lines.types import (
    RootToeLinesRequest,
    ToeLines,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from itertools import (
    chain,
)

PENDING: Decimal = Decimal("6850.95")
TARGET: Decimal = Decimal("7.24")
ADJUSTMENT: Decimal = Decimal("0.32")
LINES_ADJUSTMENT: Decimal = Decimal("1000.0")


@alru_cache(maxsize=None, typed=True)
@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
        ClientPayloadError,
        ConnectionResetError,
        ConnectTimeoutError,
        CustomUnavailabilityError,
        HTTPClientError,
        ReadTimeoutError,
        ServerTimeoutError,
        UnavailabilityError,
    ),
    sleep_seconds=30,
    max_attempts=5,
)
async def generate_one(
    group_name: str, loaders: Dataloaders
) -> PortfoliosGroupsInfo:
    group: Group = await loaders.group.load(group_name)
    group_roots: tuple[Root] = await loaders.group_roots.load(group_name)
    all_toe_lines: tuple[tuple[ToeLines, ...], ...] = await collect(
        tuple(
            loaders.root_toe_lines.load_nodes(
                RootToeLinesRequest(
                    group_name=group_name,
                    root_id=root.id,
                )
            )
            for root in group_roots
        ),
        workers=1,
    )
    all_toe_inputs: tuple[tuple[ToeInput, ...], ...] = await collect(
        tuple(
            loaders.root_toe_inputs.load_nodes(
                RootToeInputsRequest(
                    group_name=group_name,
                    root_id=root.id,
                )
            )
            for root in group_roots
        ),
        workers=1,
    )

    toe_lines: tuple[ToeLines, ...] = tuple(chain.from_iterable(all_toe_lines))
    toe_inputs: tuple[ToeInput, ...] = tuple(
        chain.from_iterable(all_toe_inputs)
    )
    tested_lines: Decimal = Decimal(
        sum(line.attacked_lines for line in toe_lines if line.attacked_at)
    )
    tested_inputs: Decimal = Decimal(
        sum(1 for input in toe_inputs if input.state.attacked_at)
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
