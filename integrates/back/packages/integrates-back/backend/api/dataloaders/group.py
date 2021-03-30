# Standard libraries
from typing import (
    cast,
    Dict,
    List,
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend.domain import project as group_domain
from backend.typing import Project as GroupType
from organizations import domain as orgs_domain


async def _batch_load_fn(group_names: List[str]) -> List[GroupType]:
    groups: Dict[str, GroupType] = {}
    groups_by_names: List[GroupType] = \
        await group_domain.get_many_groups(group_names)
    organization_ids = await collect([
        orgs_domain.get_id_for_group(group_name)
        for group_name in group_names
    ])

    for index, group in enumerate(groups_by_names):
        group_name = group_names[index].lower()
        status = group.get('project_status', 'FINISHED')
        historic_configuration: List[Dict[str, str]] = cast(
            List[Dict[str, str]],
            group.get('historic_configuration', [{}])
        )
        has_drills = historic_configuration[-1].get('has_drills', False)
        has_forces = historic_configuration[-1].get('has_forces', False)
        has_integrates = status == 'ACTIVE'
        subscription = historic_configuration[-1].get('type', None)

        historic_deletion: List[Dict[str, str]] = cast(
            List[Dict[str, str]],
            group.get('historic_deletion', [{}])
        )
        organization_id = organization_ids[index]

        groups[group_name] = dict(
            closed_vulnerabilities=group.get('closed_vulnerabilities', 0),
            deletion_date=(
                historic_deletion[-1].get('deletion_date', '')
                if 'historic_deletion' in group else ''
            ),
            description=group.get('description', ''),
            files=group.get('files', []),
            has_drills=has_drills,
            has_forces=has_forces,
            has_integrates=has_integrates,
            language=group.get('language', 'en'),
            last_closing_vuln=group.get('last_closing_date', 0),
            last_closing_vuln_finding=group.get(
                'last_closing_vuln_finding'
            ),
            max_open_severity=group.get('max_open_severity', 0),
            max_open_severity_finding=group.get(
                'max_open_severity_finding'
            ),
            mean_remediate_critical_severity=group.get(
                'mean_remediate_critical_severity',
                0
            ),
            mean_remediate_high_severity=group.get(
                'mean_remediate_high_severity',
                0
            ),
            mean_remediate_low_severity=group.get(
                'mean_remediate_low_severity',
                0
            ),
            mean_remediate_medium_severity=group.get(
                'mean_remediate_medium_severity',
                0
            ),
            mean_remediate=group.get('mean_remediate', 0),
            name=group_name,
            open_findings=group.get('open_findings', 0),
            open_vulnerabilities=group.get('open_vulnerabilities', 0),
            organization=organization_id,
            project_status=status,
            remediated_over_time=group.get('remediated_over_time', []),
            remediated_over_time_30=group.get('remediated_over_time_30', []),
            remediated_over_time_90=group.get('remediated_over_time_90', []),
            subscription=subscription,
            tags=group.get('tag', []),
            total_treatment=group.get('total_treatment', {}),
            user_deletion=(
                historic_deletion[-1].get('user', '')
                if 'historic_deletion' in group else ''
            )
        )

    return [
        groups.get(group_name, {})
        for group_name in group_names
    ]


# pylint: disable=too-few-public-methods
class GroupLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""

    # pylint: disable=method-hidden
    async def batch_load_fn(self, group_names: List[str]) -> List[GroupType]:
        return await _batch_load_fn(group_names)
