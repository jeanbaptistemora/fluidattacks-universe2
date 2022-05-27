from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.generators.single_value_indicator.remediation import (
    get_totals_by_week,
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
        finding.id: utils.get_cvssf(get_severity_score(finding.severity))
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

    total_closed: Decimal = utils.format_cvssf(total_current_closed)
    total_open: Decimal = utils.format_cvssf(total_current_open)
    previous_closed: Decimal = utils.format_cvssf(total_previous_closed)
    previous_open: Decimal = utils.format_cvssf(total_previous_open)
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


def format_data(count: FormatSprint) -> dict:
    return {
        "created": count.created,
        "remediated": count.remediated,
        "solved": count.solved,
    }


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for group_name in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                count=await generate_one(
                    loaders=loaders, group_name=group_name
                ),
            ),
            entity="group",
            subject=group_name,
        )

    async for org_id, _, org_group_names in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                count=await get_many_groups(
                    loaders=loaders, group_names=org_group_names
                ),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, group_names in await utils.get_portfolios_groups(
            org_name
        ):
            utils.json_dump(
                document=format_data(
                    count=await get_many_groups(
                        loaders=loaders, group_names=tuple(group_names)
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
