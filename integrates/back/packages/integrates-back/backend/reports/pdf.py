# -*- coding: utf-8 -*-
""" Class to export the findings A PDF. """
# pylint: disable=wrong-import-position
import time
import sys
import subprocess
import uuid
import importlib

from typing import Dict, List
from jinja2 import select_autoescape
import jinja2
import matplotlib

from backend.reports.typing import PDFWordlistEn
from newutils.vulnerabilities import get_treatments

from __init__ import (
    BASE_URL,
    STARTDIR
)
from pylab import figure, pie, axis, savefig, cla, clf, close  # noqa


matplotlib.use('Agg')


# pylint: disable=too-many-instance-attributes
class CreatorPDF():
    """Class to generate reports in PDF."""

    style_dir = '/resources/themes'
    tpl_dir = '/tpls/'
    font_dir = '/resources/fonts'
    result_dir = '/results/results_pdf/'
    proj_tpl = 'templates/pdf/executive.adoc'
    style = 'fluid'
    lang = 'en'
    doctype = 'executive'
    wordlist = None
    out_name = ''
    command = ''
    context: Dict[str, str] = {}

    def __init__(self, lang, doctype, tempdir):
        """Class constructor."""
        self.path = (
            f'{STARTDIR}/integrates/back/packages/'
            'integrates-back/backend/reports'
        )
        self.result_dir = self.path + self.result_dir
        self.font_dir = self.path + self.font_dir
        self.tpl_dir = self.path + self.tpl_dir
        self.tpl_img_path = tempdir
        self.lang = lang
        self.doctype = doctype
        self.style_dir = self.path + self.style_dir
        if self.doctype == 'tech':
            self.proj_tpl = 'templates/pdf/tech.adoc'
        importlib.reload(sys)
        try:
            sys.setdefaultencoding('utf-8')
        except AttributeError:
            # Py3
            importlib.reload(sys)
        self.lang_support()

    def create_command(self, tpl_name):
        """ Create the SO command to create the PDF with asciidoctor. """
        self.command += 'rm :template: &&'
        self.command = 'asciidoctor-pdf '
        self.command += '-a pdf-stylesdir=:style_dir: '
        self.command += '-a pdf-style=:style: '
        self.command += '-a pdf-fontsdir=:font_dir: '
        self.command += '-D :result_dir: '
        self.command += '-o :out_name: '
        self.command += ':template: && chmod 777 :template:'
        self.command = self.command.replace(':style:', self.style)
        self.command = self.command.replace(':style_dir:', self.style_dir)
        self.command = self.command.replace(':font_dir:', self.font_dir)
        self.command = self.command.replace(':result_dir:', self.result_dir)
        self.command = self.command.replace(':out_name:', self.out_name)
        self.command = self.command.replace(':template:', tpl_name)

    def lang_support(self):
        """ Define the dictionaries of accepted languages. """
        self.wordlist = dict()
        self.lang_support_en()

    def lang_support_en(self):
        """ Add the English dictionary.  """
        self.wordlist['en'] = dict(
            zip(PDFWordlistEn.keys(), PDFWordlistEn.labels())
        )

    async def tech(self, data, project, description, user, context):  # noqa pylint: disable=too-many-arguments
        """ Create the template to render and apply the context. """
        await self.fill_project(data, project, description, user, context)
        self.out_name = str(uuid.uuid4()) + '.pdf'
        searchpath = self.path
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(
            loader=template_loader,
            autoescape=select_autoescape(['html', 'xml'],
                                         default=True)
        )
        template = template_env.get_template(self.proj_tpl)
        tpl_name = self.tpl_dir + ':id_IT.tpl'.replace(':id', project)
        render_text = template.render(self.context)
        with open(tpl_name, 'wb') as tplfile:
            tplfile.write(render_text.encode('utf-8'))
        self.create_command(tpl_name)
        subprocess.call(self.command, shell=True)

    def project_info_context(self, project_info):
        """ Create the template to render and apply the context. """
        self.context['projectName'] = project_info['projectName']
        self.context['clientProject'] = project_info['clientProject']
        self.context['client'] = project_info['client']
        self.context['leader'] = project_info['leader']
        self.context['analyst'] = project_info['analyst']
        self.context['arquitect'] = project_info['arquitect']
        self.context['startDate'] = project_info['startDate']
        self.context['endDate'] = project_info['endDate']
        self.context['testType'] = project_info['testType']
        self.context['environment'] = project_info['environment']
        self.context['coverageType'] = project_info['coverageType']
        self.context['findingsMap'] = project_info['findingsMap']
        self.context['securityLevel'] = project_info['securityLevel']
        self.context['coverage'] = ''
        self.context['toeVisibleFields'] = ''
        self.context['toeVisibleLines'] = ''
        self.context['toeVisiblePorts'] = ''
        if 'coverage' in project_info:
            self.context['coverage'] = project_info['coverage']
        if 'toeVisibleFields' in project_info:
            self.context['toeVisibleFields'] = project_info['toeVisibleFields']
        if 'toeVisibleLines' in project_info:
            self.context['toeVisibleLines'] = project_info['toeVisibleLines']
        if 'toeVisiblePorts' in project_info:
            self.context['toeVisiblePorts'] = project_info['toeVisiblePorts']
        self.context['toeTestedFields'] = project_info['toeTestedFields']
        self.context['toeTestedLines'] = project_info['toeTestedLines']
        self.context['toeTestedPorts'] = project_info['toeTestedPorts']
        self.context['relevantImpact'] = project_info['relevantImpact']
        self.context['observations'] = project_info['observations']
        self.context['conclusions'] = project_info['conclusions']
        self.context['recommendations'] = project_info['recommendations']
        self.context['industryType'] = project_info['industryType']
        self.context['language'] = project_info['language']
        self.context['applicationType'] = project_info['applicationType']

    def make_content(self, words):
        """ Create context with the titles of the document. """
        base_img = 'image::../templates/pdf/{name}_{lang}.png[]'
        base_adoc = 'include::../templates/pdf/{name}_{lang}.adoc[]'
        return {
            'content_title': words['content_title'],
            'content_list': words['content_list'],
            'goals_title': words['goals_title'],
            'goals_img': base_img.format(name='goals', lang=self.lang),
            'severity_img': base_img.format(name='severity', lang=self.lang),
            'metodology_title': words['metodology_title'],
            'metodology_img': base_img.format(
                name='metodology', lang=self.lang),
            'footer_adoc': base_adoc.format(name='footer', lang=self.lang)
        }

    def make_pie_finding(self, findings, project, words):
        """ Create the findings graph. """
        figure(1, figsize=(6, 6))
        finding_state_pie = [0, 0, 0, 0]  # A, PC, C
        finding_state_pielabels = [
            words['vuln_c'],
            words['vuln_h'],
            words['vuln_m'],
            words['vuln_l']
        ]
        colors = ['#980000', 'red', 'orange', 'yellow']
        explode = (0.1, 0, 0, 0)
        for finding in findings:
            severity = finding['severityCvss']
            if 9.0 <= severity <= 10.0:
                finding_state_pie[0] += 1
            elif 7.0 <= severity <= 8.9:
                finding_state_pie[1] += 1
            elif 4.0 <= severity <= 6.9:
                finding_state_pie[2] += 1
            elif 0.0 <= severity <= 3.9:  # Abierto por defecto
                finding_state_pie[3] += 1
            else:
                finding_state_pie[3] += 1
        pie(
            finding_state_pie,
            explode=explode,
            labels=finding_state_pielabels,
            autopct='%1.0f%%',
            startangle=90,
            colors=colors
        )
        axis('equal')
        pie_filename = f'{self.tpl_img_path}/finding_graph_{project}.png'
        savefig(pie_filename, bbox_inches='tight', transparent=True, dpi=100)
        cla()
        clf()
        close('all')
        return pie_filename

    async def fill_project(self, findings, project, description, user, context):  # noqa pylint: disable=too-many-arguments,too-many-locals
        """ Add project information. """
        words = self.wordlist[self.lang]
        full_project = description
        doctype = words[self.doctype]
        full_project += ' [' + project + ']'
        team = 'Engineering Team'
        version = 'v1.0'
        team_mail = 'engineering@fluidattacks.com'
        main_pie_filename = self.make_pie_finding(findings, project, words)
        finding_vulns_loader = context.finding_vulns_nzr
        vulnerabilities = await finding_vulns_loader.load_many([
            finding['findingId'] for finding in findings
        ])
        for finding, vulns in zip(findings, vulnerabilities):
            treatment = get_treatments(vulns)
            treatments: List[str] = []
            if treatment.ACCEPTED > 0:
                treatments.append(
                    f'{words["treat_status_asu"]}: {treatment.ACCEPTED}'
                )
            if treatment.ACCEPTED_UNDEFINED > 0:
                treatments.append(
                    f'{words["treat_ete_asu"]}: {treatment.ACCEPTED_UNDEFINED}'
                )
            if treatment.IN_PROGRESS > 0:
                treatments.append(
                    f'{words["treat_status_rem"]}: {treatment.IN_PROGRESS}'
                )
            if treatment.NEW > 0:
                treatments.append(
                    f'{words["treat_status_wor"]}: {treatment.NEW}'
                )

            if int(finding['openVulnerabilities']) > 0:
                finding['state'] = words['fin_status_open']
                finding['treatment'] = '\n'.join(sorted(treatments))
            else:
                finding['state'] = words['fin_status_closed']
                finding['treatment'] = '-'

        main_pie_filename = 'image::' \
            + main_pie_filename \
            + '[width=300, align=center]'
        main_tables = make_vuln_table(findings, words)
        fluid_tpl_content = self.make_content(words)
        access_vector = get_access_vector(findings[0])
        self.context = {
            'full_project': full_project.upper(),
            'team': team,
            'team_mail': team_mail,
            'customer': '',
            'toe': description,
            'version': version,
            'revdate': doctype + ' ' + time.strftime('%d/%m/%Y'),
            'simpledate': time.strftime('%Y.%m.%d'),
            'fluid_tpl': fluid_tpl_content,
            'main_pie_filename': main_pie_filename,
            'main_tables': main_tables,
            'findings': findings,
            'accessVector': access_vector,
            # Titulos segun lenguaje
            'finding_title': words['finding_title'],
            'finding_section_title': words['finding_section_title'],
            'where_title': words['where_title'],
            'description_title': words['description_title'],
            'resume_vuln_title': words['resume_vuln_title'],
            'resume_perc_title': words['resume_perc_title'],
            'resume_regi_title': words['resume_regi_title'],
            'resume_vnum_title': words['resume_vnum_title'],
            'resume_vname_title': words['resume_vname_title'],
            'resume_ttab_title': words['resume_ttab_title'],
            'resume_top_title': words['resume_top_title'],
            'risk_title': words['risk_title'],
            'evidence_title': words['evidence_title'],
            'records_title': words['records_title'],
            'threat_title': words['threat_title'],
            'solution_title': words['solution_title'],
            'requisite_title': words['requisite_title'],
            'treatment_title': words['treatment_title'],
            'severity_title': words['severity_title'],
            'cardinality_title': words['cardinality_title'],
            'attack_vector_title': words['attack_vector_title'],
            'compromised_system_title': words['compromised_system_title'],
            'resume_page_title': words['resume_page_title'],
            'resume_table_title': words['resume_table_title'],
            'state_title': words['state_title'],
            'crit_h': words['crit_h'],
            'crit_m': words['crit_m'],
            'crit_l': words['crit_l'],
            'field': words['field'],
            'inputs': words['inputs'],
            'line': words['line'],
            'lines': words['lines'],
            'path': words['path'],
            'port': words['port'],
            'ports': words['ports'],
            'user': user,
            'date': time.strftime('%Y-%m-%d at %H:%M'),
            'link': f'{BASE_URL}/groups/{project}/vulns'
        }


def get_access_vector(finding):
    """ Get metrics based on cvss version. """
    if finding.get('cvssVersion') == '3.1':
        severity = get_severity('attackVector', finding['attackVector'])
    else:
        severity = get_severity('accessVector', finding['accessVector'])
    return severity


def get_severity(metric, metric_value):
    """Extract number of CSSV2 metrics."""
    try:
        metrics = {
            'accessVector': {
                '0.395': 'Local',
                '0.646': 'Red adyacente',
                '1.0': 'Red',
            },
            'attackVector': {
                '0.85': 'Red',
                '0.62': 'Red adyacente',
                '0.55': 'Local',
                '0.20': 'Físico',
            },
            'confidentialityImpact': {
                '0.0': 'Ninguno',
                '0.275': 'Parcial',
                '0.66': 'Completo',
            },
            'integrityImpact': {
                '0.0': 'Ninguno',
                '0.275': 'Parcial',
                '0.66': 'Completo',
            },
            'availabilityImpact': {
                '0.0': 'Ninguno',
                '0.275': 'Parcial',
                '0.66': 'Completo',
            },
            'authentication': {
                '0.45': 'Múltiple',
                '0.56': 'Única',
                '0.704': 'Ninguna',
            },
            'exploitability': {
                '0.85': 'Improbable',
                '0.9': 'Conceptual',
                '0.95': 'Funcional',
                '1.0': 'Alta',
            },
            'confidenceLevel': {
                '0.9': 'No confirmado',
                '0.95': 'No corroborado',
                '1.0': 'Confirmado',
            },
            'resolutionLevel': {
                '0.87': 'Oficial',
                '0.9': 'Temporal',
                '0.95': 'Paliativa',
                '1.0': 'Inexistente',
            },
            'accessComplexity': {
                '0.35': 'Alto',
                '0.61': 'Medio',
                '0.71': 'Bajo',
            }
        }
        metric_descriptions = metrics.get(metric)
        if metric_descriptions:
            description = metric_descriptions.get(str(metric_value))
        else:
            description = ''
        return description
    except ValueError:
        return ''


def make_vuln_table(findings, words):
    """Label findings percent quantity."""
    vuln_table = [
        [words['vuln_c'], 0, 0, 0],
        [words['vuln_h'], 0, 0, 0],
        [words['vuln_m'], 0, 0, 0],
        [words['vuln_l'], 0, 0, 0],
        ['Total', len(findings), '100.00%', 0],
    ]
    top_table = []
    ttl_vulns, ttl_num_reg, top = 0, 0, 1
    for finding in findings:
        severity = finding['severityCvss']
        crit_as_text = words['crit_l']
        vuln_amount = 0
        if finding['openVulnerabilities'] != '-':
            vuln_amount = int(finding['openVulnerabilities'])
        ttl_vulns += vuln_amount
        if 9.0 <= severity <= 10.0:
            vuln_table[0][1] += 1
            vuln_table[0][3] += vuln_amount
            crit_as_text = words['crit_c']
        elif 7.0 <= severity <= 8.9:
            vuln_table[1][1] += 1
            vuln_table[1][3] += vuln_amount
            crit_as_text = words['crit_h']
        elif 4.0 <= severity <= 6.9:
            vuln_table[2][1] += 1
            vuln_table[2][3] += vuln_amount
            crit_as_text = words['crit_m']
        else:
            vuln_table[3][1] += 1
            vuln_table[3][3] += vuln_amount
        ttl_num_reg += int(finding.get('recordsNumber', 0))
        finding['severityCvss'] = str(finding['severityCvss'])
        if top <= 5:
            top_table.append([
                top,
                finding['severityCvss'] + ' ' + crit_as_text,
                finding['finding']
            ])
            top += 1
    vuln_table[0][2] = vuln_table[0][1] * 100 / float(len(findings))
    vuln_table[1][2] = vuln_table[1][1] * 100 / float(len(findings))
    vuln_table[2][2] = vuln_table[2][1] * 100 / float(len(findings))
    vuln_table[3][2] = vuln_table[3][1] * 100 / float(len(findings))
    vuln_table[0][2] = '{0:.2f}%'.format(vuln_table[0][2])
    vuln_table[1][2] = '{0:.2f}%'.format(vuln_table[1][2])
    vuln_table[2][2] = '{0:.2f}%'.format(vuln_table[2][2])
    vuln_table[3][2] = '{0:.2f}%'.format(vuln_table[3][2])
    vuln_table[4][3] = ttl_vulns
    return {
        'resume': vuln_table,
        'top': top_table,
        'num_reg': ttl_num_reg
    }
