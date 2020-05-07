from collections import defaultdict
from typing import Dict, List, Union, cast
from decimal import Decimal
from backend.dal import tag as tag_dal
from backend.domain import finding as finding_domain, project as project_domain


def update_organization_indicators(company: str,
                                   projects: List[Dict[str, str]]) -> bool:
    success = []
    company_projects = \
        [project for project in projects
         if company in
         [proj_company.lower() for proj_company in project.get('companies', [])]]
    tags_dict: Dict[str, List[Dict[str, Union[str, float]]]] = defaultdict(list)
    for project in company_projects:
        findings = finding_domain.get_findings(
            finding_domain.filter_deleted_findings(
                project_domain.list_findings(project.get('project_name', ''))))
        project_data: Dict[str, Union[str, float]] = cast(
            Dict[str, Union[str, float]],
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
        project_data['name'] = project.get('project_name', '')
        for tag in project.get('tag', []):
            tags_dict[tag].append(project_data)
    for tag in tags_dict:
        tag_info: Dict[str, Union[List[str], Decimal]] = {
            'max_open_severity': max(
                [Decimal(project.get('max_open_severity', 0))
                 for project in tags_dict[tag]]),
            'max_severity': max(
                [Decimal(project.get('max_severity', 0))
                 for project in tags_dict[tag]]),
            'last_closing_date': min(
                [Decimal(project.get('last_closing_date', float('inf')))
                 for project in tags_dict[tag]]),
            'mean_remediate': Decimal(sum(
                [float(project.get('mean_remediate', 0))
                 for project in tags_dict[tag]]) / len(tags_dict[tag])
            ).quantize(Decimal('0.1')),
            'mean_remediate_critical_severity': Decimal(sum(
                [float(project.get('mean_remediate_critical_severity', 0))
                 for project in tags_dict[tag]]) / len(tags_dict[tag])
            ).quantize(Decimal('0.1')),
            'mean_remediate_high_severity': Decimal(sum(
                [float(project.get('mean_remediate_high_severity', 0))
                 for project in tags_dict[tag]]) / len(tags_dict[tag])
            ).quantize(Decimal('0.1')),
            'mean_remediate_low_severity': Decimal(sum(
                [float(project.get('mean_remediate_low_severity', 0))
                 for project in tags_dict[tag]]) / len(tags_dict[tag])
            ).quantize(Decimal('0.1')),
            'mean_remediate_medium_severity': Decimal(sum(
                [float(project.get('mean_remediate_medium_severity', 0))
                 for project in tags_dict[tag]]) / len(tags_dict[tag])
            ).quantize(Decimal('0.1')),
            'projects': [str(project.get('name', '')) for project in tags_dict[tag]],
        }
        success.append(tag_dal.update(company, tag, tag_info))
    return all(success)


def get_attributes(organization: str, tag: str,
                   attributes: List[str]) -> Dict[str, Union[List[str], str]]:
    return tag_dal.get_attributes(organization, tag, attributes)


def is_tag_allowed(user_projects: List[Dict[str, Union[str, List[str]]]],
                   organization: str, tag: str) -> bool:
    all_projects_tag = get_attributes(organization, tag, ['projects'])
    user_projects_tag = \
        [str(project.get('project_name', '')).lower() for project in user_projects
         if tag in [p_tag.lower() for p_tag in project.get('tag', [])]]
    return all(project.lower() in user_projects_tag
               for project in all_projects_tag.get('projects', []))


def filter_allowed_tags(organization: str, user_projects: List[str]) -> List[str]:
    tags = []
    projects = [project_domain.get_attributes(project, ['tag', 'project_name'])
                for project in user_projects]
    all_tags = {tag.lower() for project in projects
                for tag in project.get('tag', [])}
    tags = [tag for tag in all_tags
            if is_tag_allowed(projects, organization, tag)]
    return tags
