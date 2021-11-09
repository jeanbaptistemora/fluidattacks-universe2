from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Group as GroupType,
)
from groups import (
    domain as groups_domain,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    cast,
    Dict,
    List,
)


async def _batch_load_fn(group_names: List[str]) -> List[GroupType]:
    groups: Dict[str, GroupType] = {}
    groups_by_names: List[GroupType] = await groups_domain.get_many_groups(
        group_names
    )
    organization_ids = await collect(
        [
            orgs_domain.get_id_for_group(group_name)
            for group_name in group_names
        ]
    )

    for index, group in enumerate(groups_by_names):
        group_name = group_names[index].lower()
        status = get_key_or_fallback(
            group, "group_status", "project_status", "FINISHED"
        )
        historic_configuration: List[Dict[str, str]] = cast(
            List[Dict[str, str]], group.get("historic_configuration", [{}])
        )
        has_asm = status == "ACTIVE"
        has_machine: bool = get_key_or_fallback(
            historic_configuration[-1], "has_machine", "has_skims", False
        )
        has_squad: bool = get_key_or_fallback(
            historic_configuration[-1], "has_squad", "has_drills", False
        )
        subscription = historic_configuration[-1].get("type", None)

        historic_deletion: List[Dict[str, str]] = cast(
            List[Dict[str, str]], group.get("historic_deletion", [{}])
        )
        organization_id = organization_ids[index]

        groups[group_name] = dict(
            closed_vulnerabilities=group.get("closed_vulnerabilities", 0),
            dast_access=group.get("dast_access", ""),
            deletion_date=(
                historic_deletion[-1].get("deletion_date", "")
                if "historic_deletion" in group
                else ""
            ),
            description=group.get("description", ""),
            disambiguation=group.get("disambiguation", ""),
            files=group.get("files", []),
            has_forces=historic_configuration[-1].get("has_forces", False),
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
            mobile_access=group.get("mobile_access", ""),
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
            sast_access=group.get("sast_access", ""),
            service=historic_configuration[-1].get("service"),
            subscription=subscription,
            tags=group.get("tag", []),
            total_treatment=group.get("total_treatment", {}),
            user_deletion=(
                historic_deletion[-1].get("user", "")
                if "historic_deletion" in group
                else ""
            ),
            # Compatibility with old API
            has_squad=has_squad,
            has_drills=has_squad,
            has_machine=has_machine,
            has_skims=has_machine,
            has_asm=has_asm,
            has_integrates=has_asm,
        )
    return [groups.get(group_name, {}) for group_name in group_names]


class GroupLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(self, group_names: List[str]) -> List[GroupType]:
        return await _batch_load_fn(group_names)
