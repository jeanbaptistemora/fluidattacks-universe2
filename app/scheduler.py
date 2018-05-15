""" Scheduler de ejecucion de tareas asincronicas de FLUIDIntegrates """

# pylint: disable=E0402
import rollbar
from .dao import integrates_dao
from .api.formstack import FormstackAPI
from .mailer import send_mail_new_vulnerabilities, send_mail_new_remediated, \
                    send_mail_age_finding, send_mail_age_kb_finding
from . import views
from datetime import datetime, timedelta

def get_new_vulnerabilities():
    """ Envio de correo resumen con los hallazgos de un proyecto """
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        try:
            old_findings = integrates_dao.get_vulns_by_project_dynamo(project[0].lower())
            finding_requests = api.get_findings(project)["submissions"]
            if len(old_findings) != len(finding_requests):
                delta = abs(len(old_findings) - len(finding_requests))
                for finding in finding_requests[-delta:]:
                    integrates_dao.add_or_update_vulns_dynamo(project[0].lower(),int(finding['id']), 0)
                old_findings = integrates_dao.get_vulns_by_project_dynamo(project[0].lower())
            context = {'findings': list(), 'findings_working_on': list()}
            delta_total = 0
            for finding in finding_requests:
                row = integrates_dao.get_vulns_by_id_dynamo(project[0].lower(), int(finding['id']))
                act_finding = views.finding_vulnerabilities(str(finding['id']))
                if act_finding["edad"] != "-" and act_finding["estado"] != "Cerrado" and "tratamiento" in act_finding:
                    if  act_finding["tratamiento"] == "Nuevo":
                        context['findings_working_on'].append({'hallazgo_pendiente': (act_finding['hallazgo'] + ' -' + act_finding["edad"] +' day(s)-'), \
                        'url_hallazgo': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/' + str(finding['id'] + \
                            '/description')})
                if row != []:
                    delta = int(act_finding['cardinalidad'])-int(row[0]['vuln_hoy'])
                    if int(act_finding['cardinalidad']) > int(row[0]['vuln_hoy']):
                        finding_text = act_finding['hallazgo'] + ' (+' + str(delta) +')'
                        context['findings'].append({'nombre_hallazgo': finding_text , \
                        'url_vuln': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/' + str(finding['id'] + \
                            '/description')})
                        delta_total = delta_total + abs(delta)
                        integrates_dao.add_or_update_vulns_dynamo(str(project[0].lower()),int(finding['id']), int(act_finding['cardinalidad']))
                    elif int(act_finding['cardinalidad']) < int(row[0]['vuln_hoy']):
                        finding_text = act_finding['hallazgo'] + ' (' + str(delta) +')'
                        context['findings'].append({'nombre_hallazgo': finding_text , \
                        'url_vuln': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/' + str(finding['id'] + \
                            '/description')})
                        delta_total = delta_total + abs(delta)
                        integrates_dao.add_or_update_vulns_dynamo(str(project[0].lower()),int(finding['id']), int(act_finding['cardinalidad']))
            if delta_total != 0:
                context['proyecto'] = project[0].upper()
                context['url_proyecto'] = 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/indicators'
                recipients = integrates_dao.get_project_users(project)
                to = [x[0] for x in recipients if x[1] == 1]
                to.append('continuous@fluidattacks.com')
                to.append('projects@fluidattacks.com')
                send_mail_new_vulnerabilities(to, context)
        except (TypeError, KeyError):
            rollbar.report_message('Error: An error ocurred sending age notification email', 'error')

def get_remediated_findings():
    """ Envio de correo resumen con los hallazgos pendientes de verificar """
    findings = integrates_dao.get_remediated_allfindings_dynamo(True)
    if findings != []:
        to = ['continuous@fluidattacks.com']
        context = {'findings': list()}
        cont = 0
        for finding in findings:
            context['findings'].append({'finding_name': finding['finding_name'], 'finding_url': \
                'https://fluidattacks.com/integrates/dashboard#!/project/'+ finding['project'].lower() + '/' + \
                str(finding['finding_id']) + '/description', 'project': finding['project'].upper()})
            cont += 1
        context['total'] = cont
        send_mail_new_remediated(to, context)

def get_age_notifications():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        recipients = integrates_dao.get_project_users(project)
        to = [x[0] for x in recipients if x[1] == 1]
        to.append('continuous@fluidattacks.com')
        finding_requests = api.get_findings(project)["submissions"]
        for finding in finding_requests:
            finding_parsed = views.finding_vulnerabilities(finding["id"])
            if "suscripcion" not in finding_parsed:
                pass
            elif finding_parsed["suscripcion"] == "Continua" and finding_parsed["edad"] != "-":
                age = int(finding_parsed["edad"])
                context = {
                    'project': project[0].upper(),
                    'finding': finding["id"],
                    'finding_name': finding_parsed["hallazgo"],
                    'finding_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                    + '/' + finding["id"] + '/description',
                    'finding_comment': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                    + '/' + finding["id"] + '/comments',
                    'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/indicators'
                    }
                if "kb" in finding_parsed:
                    if "https://fluidattacks.com/web/es/defends" in finding_parsed["kb"]:
                        context["kb"] = finding_parsed["kb"]
                ages = [15, 30, 60, 90, 120, 180, 240]
                if age in ages:
                    context["age"] = age
                    if "kb" in context:
                        send_mail_age_kb_finding(to, context)
                    else:
                        send_mail_age_finding(to, context)

def get_age_weekends_notifications():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        recipients = integrates_dao.get_project_users(project)
        to = [x[0] for x in recipients if x[1] == 1]
        to.append('continuous@fluidattacks.com')
        finding_requests = api.get_findings(project)["submissions"]
        for finding in finding_requests:
            finding_parsed = views.finding_vulnerabilities(finding["id"])
            if "suscripcion" not in finding_parsed:
                pass
            elif finding_parsed["suscripcion"] == "Continua" and finding_parsed["edad"] != "-":
                age = int(finding_parsed["edad"])
                context = {
                    'project': project[0].upper(),
                    'finding': finding["id"],
                    'finding_name': finding_parsed["hallazgo"],
                    'finding_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                    + '/' + finding["id"] + '/description',
                    'finding_comment': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                    + '/' + finding["id"] + '/comments',
                    'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/indicators'
                    }
                if "kb" in finding_parsed:
                    if "https://fluidattacks.com/web/es/defends" in finding_parsed["kb"]:
                        context["kb"] = finding_parsed["kb"]
                ages = [15, 30, 60, 90, 120, 180, 240]
                if age in ages:
                    context["age"] = age
                    if "kb" in context:
                        send_mail_age_kb_finding(to, context)
                    else:
                        send_mail_age_finding(to, context)
                elif (age + 1) in ages:
                    context["age"] = age + 1
                    if "kb" in context:
                        send_mail_age_kb_finding(to, context)
                    else:
                        send_mail_age_finding(to, context)
                elif (age + 2) in ages:
                    context["age"] = age + 2
                    if "kb" in context:
                        send_mail_age_kb_finding(to, context)
                    else:
                        send_mail_age_finding(to, context)

def weekly_report():
    init_date = (datetime.today() - timedelta(days=7)).date()
    final_date =  (datetime.today() - timedelta(days=1)).date()
    registered_users = integrates_dao.all_users_report("FLUID", final_date)
    logged_users = integrates_dao.logging_users_report("FLUID", init_date, final_date)
    integrates_dao.weekly_report_dynamo(str(init_date), str(final_date), registered_users[0][0], logged_users[0][0])


def inactive_users():
    final_date = (datetime.today() - timedelta(days=7))
    inac_users = integrates_dao.all_inactive_users()
    for user in inac_users:
        if user[1] <= final_date:
            integrates_dao.delete_user(user[0])
