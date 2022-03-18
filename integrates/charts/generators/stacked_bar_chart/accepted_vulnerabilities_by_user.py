from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    TREATMENT,
)
from charts.generators.stacked_bar_chart.utils import (
    MIN_PERCENTAGE,
)
from charts.utils import (
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
from typing import (
    Any,
    Counter,
    Dict,
    Iterable,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings: Tuple[Finding, ...] = await context.group_findings.load(
        group.lower()
    )

    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await context.finding_vulnerabilities_nzr.load_many_chained(
        tuple(finding.id for finding in group_findings)
    )

    temporarily = Counter(
        [
            f"{vuln.treatment.modified_by}/{TreatmentStatus.ACCEPTED}"
            for vuln in vulnerabilities
            if vuln.treatment.status == TreatmentStatus.ACCEPTED
            and vuln.state.status == StateStatus.OPEN
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
            if vuln.treatment.status == TreatmentStatus.ACCEPTED_UNDEFINED
            and vuln.treatment.acceptance_status == AcceptanceStatus.APPROVED
            and vuln.state.status == StateStatus.OPEN
        ]
    )

    return temporarily + permanently


def get_max_value(counter_values: Iterable[int]) -> int:
    if counter_values and max(list(counter_values)):
        return max(list(counter_values))

    return 1


def format_vulnerabilities_by_data(
    *, counters: Counter[str]
) -> Dict[str, Any]:
    translations: Dict[str, str] = {
        "ACCEPTED_UNDEFINED": "Permanently accepted",
        "ACCEPTED": "Temporarily accepted",
    }
    data: List[Tuple[str, int]] = Counter(
        {key.split("/")[0]: value for key, value in counters.most_common()}
    ).most_common(12)
    accepted: List[int] = [counters[f"{user}/ACCEPTED"] for user, _ in data]
    accepted_undefined: List[int] = [
        counters[f"{user}/ACCEPTED_UNDEFINED"] for user, _ in data
    ]
    max_acc_value: int = get_max_value(accepted)
    max_acc_undefined_value: int = get_max_value(accepted_undefined)

    max_accepted: List[str] = [
        str(value)
        if Decimal(value / max_acc_value) * Decimal("100.0") >= MIN_PERCENTAGE
        else ""
        for value in accepted
    ]
    max_accepted_undefined: List[str] = [
        str(value)
        if (Decimal(value / max_acc_undefined_value) * Decimal("100.0"))
        >= MIN_PERCENTAGE
        else ""
        for value in accepted_undefined
    ]

    return dict(
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
            x=dict(
                categories=[key for key, _ in data],
                type="category",
                tick=dict(
                    rotate=12,
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


async def get_data_many_groups(groups: Tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


async def generate_all() -> None:
    async for group in iterate_groups():
        json_dump(
            document=format_vulnerabilities_by_data(
                counters=await get_data_one_group(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_vulnerabilities_by_data(
                counters=await get_data_many_groups(org_groups),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_vulnerabilities_by_data(
                    counters=await get_data_many_groups(tuple(groups)),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
