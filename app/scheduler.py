""" Scheduler de ejecucion de tareas asincronicas de FLUIDIntegrates """

# pylint: disable=E0402
from .dao import integrates_dao
from .api.formstack import FormstackAPI
from .mailer import send_mail_new_vulnerabilities, send_mail_new_remediated, \
                    send_mail_age_finding, send_mail_age_kb_finding
from . import views

def get_new_vulnerabilities():
    """ Envio de correo resumen con los hallazgos de un proyecto """
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        old_findings = integrates_dao.get_vulns_by_project_dynamo(project[0].lower())
        finding_requests = api.get_findings(project)["submissions"]
        if len(old_findings) != len(finding_requests):
            delta = abs(len(old_findings) - len(finding_requests))
            for finding in finding_requests[-delta:]:
                integrates_dao.add_or_update_vulns_dynamo(project[0].lower(),int(finding['id']), 0)
            old_findings = integrates_dao.get_vulns_by_project_dynamo(project[0].lower())
        context = {'findings': list()}
        delta_total = 0
        for row in old_findings:
            act_finding = views.finding_vulnerabilities(str(row['unique_id']))
            delta = int(act_finding['cardinalidad'])-int(row['vuln_hoy'])
            if int(act_finding['cardinalidad']) > int(row['vuln_hoy']):
                finding_text = act_finding['hallazgo'] + '(+' + str(delta) +')'
                context['findings'].append({'nombre_hallazgo': finding_text })
                delta_total = delta_total + abs(delta)
                integrates_dao.add_or_update_vulns_dynamo(project[0].lower(),row['unique_id'], int(act_finding['cardinalidad']))
            elif int(act_finding['cardinalidad']) < int(row['vuln_hoy']):
                finding_text = act_finding['hallazgo'] + '(' + str(delta) +')'
                context['findings'].append({'nombre_hallazgo': finding_text })
                delta_total = delta_total + abs(delta)
                integrates_dao.add_or_update_vulns_dynamo(project[0].lower(),row['unique_id'], int(act_finding['cardinalidad']))
        if delta_total !=0:
            context['proyecto'] = project[0].upper()
            context['url_proyecto'] = 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower()
            recipients = integrates_dao.get_project_users(project)
            to = [x[0] for x in recipients]
            to.append('engineering@fluidattacks.com')
            to.append('projects@fluidattacks.com')
            send_mail_new_vulnerabilities(to, context)

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
        to = [x[0] for x in recipients]
        to.append('continuous@fluidattacks.com')
        finding_requests = api.get_findings(project)["submissions"]
        for finding in finding_requests:
            finding_parsed = views.finding_vulnerabilities(finding["id"])
            if finding_parsed["edad"] != "-":
                age = int(finding_parsed["edad"])
                context = {
                    'project': project[0].upper(),
                    'finding': finding["id"],
                    'finding_name': finding_parsed["hallazgo"],
                    'finding_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                    + '/' + finding["id"] + '/description',
                    'finding_comment': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower() \
                                    + '/' + finding["id"] + '/comments',
                    'project_url': 'https://fluidattacks.com/integrates/dashboard#!/project/' + project[0].lower()
                    }
                if "kb" in finding_parsed:
                    if "https://fluidattacks.com/web/es/defends" in finding_parsed["kb"]:
                        context["kb"] = finding_parsed["kb"]
                if age == 240:
                    context["age"] = age
                elif age == 180:
                    context["age"] = age
                elif age == 120:
                    context["age"] = age
                elif age == 90:
                    context["age"] = age
                elif age == 60:
                    context["age"] = age
                elif age == 30:
                    context["age"] = age
                elif age == 15:
                    context["age"] = age
                if "age" in context:
                    if "kb" in context:
                        send_mail_age_kb_finding(to, context)
                    else:
                        send_mail_age_finding(to, context)