import asyncio
from collections import defaultdict
from typing import Dict, List, Union, cast
from decimal import Decimal
from asgiref.sync import sync_to_async
from backend import util
from backend.dal import tag as tag_dal
from backend.domain import finding as finding_domain, project as project_domain


async def update_organization_indicators(company: str,
                                         projects: List[Dict[str, str]]) -> bool:
    success = []
    company_projects = \
        [project for project in projects
         if company in
         [proj_company.lower() for proj_company in project.get('companies', [])]]
    tags_dict: Dict[str, List[Dict[str, Union[str, float]]]] = defaultdict(list)
    finding_lists = await asyncio.gather(*[
        sync_to_async(project_domain.list_findings)(
            project.get('project_name', '')
        )
        for project in company_projects
    ])
    project_findings = await asyncio.gather(*[
        finding_domain.get_findings_async(
            finding_list
        )
        for finding_list in finding_lists
    ])
    project_datas = await asyncio.gather(*[
        sync_to_async(project_domain.get_attributes)(
            project.get('project_name', ''), [
                'max_open_severity',
                'mean_remediate',
                'mean_remediate_critical_severity',
                'mean_remediate_high_severity',
                'mean_remediate_low_severity',
                'mean_remediate_medium_severity',
                'last_closing_date',
            ]
        )
        for project in company_projects
    ])
    max_severities = [
        max(
            [cast(float, finding.get('severityCvss', 0)) for finding in findings]
        ) if findings else 0
        for findings in project_findings
    ]
    for index, project in enumerate(company_projects):
        project_datas[index]['max_severity'] = max_severities[index]
        project_datas[index]['name'] = project.get('project_name', '')
        for tag in project.get('tag', []):
            tags_dict[tag].append(project_datas[index])
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
        response = await sync_to_async(tag_dal.update)(company, tag, tag_info)
        if response:
            util.invalidate_cache(tag)
        success.append(response)
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


async def filter_allowed_tags(organization: str, user_projects: List[str]) -> List[str]:
    projects = await asyncio.gather(*[
        sync_to_async(project_domain.get_attributes)(
            project, ['tag', 'project_name']
        )
        for project in user_projects
    ])
    all_tags = {tag.lower() for project in projects
                for tag in project.get('tag', [])}
    are_tags_allowed = await asyncio.gather(*[
        sync_to_async(is_tag_allowed)(
            projects, organization, tag
        )
        for tag in all_tags
    ])
    tags = [tag for tag in all_tags
            if are_tags_allowed.pop(0)]
    return tags
