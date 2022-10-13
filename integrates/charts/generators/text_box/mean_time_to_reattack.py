# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.utils import (
    MAX_WITH_DECIMALS,
)
from charts.generators.text_box.utils import (
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
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from newutils.datetime import (
    get_datetime_from_iso_str,
    get_minus_delta,
    get_now,
    get_plus_delta,
)
from typing import (
    Optional,
)


def format_decimal(value: Decimal) -> Decimal:
    if value >= MAX_WITH_DECIMALS:
        return value.to_integral_exact(rounding=ROUND_CEILING)
    return value.quantize(Decimal("0.1"))


def _get_next_open(
    historic_state: tuple[VulnerabilityState, ...], verification: datetime
) -> datetime:
    for state in historic_state:
        if state.status == VulnerabilityStateStatus.OPEN:
            return get_datetime_from_iso_str(state.modified_date)
    return verification


def _get_in_between_state(
    historic_state: tuple[VulnerabilityState, ...], verification: datetime
) -> datetime:
    reverse_historic_state = tuple(reversed(historic_state))
    before_limit = get_minus_delta(verification, minutes=30)
    after_limit = get_plus_delta(verification, minutes=30)
    for index, state in enumerate(reverse_historic_state):
        if (
            state.status == VulnerabilityStateStatus.CLOSED
            and before_limit
            <= get_datetime_from_iso_str(state.modified_date)
            <= after_limit
        ):
            return _get_next_open(
                reverse_historic_state[len(historic_state) - index :],
                verification,
            )

    return verification


def get_diff(start: datetime, end: datetime) -> int:
    diff = end - start

    return diff.days if end > start else 0


async def _get_mean_time_to_reattack(
    filtered_vulnerabilities: tuple[Vulnerability, ...], loaders: Dataloaders
) -> Decimal:
    historic_verifications: tuple[
        tuple[VulnerabilityVerification, ...], ...
    ] = await loaders.vulnerability_historic_verification.load_many(
        vulnerability.id for vulnerability in filtered_vulnerabilities
    )
    historic_states: tuple[
        tuple[VulnerabilityState, ...], ...
    ] = await loaders.vulnerability_historic_state.load_many(
        vulnerability.id for vulnerability in filtered_vulnerabilities
    )

    number_of_days: int = 0
    current_date: datetime = get_now()
    number_of_reattacks: int = 0
    for vulnerability, historic_verification, historic_state in zip(
        filtered_vulnerabilities, historic_verifications, historic_states
    ):
        start: Optional[datetime] = get_datetime_from_iso_str(
            vulnerability.created_date
        )
        for verification in historic_verification:
            if (
                verification.status
                == VulnerabilityVerificationStatus.REQUESTED
                and start is not None
            ):
                number_of_reattacks += 1
                number_of_days += get_diff(
                    start,
                    get_datetime_from_iso_str(verification.modified_date),
                )
                start = None
            if (
                verification.status == VulnerabilityVerificationStatus.VERIFIED
                and start is None
            ):
                start = _get_in_between_state(
                    historic_state,
                    get_datetime_from_iso_str(verification.modified_date),
                )

        if start is not None:
            number_of_days += get_diff(start, current_date)

    return (
        format_decimal(Decimal(number_of_days / number_of_reattacks))
        if number_of_reattacks > 0
        else Decimal("0.0")
    )


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
        return await _get_mean_time_to_reattack(
            filtered_vulnerabilities, loaders
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
    text: str = "Mean time to reattack"
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

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            mean_time=await get_many_groups(org_groups, loaders),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                header=text, value=str(document["text"])
            ),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                mean_time=await get_many_groups(tuple(groups), loaders),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    header=text, value=str(document["text"])
                ),
            )


if __name__ == "__main__":
    run(generate_all())
