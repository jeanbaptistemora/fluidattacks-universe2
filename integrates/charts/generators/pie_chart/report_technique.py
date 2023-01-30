from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.pie_chart.common import (
    format_csv_data,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from typing import (
    Counter,
)

SCA_FINDINGS_IDS = ["011", "393"]


def _get_technique(
    *, vulnerability_type: VulnerabilityType, finding_title: str
) -> str:
    if any(
        finding_title.lower().startswith(title_id)
        for title_id in SCA_FINDINGS_IDS
    ):
        return "SCA"

    if vulnerability_type == VulnerabilityType.LINES:
        return "SAST"

    return "DAST"


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> Counter[str]:
    findings = await loaders.group_findings.load(group.lower())
    findings_title: dict[str, str] = {
        finding.id: finding.title for finding in findings
    }
    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )

    return Counter(
        tuple(
            _get_technique(
                vulnerability_type=vulnerability.type,
                finding_title=findings_title[vulnerability.finding_id],
            )
            for vulnerability in vulnerabilities
        )
    )


async def get_data_many_groups(
    *, groups: tuple[str, ...], loaders: Dataloaders
) -> Counter[str]:
    groups_data: tuple[Counter[str], ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return sum(groups_data, Counter())


def format_data(*, data: Counter[str]) -> dict:

    return dict(
        data=dict(
            columns=[
                ["SAST", data["SAST"]],
                ["DAST", data["DAST"]],
                ["SCA", data["SCA"]],
            ],
            type="pie",
            colors=dict(
                SAST=RISK.agressive,
                DAST=RISK.neutral,
                SCA=RISK.passive,
            ),
        ),
        legend=dict(
            position="right",
        ),
        pie=dict(
            label=dict(
                show=True,
            ),
        ),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    headers: list[str] = ["Report Technique", "Occurrences"]
    async for group in iterate_groups():
        document = format_data(
            data=await get_data_one_group(group=group, loaders=loaders),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=headers),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            data=await get_data_many_groups(
                groups=org_groups, loaders=loaders
            ),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=headers),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(
                    groups=tuple(groups), loaders=loaders
                ),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document, header=headers
                ),
            )


if __name__ == "__main__":
    run(generate_all())
