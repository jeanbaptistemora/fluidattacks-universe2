from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    LIMIT,
)
from charts.generators.common.colors import (
    TREATMENT,
)
from charts.generators.stacked_bar_chart.utils import (
    format_data_csv,
    MIN_PERCENTAGE,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus as AcceptanceStatus,
    VulnerabilityStateStatus as StateStatus,
    VulnerabilityTreatmentStatus as TreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from functools import (
    reduce,
)
import operator
from typing import (
    Counter,
    Iterable,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings: tuple[Finding, ...] = await context.group_findings.load(
        group.lower()
    )

    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await context.finding_vulnerabilities_released_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    temporarily = Counter(
        [
            f"{vuln.treatment.modified_by}/{TreatmentStatus.ACCEPTED}"
            for vuln in vulnerabilities
            if vuln.treatment
            and vuln.treatment.status == TreatmentStatus.ACCEPTED
            and vuln.state.status == StateStatus.VULNERABLE
        ]
    )
    permanently = Counter(
        [
            (
                f"{vuln.treatment.modified_by}"
                "/"
                f"{TreatmentStatus.ACCEPTED_UNDEFINED}"
            )
            for vuln in vulnerabilities
            if vuln.treatment
            and vuln.treatment.status == TreatmentStatus.ACCEPTED_UNDEFINED
            and vuln.treatment.acceptance_status == AcceptanceStatus.APPROVED
            and vuln.state.status == StateStatus.VULNERABLE
        ]
    )

    return temporarily + permanently


def get_max_value(counter_values: Iterable[int]) -> int:
    if counter_values and max(list(counter_values)):
        return max(list(counter_values))

    return 1


def format_vulnerabilities_by_data(
    *, counters: Counter[str]
) -> tuple[dict, CsvData]:
    translations: dict[str, str] = {
        "ACCEPTED_UNDEFINED": "Permanently accepted",
        "ACCEPTED": "Temporarily accepted",
    }
    counter_user: Counter[str] = Counter(
        reduce(
            operator.add,
            [
                Counter({key.split("/")[0]: value})
                for key, value in counters.most_common()
            ],
            Counter(),
        )
    )
    all_data: list[tuple[str, int]] = counter_user.most_common()
    data: list[tuple[str, int]] = all_data[:LIMIT]
    accepted: list[int] = [counters[f"{user}/ACCEPTED"] for user, _ in data]
    accepted_undefined: list[int] = [
        counters[f"{user}/ACCEPTED_UNDEFINED"] for user, _ in data
    ]
    max_acc_value: int = get_max_value(accepted)
    max_acc_undefined_value: int = get_max_value(accepted_undefined)

    max_accepted: list[str] = [
        str(value)
        if Decimal(value / max_acc_value) * Decimal("100.0") >= MIN_PERCENTAGE
        else ""
        for value in accepted
    ]
    max_accepted_undefined: list[str] = [
        str(value)
        if (Decimal(value / max_acc_undefined_value) * Decimal("100.0"))
        >= MIN_PERCENTAGE
        else ""
        for value in accepted_undefined
    ]

    json_data = dict(
        data=dict(
            colors={
                "Permanently accepted": TREATMENT.more_passive,
                "Temporarily accepted": TREATMENT.passive,
            },
            columns=[
                [value, *[counters[f"{user}/{key}"] for user, _ in data]]
                for key, value in translations.items()
            ],
            groups=[list(translations.values())],
            labels=dict(
                format={"Permanently accepted": None},
            ),
            order=None,
            stack=dict(
                normalize=False,
            ),
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[key for key, _ in data],
                type="category",
                tick=dict(
                    rotate=0,
                    multiline=False,
                ),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        maxValues={
            "Permanently accepted": max_accepted_undefined,
            "Temporarily accepted": max_accepted,
        },
        stackedBarChartYTickFormat=True,
    )

    csv_data = format_data_csv(
        columns=[
            "Permanently accepted",
            "Temporarily accepted",
        ],
        values=[
            [counters[f"{user}/{key}"] for user, _ in all_data]
            for key, _ in translations.items()
        ],
        categories=[key for key, _ in all_data],
        header="User",
    )
    return (json_data, csv_data)


async def get_data_many_groups(groups: tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


async def generate_all() -> None:
    async for group in iterate_groups():
        json_document, csv_document = format_vulnerabilities_by_data(
            counters=await get_data_one_group(group),
        )
        json_dump(
            document=json_document,
            entity="group",
            subject=group,
            csv_document=csv_document,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_document, csv_document = format_vulnerabilities_by_data(
            counters=await get_data_many_groups(org_groups),
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_document, csv_document = format_vulnerabilities_by_data(
                counters=await get_data_many_groups(tuple(groups)),
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
