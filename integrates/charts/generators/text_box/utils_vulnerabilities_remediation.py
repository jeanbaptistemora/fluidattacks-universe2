from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    RISK,
)
from charts.generators.single_value_indicator.remediation import (
    get_totals_by_week,
)
from charts.utils import (
    format_cvssf,
    get_cvssf,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    GroupNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.utils import (
    get_first_day_iso_date,
    get_min_iso_date,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from pandas import (
    date_range,
    DatetimeIndex,
)
from typing import (
    NamedTuple,
)


class FormatSprint(NamedTuple):
    created: Decimal
    solved: Decimal
    remediated: Decimal


def get_last_sprint_start_date(
    *, sprint_start_date: str, sprint_length: int
) -> datetime:
    end_date: datetime = get_min_iso_date(datetime.now()).astimezone(
        tz=timezone.utc
    )
    start_date: datetime = datetime.fromisoformat(
        sprint_start_date
    ).astimezone(tz=timezone.utc)

    sprint_dates: DatetimeIndex = date_range(
        start=start_date.isoformat(),
        end=end_date,
        freq=f'{sprint_length}W-{start_date.strftime("%A")[:3].upper()}',
    )

    if sprint_dates.size > 0:
        return datetime.combine(
            sprint_dates.tolist()[-1].date(), datetime.min.time()
        ).astimezone(tz=timezone.utc)

    return start_date


def get_percentage_change(
    *,
    current: Decimal,
    total: Decimal,
) -> Decimal:
    if total == Decimal("0.0") and current <= Decimal("0.0"):
        return Decimal("0.0")

    if total == Decimal("0.0") and current > Decimal("0.0"):
        return Decimal("1.0")

    return current / total


@alru_cache(maxsize=None, typed=True)
async def generate_one(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    group_name: str,
) -> FormatSprint:
    sprint_length: int = 1
    sprint_start_date: str = get_first_day_iso_date()
    with suppress(GroupNotFound):
        group: Group = await loaders.group.load(group_name)
        sprint_length = group.sprint_duration
        sprint_start_date = group.sprint_start_date

    current_sprint_date = get_last_sprint_start_date(
        sprint_start_date=sprint_start_date, sprint_length=sprint_length
    )
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_cvssf: dict[str, Decimal] = {
        finding.id: get_cvssf(get_severity_score(finding.severity))
        for finding in findings
    }
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        tuple(finding.id for finding in findings)
    )

    total_previous_open, total_previous_closed = await get_totals_by_week(
        vulnerabilities=vulnerabilities,
        findings_cvssf=findings_cvssf,
        last_day=current_sprint_date,
        loaders=loaders,
        sprint=True,
    )

    total_current_open, total_current_closed = await get_totals_by_week(
        vulnerabilities=vulnerabilities,
        findings_cvssf=findings_cvssf,
        last_day=datetime.now(tz=timezone.utc),
        loaders=loaders,
    )

    total_closed: Decimal = format_cvssf(total_current_closed)
    total_open: Decimal = format_cvssf(total_current_open)
    previous_closed: Decimal = format_cvssf(total_previous_closed)
    previous_open: Decimal = format_cvssf(total_previous_open)
    solved: Decimal = get_percentage_change(
        current=previous_closed, total=total_closed
    )
    created: Decimal = get_percentage_change(
        current=previous_open, total=total_open
    )
    created = created if created > Decimal("0.0") else Decimal("0")
    solved = solved if solved > Decimal("0.0") else Decimal("0")

    return FormatSprint(
        solved=solved,
        created=created,
        remediated=solved - created,
    )


async def get_many_groups(
    *,
    loaders: Dataloaders,
    group_names: tuple[str, ...],
) -> FormatSprint:
    groups_data: tuple[FormatSprint, ...] = await collect(
        tuple(
            generate_one(loaders=loaders, group_name=group_name)
            for group_name in group_names
        ),
        workers=32,
    )
    number_of_groups: int = len(groups_data)

    if number_of_groups:
        return FormatSprint(
            created=Decimal(
                sum(group.created for group in groups_data) / number_of_groups
            ),
            solved=Decimal(
                sum(group.solved for group in groups_data) / number_of_groups
            ),
            remediated=Decimal(
                sum(group.remediated for group in groups_data)
                / number_of_groups
            ),
        )

    return FormatSprint(
        created=Decimal("0.0"),
        remediated=Decimal("0.0"),
        solved=Decimal("0.0"),
    )


def format_data(count: Decimal, state: str) -> dict:
    if state == "created" and count > Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color=RISK.more_agressive,
            arrow="&#129065;",
        )

    if state == "solved" and count > Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color=RISK.more_passive,
            arrow="&#129065;",
        )

    if state == "remediated" and count > Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color=RISK.more_passive,
            arrow="&#129065;",
        )

    if state == "remediated" and count < Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color=RISK.more_agressive,
            arrow="&#129067;",
        )

    return dict(
        fontSizeRatio=0.5,
        text=count,
    )


def format_count(count: FormatSprint) -> dict[str, Decimal]:
    return {
        "created": count.created,
        "remediated": count.remediated,
        "solved": count.solved,
    }


async def generate_all(state: str) -> None:
    loaders: Dataloaders = get_new_context()
    async for group_name in iterate_groups():
        json_dump(
            document=format_data(
                count=format_count(
                    count=await generate_one(
                        loaders=loaders, group_name=group_name
                    ),
                )[state],
                state=state,
            ),
            entity="group",
            subject=group_name,
        )

    async for org_id, _, org_group_names in (
        iterate_organizations_and_groups()
    ):
        json_dump(
            document=format_data(
                count=format_count(
                    count=await get_many_groups(
                        loaders=loaders, group_names=org_group_names
                    ),
                )[state],
                state=state,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, group_names in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    count=format_count(
                        count=await get_many_groups(
                            loaders=loaders, group_names=tuple(group_names)
                        ),
                    )[state],
                    state=state,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )
