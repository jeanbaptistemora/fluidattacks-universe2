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
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from tags import (
    domain as tags_domain,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


def calculate_tag_indicators(
    tag: str,
    tags_dict: Dict[str, List[Dict[str, Any]]],
    indicator_list: List[str],
) -> Dict[str, Union[Decimal, List[str]]]:
    tag_info: Dict[str, Union[Decimal, List[str]]] = {}
    for indicator in indicator_list:
        if "max" in indicator:
            tag_info[indicator] = Decimal(
                max(
                    [
                        cast(Decimal, group.get(indicator, Decimal("0.0")))
                        for group in tags_dict[tag]
                    ]
                )
            ).quantize(Decimal("0.1"))
        elif "mean" in indicator:
            tag_info[indicator] = Decimal(
                sum(
                    [
                        cast(Decimal, group.get(indicator, Decimal("0.0")))
                        for group in tags_dict[tag]
                    ]
                )
                / Decimal(len(tags_dict[tag]))
            ).quantize(Decimal("0.1"))
        else:
            tag_info[indicator] = Decimal(
                min(
                    [
                        cast(Decimal, group.get(indicator, Decimal("inf")))
                        for group in tags_dict[tag]
                    ]
                )
            ).quantize(Decimal("0.1"))
        tag_info["projects"] = [str(group["name"]) for group in tags_dict[tag]]
    return tag_info


async def get_group_indicators_and_tags(
    loaders: Dataloaders,
    group: Group,
    indicator_list: List[str],
) -> Dict[str, Any]:
    unreliable_indicators = await loaders.group_indicators_typed.load(
        group.name
    )
    filtered_indicators = {
        indicator: getattr(unreliable_indicators, indicator)
        for indicator in indicator_list
        if getattr(unreliable_indicators, indicator) is not None
    }

    # This one is not present in group's unreliable_indicators
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.name
    )
    filtered_indicators["max_severity"] = Decimal(
        max(
            [
                float(get_severity_score(finding.severity))
                for finding in group_findings
            ]
            if group_findings
            else [0.0]
        )
    ).quantize(Decimal("0.1"))

    filtered_indicators["tag"] = group.tags
    filtered_indicators["name"] = group.name
    return filtered_indicators


async def update_organization_indicators(
    loaders: Dataloaders,
    org_name: str,
    groups: Tuple[Group, ...],
) -> Tuple[bool, List[str]]:
    success: List[bool] = []
    updated_tags: List[str] = []
    indicator_list: List[str] = [
        "max_open_severity",
        "max_severity",
        "mean_remediate",
        "mean_remediate_critical_severity",
        "mean_remediate_high_severity",
        "mean_remediate_low_severity",
        "mean_remediate_medium_severity",
        "last_closed_vulnerability_days",
    ]
    groups_indicators = list(
        await collect(
            get_group_indicators_and_tags(loaders, group.name, indicator_list)
            for group in groups
        )
    )
    tags_dict: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
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
        org_groups: Tuple[Group, ...] = await loaders.group_typed.load_many(
            org_group_names
        )
        tag_groups: Tuple[Group, ...] = tuple(
            group
            for group in org_groups
            if group.state.status == GroupStateStatus.ACTIVE and group.tags
        )
        success, updated_tags = await update_organization_indicators(
            loaders, org_name, tag_groups
        )
        if not success:
            LOGGER.error(
                "[scheduler]: error updating portfolio indicators",
                extra={"extra": {"organization": org_name}},
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
