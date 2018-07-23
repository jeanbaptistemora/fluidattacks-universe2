""" Asynchronous task execution scheduler for FLUIDIntegrates """

# pylint: disable=E0402
import rollbar
import logging
import logging.config
from django.conf import settings
from .dao import integrates_dao
from .api.formstack import FormstackAPI
from .mailer import send_mail_new_vulnerabilities, send_mail_new_remediated, \
                    send_mail_age_finding, send_mail_age_kb_finding, \
                    send_mail_new_releases, send_mail_continuous_report
from . import views
from datetime import datetime, timedelta

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

BASE_URL = "https://fluidattacks.com/integrates"
BASE_WEB_URL = "https://fluidattacks.com/web"


def get_new_vulnerabilities():
    """Summary mail send with the findings of a project."""
    # pylint: disable-msg=R0914
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        project = str.lower(str(project[0]))
        context = {'findings': list(), 'findings_working_on': list()}
        delta_total = 0
        try:
            finding_requests = api.get_findings(project)["submissions"]
            for finding in finding_requests:
                message = ""
                act_finding = views.finding_vulnerabilities(str(finding['id']))
                row = integrates_dao.get_vulns_by_id_dynamo(
                    project,
                    int(finding['id'])
                )
                if str.lower(str(act_finding['fluidProject'])) == project and \
                        "releaseDate" in act_finding and row:
                    finding_url = '{url!s}/dashboard#!/project/{project!s}/' \
                        '{finding!s}/description' \
                        .format(url=BASE_URL,
                                project=project,
                                finding=finding['id'])
                    has_treatment = finding_has_treatment(
                        act_finding,
                        finding_url)
                    if has_treatment:
                        context['findings_working_on'].append(has_treatment)
                    else:
                        message = 'Finding {finding!s} of project {project!s} '
                        'has defined treatment' \
                            .format(finding=finding['id'], project=project)
                        logger.info(message)
                    delta = int(act_finding['openVulnerabilities']) - \
                        int(row[0]['vuln_hoy'])
                    finding_text = format_vulnerabilities(delta, act_finding)
                    if finding_text != "":
                        context['findings'].append({
                            'nombre_hallazgo': finding_text,
                            'url_vuln': finding_url
                        })
                        delta_total = delta_total + abs(delta)
                        integrates_dao.add_or_update_vulns_dynamo(
                            str.lower(str(project[0])),
                            int(finding['id']),
                            int(act_finding['openVulnerabilities'])
                        )
                    else:
                        message = 'Finding {finding!s} of project ' \
                            '{project!s} no change during the week' \
                            .format(finding=finding['id'], project=project)
                        logger.info(message)
                else:
                    message = 'Finding {finding!s} of project {project!s} is '
                    'not valid' \
                        .format(finding=finding['id'], project=project)
                    logger.info(message)
        except (TypeError, KeyError):
            rollbar.report_message(
                'Error: An error ocurred getting new vulnerabilities '
                'notification email',
                'error')
        if delta_total > 0:
            context['proyecto'] = str.upper(str(project))
            context['url_proyecto'] = '{url!s}/dashboard#!/project/' \
                '{project!s}/indicators' \
                .format(url=BASE_URL, project=project)
            recipients = integrates_dao.get_project_users(project)
            to = [x[0] for x in recipients if x[1] == 1]
            to.append('continuous@fluidattacks.com')
            to.append('projects@fluidattacks.com')
            send_mail_new_vulnerabilities(to, context)


def format_vulnerabilities(delta, act_finding):
    """Format vulnerabities changes in findings."""
    if delta > 0:
        finding_text = u'{finding!s} (+{delta!s})'.format(
            finding=act_finding['finding'],
            delta=delta)
    elif delta < 0:
        finding_text = u'{finding!s} ({delta!s})'.format(
            finding=act_finding['finding'],
            delta=delta)
    else:
        finding_text = ""
    return finding_text


def finding_has_treatment(act_finding, finding_url):
    """Validate if a finding has treatment."""
    if ("releaseDate" in act_finding) and \
            (act_finding["estado"] != "Cerrado") and \
            (act_finding["edad"] != "-"):
        if "treatment" in act_finding and \
                act_finding["treatment"] == "Nuevo":
            finding_name = act_finding['finding'] + ' -' + \
                act_finding["edad"] + ' day(s)-'
            resp = {
                'hallazgo_pendiente': finding_name,
                'url_hallazgo': finding_url
            }
        else:
            resp = False
    else:
        resp = False
    return resp


def update_new_vulnerabilities():
    """Summary mail send to update the vulnerabilities of a project."""
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
                    if ("releaseDate" in act_finding and
                            str.lower(str(act_finding['fluidProject'])) == str.lower(str(project[0]))):
                        integrates_dao.add_or_update_vulns_dynamo(
                            str.lower(str(project[0])),
                            int(finding['id']), 0)
            else:
                message = 'Project {project!s} does not have new vulnerabilities' \
                    .format(project=project[0])
                logger.info(message)
        except (TypeError, KeyError):
            rollbar.report_message('Error: An error ocurred updating new vulnerabilities', 'error')


def get_remediated_findings():
    """Summary mail send with findings that have not been verified yet."""
    findings = integrates_dao.get_remediated_allfindings_dynamo(True)
    if findings != []:
        try:
            to = ['continuous@fluidattacks.com']
            context = {'findings': list()}
            cont = 0
            for finding in findings:
                context['findings'].append({
                    'finding_name': finding['finding_name'],
                    'finding_url':
                    '{url!s}/dashboard#!/project/{project!s}/{finding!s}/description'
                        .format(url=BASE_URL,
                                project=str.lower(str(finding['project'])),
                                finding=finding['finding_id']),
                    'project': str.upper(str(finding['project']))})
                cont += 1
            context['total'] = cont
            send_mail_new_remediated(to, context)
        except (TypeError, KeyError):
            rollbar.report_message(
                'Warning: An error ocurred getting data for remediated email',
                'warning')
    else:
        logger.info('There are no findings to verificate')


def get_age_notifications():
    """Send mail with findings that match age criteria."""
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        try:
            recipients = integrates_dao.get_project_users(project)
            to = [x[0] for x in recipients if x[1] == 1]
            to.append('continuous@fluidattacks.com')
            finding_requests = api.get_findings(project)["submissions"]
            project = str.lower(str(project[0]))
            for finding in finding_requests:
                finding_parsed = views.finding_vulnerabilities(finding["id"])
                if finding_parsed["edad"] != "-":
                    age = int(finding_parsed["edad"])
                else:
                    age = 0
                format_age_email(finding_parsed, project, to, age)
        except (TypeError, KeyError):
            rollbar.report_message(
                'Warning: An error ocurred getting data for age email',
                'warning')


def get_age_weekends_notifications():
    """Send mail on weekends with findings that match age criteria."""
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    for project in projects:
        try:
            recipients = integrates_dao.get_project_users(project)
            to = [x[0] for x in recipients if x[1] == 1]
            to.append('continuous@fluidattacks.com')
            finding_requests = api.get_findings(project)["submissions"]
            project = str.lower(str(project[0]))
            for finding in finding_requests:
                finding_parsed = views.finding_vulnerabilities(finding["id"])
                if finding_parsed["edad"] != "-":
                    unformatted_age = int(finding_parsed["edad"])
                    age = format_age_weekend(unformatted_age)
                else:
                    age = 0
                format_age_email(finding_parsed, project, to, age)
        except (TypeError, KeyError):
            rollbar.report_message(
                'Error: An error ocurred getting data for age weekends email',
                'error')


def format_age_email(finding_parsed, project, to, age):
    """Format data to send age email."""
    ages = [15, 30, 60, 90, 120, 180, 240]
    message = ""
    project_fin = str.lower(str(finding_parsed['fluidProject']))
    if ("suscripcion" in finding_parsed and
            "releaseDate" in finding_parsed and
            project_fin == project and
            finding_parsed["suscripcion"] == "Continua" and
            age in ages):
        context = {
            'project': str.upper(str(project)),
            'finding': finding_parsed["id"],
            'finding_name': finding_parsed["finding"],
            'finding_url':
            '{url!s}/dashboard#!/project/{project!s}/{finding!s}/description'
                .format(url=BASE_URL,
                        project=project,
                        finding=finding_parsed["id"]),
            'finding_comment':
            '{url!s}/dashboard#!/project/{project!s}/{finding!s}/comments'
                .format(url=BASE_URL,
                        project=project,
                        finding=finding_parsed["id"]),
            'project_url':
            '{url!s}/dashboard#!/project/{project!s}/indicators'
                .format(url=BASE_URL, project=project)
        }
        if "kb" in finding_parsed and \
                BASE_WEB_URL + "/es/defends" in \
                finding_parsed["kb"]:
            context["kb"] = finding_parsed["kb"]
        else:
            message = 'Finding {finding!s} of project ' \
                '{project!s} does not have kb link' \
                .format(finding=finding_parsed["id"], project=project)
            logger.info(message)
        send_mail_age(age, to, context)
    else:
        message = 'Finding {finding!s} of project {project!s} '\
            'does not match age mail criteria' \
            .format(finding=finding_parsed["id"], project=project)
        logger.info(message)

def format_age_weekend(age):
    ages = [15, 30, 60, 90, 120, 180, 240]
    if (age + 1) in ages:
        formatted_age = age + 1
    elif (age + 2) in ages:
        formatted_age = age + 2
    else:
        formatted_age = age
    return formatted_age

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
    """Summary mail send with findings that have not been released yet."""
    projects = integrates_dao.get_registered_projects()
    api = FormstackAPI()
    context = {'findings': list()}
    cont = 0
    for project in projects:
        try:
            finding_requests = api.get_findings(project)["submissions"]
            project = str.lower(str(project[0]))
            for finding in finding_requests:
                finding_parsed = views.finding_vulnerabilities(finding["id"])
                project_fin = str.lower(str(finding_parsed['fluidProject']))
                if ("releaseDate" not in finding_parsed and
                        project_fin == project):
                    context['findings'].append({
                        'finding_name': finding_parsed["finding"],
                        'finding_url':
                        '{url!s}/dashboard#!/project/{project!s}/{finding!s}'
                        '/description'
                            .format(url=BASE_URL,
                                    project=project,
                                    finding=finding["id"]),
                        'project': project
                    })
                    cont += 1
        except (TypeError, KeyError):
            rollbar.report_message(
                'Warning: An error ocurred getting data for new drafts email',
                'warning')
    if cont > 0:
        context['total'] = cont
        to = ["engineering@fluidattacks.com"]
        send_mail_new_releases(to, context)
    else:
        logger.info('There are no new drafts')

def continuous_report():
    to = ['jrestrepo@fluidattacks.com', 'ralvarez@fluidattacks.com', \
          'oparada@fluidattacks.com', 'projects@fluidattacks.com', 'relations@fluidattacks.com'  ]
    headers = ['#','Project','Lines','Inputs','Fixed vulns','Max severity', 'Open Events']
    context = {'projects':list(), 'headers': headers, 'date_now': str(datetime.now().date())}
    index = 0
    for x in integrates_dao.get_continuous_info():
        index += 1
        project_url = BASE_URL + "/dashboard#!/project/" + \
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
