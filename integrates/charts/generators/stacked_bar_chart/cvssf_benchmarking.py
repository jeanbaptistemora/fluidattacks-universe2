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
    RISK,
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
from statistics import (
    mean,
)
from typing import (
    Any,
    Counter,
    Dict,
    List,
    NamedTuple,
    Tuple,
)


class OrganizationCvssfBenchmarking(NamedTuple):
    accepted: Decimal
    closed: Decimal
    open: Decimal
    organization_id: str
    total: Decimal


@alru_cache(maxsize=None, typed=True)
async def get_group_data(*, group: str, loaders: Dataloaders) -> Counter[str]:
    finding_severity: Dict[str, Decimal] = {}
    if FI_API_STATUS == "migration":
        group_findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group.lower())
        finding_severity.update(
            {
                finding.id: get_severity_score_new(finding.severity)
                for finding in group_findings_new
            }
        )
        vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
            [finding.id for finding in group_findings_new]
        )
    else:
        group_findings = await loaders.group_findings.load(group)
        finding_severity.update(
            {
                str(finding["finding_id"]): Decimal(
                    finding.get("cvss_temporal", 0.0)
                )
                for finding in group_findings
            }
        )
        vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
            [str(finding["finding_id"]) for finding in group_findings]
        )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        severity: Decimal = utils.get_cvssf(
            finding_severity[str(vulnerability["finding_id"])]
        )
        counter.update({"total": severity})
        if vulnerability["current_state"] == "open":
            if vulnerability["historic_treatment"][-1]["treatment"] in {
                "ACCEPTED",
                "ACCEPTED_UNDEFINED",
            }:
                counter.update({"accepted": severity})
            else:
                counter.update({"open": severity})
        else:
            counter.update({"closed": severity})

    return counter


@alru_cache(maxsize=None, typed=True)
async def get_data_one_organization(
    *, organization_id: str, groups: Tuple[str, ...], loaders: Dataloaders
) -> OrganizationCvssfBenchmarking:
    groups_data = await collect(
        [
            get_group_data(group=group.lower(), loaders=loaders)
            for group in groups
        ],
        workers=24,
    )

    counter: Counter[str] = sum(groups_data, Counter())

    return OrganizationCvssfBenchmarking(
        accepted=Decimal(counter["accepted"]).quantize(Decimal("0.1")),
        closed=Decimal(counter["closed"]).quantize(Decimal("0.1")),
        open=Decimal(counter["open"]).quantize(Decimal("0.1")),
        organization_id=organization_id,
        total=Decimal(counter["total"]).quantize(Decimal("0.1")),
    )


def get_best_organization(
    *, organizations: List[OrganizationCvssfBenchmarking]
) -> OrganizationCvssfBenchmarking:
    if organizations:
        return max(
            organizations,
            key=lambda organization: Decimal(
                organization.closed / organization.total
            ).quantize(Decimal("0.1"))
            if organization.total > Decimal("0.0")
            else Decimal("0.0"),
        )

    return OrganizationCvssfBenchmarking(
        accepted=Decimal("0.0"),
        closed=Decimal("1.0"),
        open=Decimal("0.0"),
        organization_id="",
        total=Decimal("1.0"),
    )


def get_mean_organizations(
    *, organizations: List[OrganizationCvssfBenchmarking]
) -> OrganizationCvssfBenchmarking:
    if organizations:
        accepted = Decimal(
            mean([organization.accepted for organization in organizations])
        ).quantize(Decimal("0.1"))
        opened = Decimal(
            mean([organization.open for organization in organizations])
        ).quantize(Decimal("0.1"))
        closed = Decimal(
            mean([organization.closed for organization in organizations])
        ).quantize(Decimal("0.1"))

        return OrganizationCvssfBenchmarking(
            accepted=accepted,
            closed=closed,
            open=opened,
            organization_id="",
            total=accepted + closed + opened,
        )

    return OrganizationCvssfBenchmarking(
        accepted=Decimal("0.0"),
        closed=Decimal("0.0"),
        open=Decimal("0.0"),
        organization_id="",
        total=Decimal("0.0"),
    )


def get_valid_organizations(
    *,
    organizations: Tuple[OrganizationCvssfBenchmarking, ...],
    organization_id: str,
) -> List[OrganizationCvssfBenchmarking]:
    return [
        organization
        for organization in organizations
        if organization_id != organization.organization_id
    ]


def format_data(
    *,
    organization: OrganizationCvssfBenchmarking,
    mean_cvssf: OrganizationCvssfBenchmarking,
    best_cvssf: OrganizationCvssfBenchmarking,
) -> Dict[str, Any]:
    return dict(
        data=dict(
            columns=[
                [
                    "Closed",
                    organization.closed,
                    mean_cvssf.closed,
                    best_cvssf.closed,
                ],
                [
                    "Accepted",
                    organization.accepted,
                    mean_cvssf.accepted,
                    best_cvssf.accepted,
                ],
                [
                    "Open",
                    organization.open,
                    mean_cvssf.open,
                    best_cvssf.open,
                ],
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": TREATMENT.passive,
                "Open": RISK.more_agressive,
            },
            type="bar",
            groups=[
                [
                    "Closed",
                    "Accepted",
                    "Open",
                ],
            ],
            order=None,
            stack=dict(
                normalize=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
        axis=dict(
            x=dict(
                categories=[
                    "My organization",
                    "Average organization",
                    "Best organization",
                ],
                type="category",
                tick=dict(multiline=False),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text="Severity (CVSSF)",
                    position="inner-top",
                ),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        normalizedToolTip=True,
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    organizations: List[Tuple[str, Tuple[str, ...]]] = []

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        organizations.append((org_id, org_groups))

    all_organizations_data = await collect(
        [
            get_data_one_organization(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
            )
            for organization in organizations
        ],
        workers=24,
    )

    best_cvssf = get_best_organization(organizations=all_organizations_data)

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                organization=await get_data_one_organization(
                    organization_id=org_id,
                    groups=org_groups,
                    loaders=loaders,
                ),
                mean_cvssf=get_mean_organizations(
                    organizations=get_valid_organizations(
                        organizations=all_organizations_data,
                        organization_id=org_id,
                    )
                ),
                best_cvssf=best_cvssf,
            ),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
