""" Scheduler de ejecucion de tareas asincronicas de FLUIDIntegrates """

# pylint: disable=E0402
from .dao import integrates_dao
from .models import FormstackAPI
from .mailer import Mailer


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
                if delta == 1:
                    reason = str(delta) + ' nuevo hallazgo'
                else:
                    reason = str(delta) + ' nuevos hallazgos'
            else:
                reason = 'un cambio en los hallazgos'
            recipients = integrates_dao.get_project_users(project)
            print(recipients)
            # Send email
            to = ['engineering@fluid.la', 'projects@fluid.la']
            send_mail = Mailer()
            send_mail.send_new_finding(project[0], to, reason)
            send_mail.close()
            integrates_dao.update_findings_amount(project[0], new_findings)
