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
from charts.colors import (
    TREATMENT,
)
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_severity_score_new,
)
from typing import (
    Counter,
    Dict,
    NamedTuple,
    Tuple,
)

Treatment = NamedTuple(
    "Treatment",
    [
        ("acceptedUndefined", int),
        ("accepted", int),
        ("inProgress", int),
        ("undefined", int),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str, loaders: Dataloaders) -> Treatment:
    finding_cvssf: Dict[str, Decimal] = {}
    if FI_API_STATUS == "migration":
        group_findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group.lower())
        finding_ids = [finding.id for finding in group_findings_new]
        finding_cvssf = {
            finding.id: utils.get_cvssf(
                get_severity_score_new(finding.severity)
            )
            for finding in group_findings_new
        }
    else:
        group_findings_data = await loaders.group_findings.load(group.lower())
        finding_ids = [
            finding["finding_id"] for finding in group_findings_data
        ]
        finding_cvssf = {
            str(finding["finding_id"]): utils.get_cvssf(
                Decimal(finding.get("cvss_temporal", "0.0")).quantize(
                    Decimal("0.1")
                )
            )
            for finding in group_findings_data
        }

    vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    treatment: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        treatment.update(
            {
                str(
                    vulnerability["historic_treatment"][-1]["treatment"]
                ): Decimal(
                    finding_cvssf[str(vulnerability["finding_id"])]
                ).quantize(
                    Decimal("0.001")
                )
            }
        )

    return Treatment(
        acceptedUndefined=treatment["ACCEPTED_UNDEFINED"],
        accepted=treatment["ACCEPTED"],
        inProgress=treatment["IN PROGRESS"],
        undefined=treatment["NEW"],
    )


async def get_data_many_groups(
    groups: Tuple[str, ...], loaders: Dataloaders
) -> Treatment:
    groups_data = await collect(
        [get_data_one_group(group, loaders) for group in groups]
    )

    return Treatment(
        acceptedUndefined=sum(
            [group.acceptedUndefined for group in groups_data]
        ),
        accepted=sum([group.accepted for group in groups_data]),
        inProgress=sum([group.inProgress for group in groups_data]),
        undefined=sum([group.undefined for group in groups_data]),
    )


def format_data(data: Treatment) -> dict:
    translations: Dict[str, str] = {
        "acceptedUndefined": "Permanently accepted",
        "accepted": "Temporarily Accepted",
        "inProgress": "In Progress",
        "undefined": "Not defined",
    }

    return {
        "data": {
            "columns": [
                [value, str(getattr(data, key))]
                for key, value in translations.items()
            ],
            "type": "pie",
            "colors": {
                "Permanently accepted": TREATMENT.more_passive,
                "Temporarily Accepted": TREATMENT.passive,
                "In Progress": TREATMENT.neutral,
                "Not defined": TREATMENT.more_agressive,
            },
        },
        "legend": {
            "position": "right",
        },
        "pie": {
            "label": {
                "show": True,
            },
        },
    }


async def generate_all() -> None:
    loaders = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                data=await get_data_one_group(group, loaders),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(org_groups, loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(tuple(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
