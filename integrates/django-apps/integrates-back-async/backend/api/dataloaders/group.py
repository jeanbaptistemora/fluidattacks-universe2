# Standard
from typing import cast, Dict, List, Set

# Third party
from aiodataloader import DataLoader

# Local
from backend.domain import project as group_domain
from backend.typing import Project as Group


def format_group(group: Group) -> Group:
    """Returns the data in the format expected by default resolvers"""

    historic_configuration: List[Dict[str, str]] = cast(
        List[Dict[str, str]],
        group['historic_configuration']
    )
    historic_deletion: List[Dict[str, str]] = cast(
        List[Dict[str, str]],
        group.get('historic_deletion', [])
    )

    return {
        'closed_vulnerabilities': group.get('closed_vulnerabilities', 0),
        'deletion_date': (
            historic_deletion[-1].get('deletion_date', '')
            if 'historic_deletion' in group else ''
        ),
        'description': group.get('description', ''),
        'environments': group.get('environments', []),
        'files': group.get('files', []),
        'has_drills': historic_configuration[-1]['has_drills'],
        'has_forces': historic_configuration[-1]['has_forces'],
        'has_integrates': group['project_status'] == 'ACTIVE',
        'last_closing_vuln': group.get('last_closing_date', 0),
        'last_closing_vuln_finding': group.get(
            'last_closing_vuln_finding'
        ),
        'max_open_severity': group.get('max_open_severity', 0),
        'max_open_severity_finding': group.get(
            'max_open_severity_finding'
        ),
        'mean_remediate_critical_severity': group.get(
            'mean_remediate_critical_severity',
            0
        ),
        'mean_remediate_high_severity': group.get(
            'mean_remediate_high_severity',
            0
        ),
        'mean_remediate_low_severity': group.get(
            'mean_remediate_low_severity',
            0
        ),
        'mean_remediate_medium_severity': group.get(
            'mean_remediate_medium_severity',
            0
        ),
        'mean_remediate': group.get('mean_remediate', 0),
        'name': group['project_name'],
        'open_findings': group.get('open_findings', 0),
        'open_vulnerabilities': group.get('open_vulnerabilities', 0),
        'repositories': group.get('repositories', []),
        'subscription': historic_configuration[-1]['type'],
        'tags': group.get('tag', []),
        'total_treatment': group.get('total_treatment', {}),
        'user_deletion': (
            historic_deletion[-1].get('user', '')
            if 'historic_deletion' in group else ''
        )
    }


# pylint: disable=too-few-public-methods
class GroupLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(self, group_names: List[str]) -> List[Group]:
        groups: List[Group] = await group_domain.get_many_groups(group_names)
        allowed_status: Set[str] = {'ACTIVE', 'PENDING_DELETION'}

        return [
            format_group(group)
            for group in groups
            if group['project_status'] in allowed_status
        ]
