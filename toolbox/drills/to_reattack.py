# Standard library
from datetime import datetime as dt
from glob import glob
from os import listdir
from os.path import relpath
from typing import List, Dict

# Local libraries
from toolbox import api
from toolbox.constants import API_TOKEN


BASE_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project'


def get_subs_unverified_findings(subs: str):
    query = f'''
        query {{
            project(projectName: "{subs}") {{
                findings (filters: {{verified: False}}) {{
                    id,
                    vulnerabilities (state: "open"){{
                      id,
                      historicVerification {{
                          status,date
                        }}
                    }}
                }}
            }}
        }}
    '''

    return api.integrates.request(API_TOKEN, query)


def get_url(subs_name: str, finding_id: str) -> str:
    """Return a string with an url associated to a subs finding"""
    return f'  url:       {BASE_URL}/{subs_name}/{finding_id}'


def get_exploits(subs_name: str, finding_id: str) -> str:
    """Return a string with exploit paths associated to a subs finding"""
    message: str = ''
    exp_glob: str = \
        f'./groups/{subs_name}/forces/*/exploits/*{finding_id}*'
    exp_paths: List[str] = glob(exp_glob)
    for exp_path in map(relpath, exp_paths):
        message += f'  exploit:   {exp_path}\n'
    return message


def to_reattack(subs_name: str, with_exp: bool) -> tuple:
    """
    Return a string with non-verified findings from a subs.
    It includes integrates url and exploits paths in case they exist

    param: subs_name: Name of the group to check
    param: with_exp: Show findings with or without exploits
    """
    message: str = ''
    findings_raw: List[Dict] = \
        get_subs_unverified_findings(subs_name).data['project']['findings']
    findings_parsed: List[Dict] = []
    for finding in findings_raw:
        verivulns = filter(lambda x: bool(x['historicVerification']),
                           finding['vulnerabilities'])
        vulnsort = sorted(verivulns,
                          key=lambda x: x['historicVerification'][-1]['date'],)
        oldest = (dt.now() -
                  dt.strptime(vulnsort[0]['historicVerification'][-1]['date'],
                              '%Y-%m-%d %H:%M:%S')).days
        findings_parsed.append({'id': finding['id'],
                                'vulns': len(finding['vulnerabilities']),
                                'oldest': oldest})
    findings_sorted = \
        sorted(findings_parsed, key=lambda x: x['oldest'], reverse=True)

    for finding in findings_sorted:
        finding_id = finding['id']
        finding_oldest = finding['oldest']
        url: str
        exploits: str = get_exploits(subs_name, finding_id)
        if with_exp:
            if exploits:
                url = get_url(subs_name, finding_id)
                message += f'{url}\n'
                message += exploits
                message += f'  requested: {finding_oldest} days ago\n\n'
        else:
            if not exploits:
                url = get_url(subs_name, finding_id)
                message += f'{url}\n'
                message += f'  requested: {finding_oldest} days ago\n\n'

    return message, findings_parsed


def main(with_exp: bool):
    """
    Print all non-verified findings and their exploits

    param: with_exp: Show findings with or without exploits
    """
    subs_names: List[str] = listdir('groups')
    total_vulns: int = 0
    total_fin: int = 0
    oldest: tuple = (0, 'null')
    for subs_name in subs_names:
        message, pending_findings = to_reattack(subs_name, with_exp)
        if message:
            print(subs_name)
            print(message)
            total_vulns += sum(map(lambda x: x['vulns'], pending_findings))
            total_fin += len(pending_findings)
            old = pending_findings[-1]['oldest']
            oldest = (old, subs_name) if old > oldest[0] else oldest
    summary = (
        f"TO-DO: FIN: {total_fin}; "
        f"Vulns: {total_vulns}; "
        f"Days since oldest request: {oldest[0]}; "
        f"Group: {oldest[1]};"
    )
    print(summary)
