from aioextensions import (
    collect,
)
from collections import (
    defaultdict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    error,
    info,
)
from tags import (
    domain as tags_domain,
)
from typing import (
    Any,
    Union,
)


def calculate_tag_indicators(
    tag: str,
    tags_dict: dict[str, list[dict[str, Any]]],
    indicator_list: list[str],
) -> dict[str, Union[Decimal, list[str]]]:
    tag_info: dict[str, Union[Decimal, list[str]]] = {}
    for indicator in indicator_list:
        if "max" in indicator:
            tag_info[indicator] = Decimal(
                max(
                    Decimal(group.get(indicator, Decimal("0.0")))
                    for group in tags_dict[tag]
                )
            ).quantize(Decimal("0.1"))
        elif "mean" in indicator:
            tag_info[indicator] = Decimal(
                sum(
                    Decimal(group.get(indicator, Decimal("0.0")))
                    for group in tags_dict[tag]
                )
                / Decimal(len(tags_dict[tag]))
            ).quantize(Decimal("0.1"))
        else:
            tag_info[indicator] = Decimal(
                min(
                    Decimal(group.get(indicator, Decimal("inf")))
                    for group in tags_dict[tag]
                )
            ).quantize(Decimal("0.1"))
        tag_info["projects"] = [str(group["name"]) for group in tags_dict[tag]]
    return tag_info


def format_indicators(
    indicators: GroupUnreliableIndicators,
) -> dict[str, Any]:
    formatted_indicators = {
        "max_open_severity": getattr(indicators, "max_open_severity"),
        "max_severity": getattr(indicators, "max_severity"),
        "mean_remediate": getattr(indicators, "mean_remediate"),
        "mean_remediate_critical_severity": getattr(
            indicators, "mean_remediate_critical_severity"
        ),
        "mean_remediate_high_severity": getattr(
            indicators, "mean_remediate_high_severity"
        ),
        "mean_remediate_low_severity": getattr(
            indicators, "mean_remediate_low_severity"
        ),
        "mean_remediate_medium_severity": getattr(
            indicators, "mean_remediate_medium_severity"
        ),
        "last_closing_date": Decimal(
            getattr(indicators, "last_closed_vulnerability_days")
        )
        if indicators.last_closed_vulnerability_days
        else None,
    }
    return {
        key: value
        for key, value in formatted_indicators.items()
        if value is not None
    }


async def get_group_indicators_and_tags(
    loaders: Dataloaders,
    group: Group,
) -> dict[str, Any]:
    unreliable_indicators = await loaders.group_indicators_typed.load(
        group.name
    )
    filtered_indicators = format_indicators(unreliable_indicators)

    # This one is not present in group's unreliable_indicators
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.name
    )
    filtered_indicators["max_severity"] = (
        Decimal(
            max(
                float(get_severity_score(finding.severity))
                for finding in group_findings
            )
        ).quantize(Decimal("0.1"))
        if group_findings
        else Decimal("0.0")
    )

    filtered_indicators["tag"] = group.tags or {}
    filtered_indicators["name"] = group.name
    return filtered_indicators


async def update_organization_indicators(
    loaders: Dataloaders,
    org_name: str,
    groups: tuple[Group, ...],
) -> tuple[bool, list[str]]:
    success: list[bool] = []
    updated_tags: list[str] = []
    indicator_list: list[str] = [
        "max_open_severity",
        "max_severity",
        "mean_remediate",
        "mean_remediate_critical_severity",
        "mean_remediate_high_severity",
        "mean_remediate_low_severity",
        "mean_remediate_medium_severity",
        "last_closing_date",
    ]
    groups_indicators = list(
        await collect(
            get_group_indicators_and_tags(
                loaders=loaders,
                group=group,
            )
            for group in groups
        )
    )
    tags_dict: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for group_indicators in groups_indicators:
        for tag in group_indicators["tag"]:
            tags_dict[tag].append(group_indicators)
    for tag in tags_dict:
        updated_tags.append(tag)
        tag_info = calculate_tag_indicators(tag, tags_dict, indicator_list)
        success.append(await tags_domain.update(org_name, tag, tag_info))
    return all(success), updated_tags


async def update_portfolios() -> None:
    """Update portfolios metrics."""
    loaders: Dataloaders = get_new_context()
    async for _, org_name, org_group_names in (
        orgs_domain.iterate_organizations_and_groups()
    ):
        info(
            "[scheduler]: working on organization",
            extra={"organization": org_name},
        )
        org_groups: tuple[Group, ...] = await loaders.group_typed.load_many(
            org_group_names
        )
        tag_groups: tuple[Group, ...] = tuple(
            group
            for group in org_groups
            if group.state.status == GroupStateStatus.ACTIVE and group.tags
        )
        success, updated_tags = await update_organization_indicators(
            loaders, org_name, tag_groups
        )
        if not success:
            error(
                "[scheduler]: error updating portfolio indicators",
                extra={"organization": org_name},
            )

        org_tags = await loaders.organization_tags.load(org_name)
        deleted_tags = [
            tag["tag"] for tag in org_tags if tag["tag"] not in updated_tags
        ]
        await collect(
            tags_domain.delete(org_name, str(tag)) for tag in deleted_tags
        )


async def main() -> None:
    await update_portfolios()
