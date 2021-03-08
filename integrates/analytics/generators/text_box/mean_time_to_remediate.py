# Standard library
from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from statistics import (
    mean,
)
from typing import (
    Any,
    List,
    Optional,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)

# Local libraries
from backend.api import (
    get_new_context,
)
from backend.domain.project import (
    get_mean_remediate,
)
from analytics import (
    utils,
)
from newutils import (
    datetime as datetime_utils,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(
    group: str,
    context: Any,
    min_date: Optional[date] = None
) -> Decimal:
    return await get_mean_remediate(context, group.lower(), min_date)


async def get_many_groups(
    groups: Tuple[str, ...],
    context: Any,
    min_date: Optional[date] = None
) -> Decimal:
    groups_data = await collect(
        generate_one(group, context, min_date) for group in list(groups)
    )

    return (
        Decimal(mean(groups_data)).quantize(Decimal('0.1'))
        if groups_data else Decimal('Infinity')
    )


def format_data(mean_remediate: Decimal) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': mean_remediate,
    }


async def generate_all() -> None:
    context = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                mean_remediate=await generate_one(group, context),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                mean_remediate=await get_many_groups(
                    org_groups, context
                ),
            ),
            entity='organization',
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    mean_remediate=await get_many_groups(groups, context),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )

    # Limit days
    list_days: List[int] = [30, 90]
    dates: List[date] = [
        datetime_utils.get_now_minus_delta(days=list_days[0]).date(),
        datetime_utils.get_now_minus_delta(days=list_days[1]).date()
    ]
    for days, min_date in zip(list_days, dates):
        async for group in utils.iterate_groups():
            utils.json_dump(
                document=format_data(
                    mean_remediate=await generate_one(
                        group, context, min_date
                    ),
                ),
                entity='group',
                subject=f'{group}_{days}',
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            utils.json_dump(
                document=format_data(
                    mean_remediate=await get_many_groups(
                        org_groups, context, min_date
                    ),
                ),
                entity='organization',
                subject=f'{org_id}_{days}',
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                utils.json_dump(
                    document=format_data(
                        mean_remediate=await get_many_groups(
                            groups, context, min_date
                        ),
                    ),
                    entity='portfolio',
                    subject=f'{org_id}PORTFOLIO#{portfolio}_{days}',
                )


if __name__ == '__main__':
    run(generate_all())
