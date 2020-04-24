from collections import defaultdict
from typing import Dict, List, cast
from backend.dal import tag as tag_dal
from backend.domain import finding as finding_domain, project as project_domain


def update_organization_indicators(company: str,
                                   projects: List[Dict[str, str]]) -> bool:
    success = []
    company_projects = \
        [project for project in projects
         if company in
         [proj_company.lower() for proj_company in project.get('companies', [])]]
    tags_dict: Dict[str, List[Dict[str, float]]] = defaultdict(list)
    for project in company_projects:
        findings = finding_domain.get_findings(
            finding_domain.filter_deleted_findings(
                project_domain.list_findings(project.get('project_name', ''))))
        project_data: Dict[str, float] = cast(
            Dict[str, float],
            project_domain.get_attributes(project.get('project_name', ''), [
                'max_open_severity',
                'mean_remediate',
                'mean_remediate_critical_severity',
                'mean_remediate_high_severity',
                'mean_remediate_low_severity',
                'mean_remediate_medium_severity',
                'last_closing_date',
            ])
        )
        max_severity: float = max(
            [cast(float, finding.get('severityCvss', 0)) for finding in findings]
        ) if findings else 0
        project_data['max_severity'] = max_severity
        for tag in project.get('tag', []):
            tags_dict[tag].append(project_data)
    for tag in tags_dict:
        tag_info = {
            'max_open_severity': max(
                [project.get('max_open_severity', 0) for project in tags_dict[tag]]),
            'max_severity': max(
                [project.get('max_severity', 0) for project in tags_dict[tag]]),
            'last_closing_date': min(
                [project.get('last_closing_date', float('inf'))
                 for project in tags_dict[tag]]),
            'mean_remediate': sum(
                [project.get('mean_remediate', 0)
                 for project in tags_dict[tag]]) / len(tags_dict[tag]),
            'mean_remediate_critical_severity': sum(
                [project.get('mean_remediate_critical_severity', 0)
                 for project in tags_dict[tag]]) / len(tags_dict[tag]),
            'mean_remediate_high_severity': sum(
                [project.get('mean_remediate_high_severity', 0)
                 for project in tags_dict[tag]]) / len(tags_dict[tag]),
            'mean_remediate_low_severity': sum(
                [project.get('mean_remediate_low_severity', 0)
                 for project in tags_dict[tag]]) / len(tags_dict[tag]),
            'mean_remediate_medium_severity': sum(
                [project.get('mean_remediate_medium_severity', 0)
                 for project in tags_dict[tag]]) / len(tags_dict[tag]),
        }
        success.append(tag_dal.update(company, tag, tag_info))
    return all(success)
