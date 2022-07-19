from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
    MAX_WITH_DECIMALS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from newutils.datetime import (
    get_datetime_from_iso_str,
    get_now,
)
from typing import (
    Optional,
)


def format_decimal(value: Decimal) -> Decimal:
    if value >= MAX_WITH_DECIMALS:
        return value.to_integral_exact(rounding=ROUND_CEILING)
    return value.quantize(Decimal("0.1"))


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str, loaders: Dataloaders) -> Decimal:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    filtered_vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.verification
    )
    if filtered_vulnerabilities:
        historic_verifications: tuple[
            tuple[VulnerabilityVerification, ...], ...
        ] = await loaders.vulnerability_historic_verification.load_many(
            vulnerability.id for vulnerability in filtered_vulnerabilities
        )
        number_of_hours: Decimal = Decimal("0.0")
        current_date: datetime = get_now()
        number_of_reattacks: int = 0
        for historic_verification in historic_verifications:
            start: Optional[str] = None
            for verification in historic_verification:
                if (
                    verification.status
                    == VulnerabilityVerificationStatus.REQUESTED
                    and start is None
                ):
                    start = verification.modified_date
                    number_of_reattacks += 1
                if (
                    verification.status
                    == VulnerabilityVerificationStatus.VERIFIED
                    and start is not None
                ):
                    number_of_hours += Decimal(
                        (
                            get_datetime_from_iso_str(
                                verification.modified_date
                            )
                            - get_datetime_from_iso_str(start)
                        ).seconds
                        / Decimal("3600.0")
                    )
                    start = None

            if start is not None:
                number_of_hours += Decimal(
                    (current_date - get_datetime_from_iso_str(start)).seconds
                    / Decimal("3600.0")
                )
                number_of_reattacks += 1

        return (
            format_decimal(number_of_hours / number_of_reattacks)
            if number_of_reattacks > 0
            else Decimal("0.0")
        )

    return Decimal("0.0")


async def get_many_groups(
    groups: tuple[str, ...], loaders: Dataloaders
) -> Decimal:
    groups_data: tuple[Decimal, ...] = await collect(
        tuple(generate_one(group, loaders) for group in groups), workers=32
    )

    return (
        format_decimal(Decimal(sum(groups_data)) / len(groups))
        if len(groups_data)
        else Decimal("0.0")
    )


def format_data(mean_time: Decimal) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": mean_time,
    }


async def generate_all() -> None:
    loaders = get_new_context()
    async for group in iterate_groups():
        json_dump(
            document=format_data(mean_time=await generate_one(group, loaders)),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                mean_time=await get_many_groups(org_groups, loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    mean_time=await get_many_groups(tuple(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
