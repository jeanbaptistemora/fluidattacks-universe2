from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
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
    timezone,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
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
    get_minus_delta,
    get_now,
    get_plus_delta,
)
from typing import (
    Optional,
)


def format_decimal(value: Decimal) -> Decimal:
    return value.to_integral_exact(rounding=ROUND_CEILING)


def _get_next_open(
    historic_state: tuple[VulnerabilityState, ...]
) -> Optional[datetime]:
    for state in historic_state:
        if state.status == VulnerabilityStateStatus.VULNERABLE:
            return state.modified_date
    return None


def _get_in_between_state(
    historic_state: tuple[VulnerabilityState, ...], verification: datetime
) -> Optional[datetime]:
    reverse_historic_state = tuple(reversed(historic_state))
    before_limit = get_minus_delta(verification, minutes=30)
    after_limit = get_plus_delta(verification, minutes=30)
    for index, state in enumerate(reverse_historic_state):
        if (
            state.status == VulnerabilityStateStatus.SAFE
            and before_limit <= state.modified_date <= after_limit
        ):
            return _get_next_open(
                reverse_historic_state[len(historic_state) - index :]
            )

    return verification


def get_diff(*, start: Optional[datetime], end: datetime) -> int:
    if start is None:
        return 0

    end_utc = end.astimezone(tz=timezone.utc)
    start_utc = start.astimezone(tz=timezone.utc)
    diff = end_utc - start_utc
    return diff.days if end_utc > start_utc else 0


def is_requested(
    verification: VulnerabilityVerification, start: Optional[datetime]
) -> bool:
    return (
        verification.status == VulnerabilityVerificationStatus.REQUESTED
        and start is not None
    )


def is_on_hold(
    verification: VulnerabilityVerification, start: Optional[datetime]
) -> bool:
    return (
        verification.status == VulnerabilityVerificationStatus.ON_HOLD
        and start is not None
    )


def is_verifying(
    verification: VulnerabilityVerification, start: Optional[datetime]
) -> bool:
    return (
        verification.status == VulnerabilityVerificationStatus.VERIFIED
        and start is None
    )


async def _get_mean_time_to_reattack(
    filtered_vulnerabilities: tuple[Vulnerability, ...],
    loaders: Dataloaders,
    current_date: datetime,
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
    number_of_reattacks: int = 0
    for vulnerability, historic_verification, historic_state in zip(
        filtered_vulnerabilities, historic_verifications, historic_states
    ):
        start: Optional[datetime] = vulnerability.created_date
        for verification in historic_verification:
            if is_requested(verification, start):
                number_of_reattacks += 1
                number_of_days += get_diff(
                    start=start,
                    end=verification.modified_date,
                )
                start = None
            if is_on_hold(verification, start):
                start = None
                number_of_reattacks -= 1
            if is_verifying(verification, start):
                start = _get_in_between_state(
                    historic_state,
                    verification.modified_date,
                )

        if start is not None:
            number_of_days += get_diff(start=start, end=current_date)
            number_of_reattacks += 1

    return (
        format_decimal(Decimal(number_of_days / number_of_reattacks))
        if number_of_reattacks > 0
        else Decimal("0.0")
    )


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str, loaders: Dataloaders) -> Decimal:
    group_: Group = await loaders.group.load(group)
    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)

    if not group_.state.has_squad:
        return Decimal("Infinity")

    all_vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vulnerability
        for vulnerability in all_vulnerabilities
        if not vulnerability.treatment
        or (
            vulnerability.treatment
            and vulnerability.treatment.status
            != VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        )
    )

    filtered_reattack_vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.verification
    )

    current_date: datetime = get_now()
    filtered_non_reattack_vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if not vulnerability.verification
    )
    sum_of_days: Decimal = (
        Decimal(
            sum(
                [
                    get_diff(
                        start=vulnerability.created_date,
                        end=current_date,
                    )
                    if vulnerability.state.status
                    == VulnerabilityStateStatus.VULNERABLE
                    else get_diff(
                        start=vulnerability.created_date,
                        end=vulnerability.state.modified_date,
                    )
                    for vulnerability in filtered_non_reattack_vulnerabilities
                ]
            )
            / len(filtered_non_reattack_vulnerabilities)
        )
        if filtered_non_reattack_vulnerabilities
        else Decimal("0.0")
    )

    if filtered_reattack_vulnerabilities:
        return format_decimal(
            sum_of_days
            + await _get_mean_time_to_reattack(
                filtered_reattack_vulnerabilities, loaders, current_date
            )
        )

    return format_decimal(sum_of_days)


async def get_many_groups(
    groups: tuple[str, ...], loaders: Dataloaders
) -> Decimal:
    groups_data: tuple[Decimal, ...] = await collect(
        tuple(generate_one(group, loaders) for group in groups), workers=32
    )

    groups_filtered: tuple[Decimal, ...] = tuple(
        group for group in groups_data if group != Decimal("Infinity")
    )

    return (
        format_decimal(Decimal(sum(groups_filtered)) / len(groups_filtered))
        if groups_filtered
        else Decimal("Infinity")
    )


def format_data(mean_time: Decimal) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": mean_time if mean_time != Decimal("Infinity") else "",
    }


async def generate_all() -> None:
    loaders = get_new_context()
    text: str = "Mean time to request reattacks"
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
