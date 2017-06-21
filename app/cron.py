""" Scheduler de ejecucion de tareas asincronicas de FLUIDIntegrates """

# pylint: disable=E0402
from .dao import integrates_dao
from .models import FormstackAPI


def get_new_findings():
    projects = integrates_dao.get_registered_projects()
    API = FormstackAPI()
    for project in projects:
        finding_requests = API.get_findings(project)["submissions"]
        new_findings = len(finding_requests)
        cur_findings = integrates_dao.get_findings_amount(project)
        if new_findings != cur_findings:
            recipients = integrates_dao.get_project_users(project)
            print (recipients)
            # Send email
            integrates_dao.update_findings_amount(project, new_findings)
