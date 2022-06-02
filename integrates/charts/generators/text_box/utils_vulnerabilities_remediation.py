from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
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
    timedelta,
    timezone,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
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
from typing import (
    NamedTuple,
)


class FormatSprint(NamedTuple):
    created: Decimal
    solved: Decimal
    remediated: Decimal


@alru_cache(maxsize=None, typed=True)
async def generate_one(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    group_name: str,
) -> FormatSprint:
    sprint_duration: int = 1
    with suppress(GroupNotFound):
        group: Group = await loaders.group.load(group_name)
        sprint_duration = group.sprint_duration

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
        last_day=(
            datetime.now(tz=timezone.utc) - timedelta(weeks=sprint_duration)
        ),
        loaders=loaders,
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
    solved: Decimal = Decimal(
        (total_closed - previous_closed) / total_closed
        if total_closed
        else Decimal("0"),
    )
    created: Decimal = Decimal(
        (total_open - previous_open) / total_open
        if total_open
        else Decimal("0"),
    )

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

    if len(groups_data):
        return FormatSprint(
            created=Decimal(sum(group.created for group in groups_data)),
            solved=Decimal(sum(group.solved for group in groups_data)),
            remediated=Decimal(sum(group.remediated for group in groups_data)),
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
            color="red",
            arrow="\uD83E\uDC29",
        )

    if state == "solved" and count > Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color="green",
            arrow="\uD83E\uDC29",
        )

    if state == "remediated" and count > Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color="green",
            arrow="\uD83E\uDC29",
        )

    if state == "remediated" and count < Decimal("0.0"):
        return dict(
            arrowFontSizeRatio=0.6,
            fontSizeRatio=0.5,
            text=count,
            color="green",
            arrow="\uD83E\uDC2B",
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
