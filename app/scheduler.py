""" Scheduler de ejecucion de tareas asincronicas de FLUIDIntegrates """

# pylint: disable=E0402
from .dao import integrates_dao
from .models import FormstackAPI
from .mailer import send_mail_new_finding


def get_new_findings():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        finding_requests = api.get_findings(project)["submissions"]
        new_findings = len(finding_requests)
        cur_findings = integrates_dao.get_findings_amount(project)
        if new_findings != cur_findings:
            if new_findings > cur_findings:
                delta = new_findings - cur_findings
            else:
                delta = 0
            recipients = integrates_dao.get_project_users(project)
            print(recipients)
            # Send email
            to = ['engineering@fluid.la', 'projects@fluid.la']
            context = {
                'cantidad': str(delta),
                'proyecto': project[0],
            }
            send_mail_new_finding(to, context)
            integrates_dao.update_findings_amount(project[0], new_findings)
