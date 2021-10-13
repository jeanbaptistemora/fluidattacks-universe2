from aioextensions import (
    collect,
)
from collections import (
    defaultdict,
)
from custom_types import (
    Group as GroupType,
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
from findings.domain.core import (
    get_severity_score,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils.utils import (
    get_key_or_fallback,
)
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
    cast,
    Dict,
    List,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


def calculate_tag_indicators(
    tag: str, tags_dict: Dict[str, List[GroupType]], indicator_list: List[str]
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


async def update_organization_indicators(
    loaders: Dataloaders, org_name: str, groups: List[str]
) -> Tuple[bool, List[str]]:
    group_findings_loader = loaders.group_findings_new
    success: List[bool] = []
    updated_tags: List[str] = []
    indicator_list: List[str] = [
        "max_open_severity",
        "mean_remediate",
        "mean_remediate_critical_severity",
        "mean_remediate_high_severity",
        "mean_remediate_low_severity",
        "mean_remediate_medium_severity",
        "last_closing_date",
    ]
    tags_dict: Dict[str, List[GroupType]] = defaultdict(list)
    groups_attrs = await collect(
        groups_domain.get_attributes(group, indicator_list + ["tag"])
        for group in groups
    )
    group_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await group_findings_loader.load_many(groups)
    for index, group in enumerate(groups):
        groups_attrs[index]["max_severity"] = Decimal(
            max(
                [
                    float(get_severity_score(finding.severity))
                    for finding in group_findings[index]
                ]
                if group_findings[index]
                else [0.0]
            )
        ).quantize(Decimal("0.1"))
        groups_attrs[index]["name"] = group
        for tag in groups_attrs[index]["tag"]:
            tags_dict[tag].append(groups_attrs[index])
    for tag in tags_dict:
        updated_tags.append(tag)
        tag_info = calculate_tag_indicators(
            tag, tags_dict, indicator_list + ["max_severity"]
        )
        success.append(await tags_domain.update(org_name, tag, tag_info))
    return all(success), updated_tags


async def update_portfolios() -> None:
    """Update portfolios metrics"""
    loaders: Dataloaders = get_new_context()
    group_loader = loaders.group
    async for _, org_name, org_groups in (
        orgs_domain.iterate_organizations_and_groups()
    ):
        org_tags = await loaders.organization_tags.load(org_name)
        org_groups_attrs = await group_loader.load_many(list(org_groups))
        tag_groups: List[str] = [
            str(group["name"])
            for group in org_groups_attrs
            if get_key_or_fallback(group, "group_status", "project_status")
            == "ACTIVE"
            and group["tags"]
        ]
        success, updated_tags = await update_organization_indicators(
            loaders, org_name, tag_groups
        )
        if success:
            deleted_tags = [
                tag["tag"]
                for tag in org_tags
                if tag["tag"] not in updated_tags
            ]
            await collect(
                tags_domain.delete(org_name, str(tag)) for tag in deleted_tags
            )
        else:
            LOGGER.error(
                "[scheduler]: error updating portfolio indicators",
                extra={"extra": {"organization": org_name}},
            )


async def main() -> None:
    await update_portfolios()
