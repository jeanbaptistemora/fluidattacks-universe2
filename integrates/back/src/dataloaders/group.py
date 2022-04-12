from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Group as GroupType,
)
from db_model.groups.types import (
    Group,
    GroupState,
    GroupUnreliableIndicators,
)
from dynamodb.types import (
    Item,
)
from groups import (
    domain as groups_domain,
)
from newutils.groups import (
    format_group,
    format_group_historic_state,
    format_group_unreliable_indicators,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    cast,
    Optional,
    Union,
)


async def _batch_load_fn(
    group_names: list[str], parent_org_id: Optional[list[str]]
) -> list[GroupType]:
    groups: dict[str, GroupType] = {}
    groups_by_names: list[GroupType] = await groups_domain.get_many_groups(
        group_names
    )
    organization_ids = (
        parent_org_id
        if parent_org_id
        else await collect(
            [
                orgs_domain.get_id_for_group(group_name)
                for group_name in group_names
            ]
        )
    )

    for index, group in enumerate(groups_by_names):
        group_name = group_names[index].lower()
        status = get_key_or_fallback(
            group, "group_status", "project_status", "DELETED"
        )
        historic_configuration: list[dict[str, str]] = cast(
            list[dict[str, str]], group.get("historic_configuration", [{}])
        )
        has_asm = status == "ACTIVE"
        has_machine: bool = get_key_or_fallback(
            historic_configuration[-1], "has_machine", "has_skims", False
        )
        has_squad: bool = get_key_or_fallback(
            historic_configuration[-1], "has_squad", "has_drills", False
        )

        historic_deletion: list[dict[str, str]] = cast(
            list[dict[str, str]], group.get("historic_deletion", [{}])
        )
        organization_id = organization_ids[index]

        groups[group_name] = dict(
            business_id=group.get("business_id", None),
            business_name=group.get("business_name", None),
            created_date=historic_configuration[0].get("date"),
            closed_vulnerabilities=group.get("closed_vulnerabilities", 0),
            deletion_date=(
                historic_deletion[-1].get("deletion_date")
                if "historic_deletion" in group
                else None
            ),
            description=group.get("description", ""),
            disambiguation=group.get("disambiguation", ""),
            files=group.get("files", []),
            group_context=group.get("group_context", ""),
            language=group.get("language", "en"),
            last_closing_vuln=group.get("last_closing_date", 0),
            last_closing_vuln_finding=group.get("last_closing_vuln_finding"),
            max_open_severity=group.get("max_open_severity", 0),
            max_open_severity_finding=group.get("max_open_severity_finding"),
            mean_remediate_critical_severity=group.get(
                "mean_remediate_critical_severity", 0
            ),
            mean_remediate_high_severity=group.get(
                "mean_remediate_high_severity", 0
            ),
            mean_remediate_low_severity=group.get(
                "mean_remediate_low_severity", 0
            ),
            mean_remediate_medium_severity=group.get(
                "mean_remediate_medium_severity", 0
            ),
            mean_remediate=group.get("mean_remediate", 0),
            name=group_name,
            open_findings=group.get("open_findings", 0),
            open_vulnerabilities=group.get("open_vulnerabilities", 0),
            organization=organization_id,
            project_status=status,
            remediated_over_time=group.get("remediated_over_time", []),
            remediated_over_time_month=group.get(
                "remediated_over_time_month", []
            ),
            remediated_over_time_year=group.get(
                "remediated_over_time_year", []
            ),
            exposed_over_time_cvssf=group.get("exposed_over_time_cvssf", []),
            exposed_over_time_month_cvssf=group.get(
                "exposed_over_time_month_cvssf", []
            ),
            exposed_over_time_year_cvssf=group.get(
                "exposed_over_time_year_cvssf", []
            ),
            remediated_over_time_30=group.get("remediated_over_time_30", []),
            remediated_over_time_90=group.get("remediated_over_time_90", []),
            remediated_over_time_cvssf=group.get(
                "remediated_over_time_cvssf", []
            ),
            remediated_over_time_month_cvssf=group.get(
                "remediated_over_time_month_cvssf", []
            ),
            remediated_over_time_year_cvssf=group.get(
                "remediated_over_time_year_cvssf", []
            ),
            remediated_over_time_cvssf_30=group.get(
                "remediated_over_time_cvssf_30", []
            ),
            remediated_over_time_cvssf_90=group.get(
                "remediated_over_time_cvssf_90", []
            ),
            service=historic_configuration[-1].get("service"),
            subscription=historic_configuration[-1].get("type", None),
            tier=historic_configuration[-1].get("tier", None),
            tags=group.get("tag", []),
            total_treatment=group.get("total_treatment", {}),
            user_deletion=(
                historic_deletion[-1].get("user")
                if "historic_deletion" in group
                else None
            ),
            # Compatibility with old API
            has_squad=has_squad,
            has_drills=has_squad,
            has_machine=has_machine,
            has_skims=has_machine,
            has_asm=has_asm,
            has_integrates=has_asm,
            # Forces related
            has_forces=historic_configuration[-1].get("has_forces", False),
            agent_token=group.get("agent_token", None),
        )
    return [groups.get(group_name, {}) for group_name in group_names]


class GroupLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Union[list[str], list[tuple[str, str]]]
    ) -> list[GroupType]:

        groups_names = (
            list(map(str, group_names))
            if isinstance(group_names[0], str)
            else [group_name[0] for group_name in group_names]
        )
        parent_org_id: Optional[list[str]] = (
            None
            if isinstance(group_names[0], str)
            else [group_name[1] for group_name in group_names]
        )

        return await _batch_load_fn(groups_names, parent_org_id)


class GroupTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, groups_info: Union[tuple[str, ...], tuple[tuple[str, str], ...]]
    ) -> tuple[Group, ...]:
        if isinstance(groups_info[0], str):
            # Given info is tuple[group_name, ...]
            groups_names: tuple[str, ...] = tuple(
                str(group_name) for group_name in groups_info
            )
            organizations_names = await collect(
                orgs_domain.get_name_for_group(str(group_name))
                for group_name in groups_info
            )
        else:
            # Given info is tuple[tuple[group_name, organization_name], ...]
            groups_names = tuple(group_info[0] for group_info in groups_info)
            organizations_names = tuple(
                group_info[1] for group_info in groups_info
            )

        groups_items: list[Item] = await groups_domain.get_many_groups(
            list(groups_names)
        )
        return tuple(
            format_group(item=group, organization_name=organization)
            for group, organization in zip(groups_items, organizations_names)
        )


class GroupIndicatorsTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: tuple[str, ...]
    ) -> tuple[GroupUnreliableIndicators, ...]:
        groups_items: list[Item] = await groups_domain.get_many_groups(
            list(group_names)
        )
        return tuple(
            format_group_unreliable_indicators(item=item)
            for item in groups_items
        )


class GroupHistoricStateTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: tuple[str, ...]
    ) -> tuple[tuple[GroupState, ...], ...]:
        groups_items: list[Item] = await groups_domain.get_many_groups(
            list(group_names)
        )
        return tuple(
            format_group_historic_state(item=item) for item in groups_items
        )
