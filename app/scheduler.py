""" Scheduler de ejecucion de tareas asincronicas de FLUIDIntegrates """

# pylint: disable=E0402
from .dao import integrates_dao
from .models import FormstackAPI
from .mailer import send_mail_new_finding, send_mail_change_finding


def get_new_findings():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        # Send email parameters
        recipients = integrates_dao.get_project_users(project)
        to = [ x[0] for x in recipients ]
        to.append('engineering@fluid.la')
        to.append('projects@fluid.la')
        finding_requests = api.get_findings(project)["submissions"]
        new_findings = len(finding_requests)
        cur_findings = integrates_dao.get_findings_amount(project)
        if new_findings != cur_findings:
            if new_findings > cur_findings:
                delta = new_findings - cur_findings
                context = {
                    'cantidad': str(delta),
                    'proyecto': project[0].upper(),
                }
                print(to)
                send_mail_new_finding(to, context)
            else:
                context = {
                    'proyecto': project[0].upper(),
                }
                print(to)
                send_mail_change_finding(to, context)
            integrates_dao.update_findings_amount(project[0], new_findings)
