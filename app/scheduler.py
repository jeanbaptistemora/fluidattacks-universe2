""" Asynchronous task execution scheduler for FLUIDIntegrates """

# pylint: disable=E0402
import rollbar
from .dao import integrates_dao
from .api.formstack import FormstackAPI
from .mailer import send_mail_new_vulnerabilities, send_mail_new_remediated, \
                    send_mail_age_finding, send_mail_age_kb_finding, \
                    send_mail_new_releases, send_mail_continuous_report
from . import views
from datetime import datetime, timedelta

def get_new_vulnerabilities():
    """ Summary mail send with the findings of a project. """
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        try:
            old_findings = integrates_dao.get_vulns_by_project_dynamo(project[0].lower())
            finding_requests = api.get_findings(project)["submissions"]
            if len(old_findings) != len(finding_requests):
                delta = abs(len(old_findings) - len(finding_requests))
                for finding in finding_requests[-delta:]:
                    act_finding = views.finding_vulnerabilities(str(finding['id']))
                    if ("releaseDate" in act_finding and act_finding['fluidProject'].lower() == project[0].lower()):
                        integrates_dao.add_or_update_vulns_dynamo(project[0].lower(),int(finding['id']), 0)
                old_findings = integrates_dao.get_vulns_by_project_dynamo(project[0].lower())
            context = {'findings': list(), 'findings_working_on': list()}
            delta_total = 0
            for finding in finding_requests:
                row = integrates_dao.get_vulns_by_id_dynamo(project[0].lower(), int(finding['id']))
                act_finding = views.finding_vulnerabilities(str(finding['id']))
                if (("releaseDate" in act_finding) and (act_finding["estado"] != "Cerrado") and
                    (act_finding["edad"] != "-") and ("treatment" in act_finding) and
                            (act_finding['fluidProject'].lower() == project[0].lower())):
                    if  act_finding["treatment"] == "Nuevo":
                        context['findings_working_on'].append({'hallazgo_pendiente': (act_finding['finding'] + ' -' + act_finding["edad"] +' day(s)-'), \
                        'url_hallazgo': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/' + str(finding['id'] + \
                            '/description')})
                if row != []:
                    delta = int(act_finding['openVulnerabilities'])-int(row[0]['vuln_hoy'])
                    if int(act_finding['openVulnerabilities']) > int(row[0]['vuln_hoy']):
                        finding_text = act_finding['finding'] + ' (+' + str(delta) +')'
                        context['findings'].append({'nombre_hallazgo': finding_text , \
                        'url_vuln': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/' + str(finding['id'] + \
                            '/description')})
                        delta_total = delta_total + abs(delta)
                        integrates_dao.add_or_update_vulns_dynamo(str(project[0].lower()),int(finding['id']), int(act_finding['openVulnerabilities']))
                    elif int(act_finding['openVulnerabilities']) < int(row[0]['vuln_hoy']):
                        finding_text = act_finding['finding'] + ' (' + str(delta) +')'
                        context['findings'].append({'nombre_hallazgo': finding_text , \
                        'url_vuln': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/' + str(finding['id'] + \
                            '/description')})
                        delta_total = delta_total + abs(delta)
                        integrates_dao.add_or_update_vulns_dynamo(str(project[0].lower()),int(finding['id']), int(act_finding['openVulnerabilities']))
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
    """ Summary mail send with findings that have not been verified yet. """
    findings = integrates_dao.get_remediated_allfindings_dynamo(True)
    if findings != []:
        try:
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
        except (TypeError, KeyError):
            rollbar.report_message('Error: An error ocurred getting data for remediated email', 'error')

def get_age_notifications():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        try:
            recipients = integrates_dao.get_project_users(project)
            to = [x[0] for x in recipients if x[1] == 1]
            to.append('continuous@fluidattacks.com')
            finding_requests = api.get_findings(project)["submissions"]
            for finding in finding_requests:
                finding_parsed = views.finding_vulnerabilities(finding["id"])
                if ("suscripcion" in finding_parsed and "releaseDate" in finding_parsed and
                        finding_parsed['fluidProject'].lower() == project[0].lower() and
                        finding_parsed["suscripcion"] == "Continua" and finding_parsed["edad"] != "-"):
                    age = int(finding_parsed["edad"])
                    context = {
                        'project': project[0].upper(),
                        'finding': finding["id"],
                        'finding_name': finding_parsed["finding"],
                        'finding_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                        + '/' + finding["id"] + '/description',
                        'finding_comment': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                        + '/' + finding["id"] + '/comments',
                        'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/indicators'
                        }
                    if "kb" in finding_parsed and "https://fluidattacks.com/web/es/defends" in finding_parsed["kb"]:
                        context["kb"] = finding_parsed["kb"]
                    ages = [15, 30, 60, 90, 120, 180, 240]
                    if age in ages:
                        send_mail_age(age, to, context)
        except (TypeError, KeyError):
            rollbar.report_message('Error: An error ocurred getting data for age email', 'error')


def get_age_weekends_notifications():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        try:
            recipients = integrates_dao.get_project_users(project)
            to = [x[0] for x in recipients if x[1] == 1]
            to.append('continuous@fluidattacks.com')
            finding_requests = api.get_findings(project)["submissions"]
            for finding in finding_requests:
                finding_parsed = views.finding_vulnerabilities(finding["id"])
                if ("suscripcion" in finding_parsed and "releaseDate" in finding_parsed and
                        finding_parsed['fluidProject'].lower() == project[0].lower() and
                        finding_parsed["suscripcion"] == "Continua" and finding_parsed["edad"] != "-"):
                    age = int(finding_parsed["edad"])
                    context = {
                        'project': project[0].upper(),
                        'finding': finding["id"],
                        'finding_name': finding_parsed["finding"],
                        'finding_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                        + '/' + finding["id"] + '/description',
                        'finding_comment': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                        + '/' + finding["id"] + '/comments',
                        'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() + '/indicators'
                        }
                    if "kb" in finding_parsed and "https://fluidattacks.com/web/es/defends" in finding_parsed["kb"]:
                        context["kb"] = finding_parsed["kb"]
                    ages = [15, 30, 60, 90, 120, 180, 240]
                    if age in ages:
                        send_mail_age(age, to, context)
                    elif (age + 1) in ages:
                        send_mail_age(age + 1, to, context)
                    elif (age + 2) in ages:
                        send_mail_age(age + 2, to, context)
        except (TypeError, KeyError):
            rollbar.report_message('Error: An error ocurred getting data for age weekends email', 'error')

def send_mail_age(age, to, context):
    context["age"] = age
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

def get_new_releases():
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    context = {'findings': list()}
    cont = 0
    for project in projects:
        try:
            finding_requests = api.get_findings(project)["submissions"]
            for finding in finding_requests:
                finding_parsed = views.finding_vulnerabilities(finding["id"])
                if ("releaseDate" not in finding_parsed and
                        finding_parsed['fluidProject'].lower() == project[0].lower()):
                    context['findings'].append({'finding_name': finding_parsed["finding"], 'finding_url': \
                        'https://fluidattacks.com/integrates/dashboard#!/project/'+ project[0].lower() + '/' + \
                        str(finding["id"]) + '/description', 'project': project[0].upper()})
                    cont += 1
        except (TypeError, KeyError):
            rollbar.report_message('Error: An error ocurred getting data for new drafts email', 'error')
    if cont > 0:
        context['total'] = cont
        to = ["engineering@fluidattacks.com"]
        send_mail_new_releases(to, context)

def continuous_report():
    to = ['jrestrepo@fluidattacks.com', 'ralvarez@fluidattacks.com', \
          'oparada@fluidattacks.com', 'projects@fluidattacks.com', 'relations@fluidattacks.com'  ]
    headers = ['#','Project','Lines','Inputs','Fixed vulns','Max severity', 'Open Events']
    context = {'projects':list(), 'headers': headers, 'date_now': str(datetime.now().date())}
    index = 0
    for x in integrates_dao.get_continuous_info():
        index += 1
        project_url = "https://fluidattacks.com/integrates/dashboard#!/project/" + \
                      x['project'].lower() + "/indicators"
        indicators = views.calculate_indicators(x['project'])
        context['projects'].append({'project_url': str(project_url), \
                                    'index': index, \
                                    'project_name': str(x['project']), \
                                    'lines': str(x['lines']), \
                                    'fields': str(x['fields']), \
                                    'fixed_vuln': (str(indicators[2]) + "%"), \
                                    'cssv': indicators[1], \
                                    'events': indicators[0]
                                     })
    send_mail_continuous_report(to, context)
