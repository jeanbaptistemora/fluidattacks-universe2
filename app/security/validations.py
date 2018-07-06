# pylint: disable=E0402
from ..dao import integrates_dao
from ..api.formstack import FormstackAPI

def get_projects_map_by_user(email):
    session_findings = {}
    projects = integrates_dao.get_projects_by_user(email)
    if projects:
        for project in projects:
            session_findings[project[0]]=get_submissions_by_project(project[0])
    return session_findings


def get_submissions_by_project(project):
    api = FormstackAPI()
    ids = []
    for finding in api.get_findings(project)['submissions']:
        ids.append(finding['id'])
    return ids
