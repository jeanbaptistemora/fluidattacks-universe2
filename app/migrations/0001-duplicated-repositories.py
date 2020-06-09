"""
This migration is used to delete duplicate entries in the 'repositories' field
of several projects introduced on 2020-05-12

Execution Time:     2020-05-13 17:13 UTC-5
Finalization Time:  2020-05-13 17:14 UTC-5
"""

import rollbar
from typing import (
    cast,
    Dict,
    List,
)

from backend.dal.project import (
    get_all as get_all_projects, TABLE as PROJECT_TABLE
)
from backend.domain.resources import has_repeated_repos
from backend.typing import (
    Historic as HistoricType,
    Resource as ResourceType,
)


def get_unique_repos(repos: List[ResourceType]) -> List[ResourceType]:
    unique_repos_names = []
    unique_repos: List[ResourceType] = []
    for repo in repos:
        if repo['urlRepo'] not in unique_repos_names:
            unique_repos_names.append(repo['urlRepo'])
            unique_repos.append(repo)
        else:
          existing_repo_index = unique_repos_names.index(repo['urlRepo'])
          existing_repo = unique_repos[existing_repo_index]
          existing_repo_historic: HistoricType = existing_repo['historic_state']
          repo_historic: HistoricType = repo['historic_state']
          if repo_historic[-1]['date'] > existing_repo_historic[-1]['date']:
            unique_repos[existing_repo_index] = repo
    return unique_repos


def remove_duplicated_repos() -> None:
    projects = get_all_projects()
    for project in projects:
        try:
            if has_repeated_repos(cast(str, project['project_name']), []):
                rollbar.report_message(
                    'Migration 0001: Processing project {}...'.format(project['project_name']),
                    level='debug')
                repos: List[ResourceType] = get_unique_repos(
                    cast(List[ResourceType], project['repositories']))
                response = PROJECT_TABLE.update_item(
                    Key={'project_name': project['project_name']},
                    UpdateExpression='SET #attrName = :val1',
                    ExpressionAttributeNames={'#attrName': 'repositories'},
                    ExpressionAttributeValues={':val1': repos}
                )
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    rollbar.report_message(
                        'Migration 0001: Duplicate repositories successfully erased from project {}'.format(project['project_name']),
                        level='debug')
                else:
                    rollbar.report_message(
                        'Migration 0001: There was an error erasing duplicates from project {}'.format(project['project_name']),
                        level='debug')
        except KeyError:
            rollbar.report_message(
                'Migration 0001: Project {} errored during analysis of duplicates'.format(project['project_name']),
                level='debug')


if  __name__ == '__main__':
    rollbar.report_message(
        'Starting migration 0001 to delete duplicated repositories', level='debug')
    remove_duplicated_repos()
