# Standard library
from datetime import datetime as dt
from glob import glob
from os.path import relpath
from typing import List
from dateutil.relativedelta import relativedelta

# Local libraries
from toolbox import api
from toolbox.constants import API_TOKEN


BASE_URL: str = 'https://integrates.fluidattacks.com/dashboard#!/project'


def get_subs_unverified_findings(sub_name: str):

    project_info_query = '''
        name
        findings(filters: {verified: False}) {
            id
            vulnerabilities(state: "open") {
                id
                historicVerification {
                    status, date
                }
            }
        }

    '''

    if sub_name == 'all':
        query = f'''
            query {{
                me {{
                    projects {{
                                {project_info_query}
                     }}
                }}
            }}
        '''
    else:
        query = f'''
            query{{
                project(projectName: "{sub_name}") {{
                                {project_info_query}
                }}
            }}
        '''

    return api.integrates.request(API_TOKEN, query)


def get_url(subs_name: str, finding_id: str) -> str:
    """Return a string with an url associated to a subs finding"""
    return f'{BASE_URL}/{subs_name}/{finding_id}'


def get_exploits_paths(subs_name: str, finding_id: str) -> List:
    """Return a string with exploit paths associated to a subs finding"""
    exploits_paths: list = []
    exp_glob: str = \
        f'./groups/{subs_name}/forces/*/exploits/*{finding_id}*'
    exp_paths: List[str] = glob(exp_glob)
    for exp_path in map(relpath, exp_paths):
        exploits_paths.append(exp_path)
    return exploits_paths


def to_reattack(with_exp: bool, sub_name: str = 'all') -> list:
    """
    Return a string with non-verified findings from a subs.
    It includes integrates url and exploits paths in case they exist

    param: sub_name: Name of the group to check
    param: with_exp: Show findings with or without exploits
    """
    graphql_date_format = '%Y-%m-%d %H:%M:%S'

    projects_info = get_subs_unverified_findings(sub_name)
    if sub_name != 'all':
        class Tmp():
            def __init__(self):
                self.data = None
        tmp = Tmp()
        tmp.data = {'me': None}
        tmp.data['me'] = {'projects': [None]}
        tmp.data['me']['projects'][0] = projects_info.data['project']
        projects_info = tmp

    projects_info = list(projects_info.data['me']['projects'])
    # claning empty findigs
    projects_info = list(filter(
        lambda info: info['findings'],
        projects_info
    ))
    # cleaning findings without vulnerabilities
    for project_info in projects_info:
        project_info['findings'] = list(filter(
            lambda finding:
                finding['vulnerabilities'],
            project_info['findings']
        ))

    total_findings = 0
    total_vulnerabilities = 0
    oldest_finding = {
        'group': '',
        'date_dif': relativedelta()
    }

    for project_info in projects_info:
        for finding in project_info['findings']:
            # Filter requested vulnerabilities
            finding['vulnerabilities'] = filter(
                lambda vulnerability:
                    vulnerability
                and
                    vulnerability['historicVerification']
                and
                    vulnerability['historicVerification']
                                 [-1]
                                 ['status'] == 'REQUESTED',
                finding['vulnerabilities']
            )

            # Order vulnerabilities by date
            finding['vulnerabilities'] = list(sorted(
                finding['vulnerabilities'],
                key=lambda x: x['historicVerification']
                               [-1]
                               ['date']
            ))
            oldest_vulnerability = finding['vulnerabilities'][0]
            oldest_vuln_dif = relativedelta(
                dt.now(),
                dt.strptime(
                    oldest_vulnerability['historicVerification']
                                        [-1]
                                        ['date'],
                    graphql_date_format
                )
            )
            finding['vulnerability_counter'] = len(finding['vulnerabilities'])
            finding['oldest_vulnerability'] = oldest_vulnerability
            finding['oldest_vuln_dif'] = oldest_vuln_dif
            finding['exploit_paths'] = get_exploits_paths(
                project_info['name'],
                finding['id']
            )
            finding['url'] = get_url(project_info["name"], finding["id"])

            if with_exp and finding['exploit_paths']:
                total_vulnerabilities += finding['vulnerability_counter']
                if (oldest_finding['date_dif'].days <  # type: ignore
                        finding['oldest_vuln_dif'].days):
                    oldest_finding = {
                        'group': project_info['name'],
                        'date_dif': finding['oldest_vuln_dif']
                    }
            elif not with_exp and finding['exploit_paths']:
                total_vulnerabilities += finding['vulnerability_counter']
                # type: ignore
                if (oldest_finding['date_dif'].days <  # type: ignore
                        finding['oldest_vuln_dif'].days):

                    oldest_finding = {
                        'group': project_info['name'],
                        'date_dif': finding['oldest_vuln_dif']
                    }

        if with_exp:
            project_info['findings'] = list(filter(
                lambda finding:
                    finding['exploit_paths'],
                project_info['findings']
            ))
        else:
            project_info['findings'] = list(filter(
                lambda finding:
                    not finding['exploit_paths'],
                project_info['findings']
            ))

        total_findings += len(project_info['findings'])

    # clean trash
    projects_info = list(filter(
        lambda project_info:
            project_info['findings'],
        projects_info
    ))

    # Printing all
    for project_info in projects_info:
        if project_info['findings']:
            # Head
            print(project_info['name'])
            # Body
            for finding in project_info['findings']:
                print('  url:               '
                      f'{finding["url"]}\n'
                      '  requested (days):  '
                      f'{finding["oldest_vuln_dif"].days}\n'
                      '  vulns to verify:   '
                      f'{finding["vulnerability_counter"]}'
                      )
                if finding['exploit_paths']:
                    print('  exploits: ')
                    for path_exploit in finding['exploit_paths']:
                        print(f'           - {path_exploit}')

                print()
            print()

    # summary
    summary = (
        f"TO-DO: FIN: {total_findings}; "  # type: ignore
        f"Vulns: {total_vulnerabilities}; "
        f"Days since oldest request: {oldest_finding['date_dif'].days}; "
        f"Group: {oldest_finding['group']};"
    )

    print(summary)

    return projects_info


def main(with_exp: bool):
    """
    Print all non-verified findings and their exploits

    param: with_exp: Show findings with or without exploits
    """
    to_reattack(with_exp, 'continuoustest')
