# Standard library
from datetime import datetime as dt
from glob import glob
from os.path import relpath
from typing import List, Dict

# Local libraries
from toolbox import api, utils
from toolbox.constants import API_TOKEN


BASE_URL: str = 'https://integrates.fluidattacks.com/dashboard#!/project'


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
    findings_raw = get_subs_unverified_findings(subs_name)
    findings_raw = findings_raw.data['project'][
        'findings'] if findings_raw.ok else []
    findings_parsed: List[Dict] = []
    findings_ret: List[Dict] = []
    for finding in findings_raw:
        # Find the oldest verification request
        verivulns = filter(lambda x: x['historicVerification'] and
                           x['historicVerification'][-1]['status']
                           == 'REQUESTED',
                           finding['vulnerabilities'])
        vulnsort = sorted(verivulns,
                          key=lambda x: x['historicVerification'][-1]['date'],)
        oldest = (dt.now() -
                  dt.strptime(vulnsort[0]['historicVerification'][-1]['date'],
                              '%Y-%m-%d %H:%M:%S')).days
        findings_parsed.append({'id': finding['id'],
                                'vulns': len(vulnsort),
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
                findings_ret.append(finding)
                url = get_url(subs_name, finding_id)
                message += f'{url}\n'
                message += exploits
                message += f'  requested: {finding_oldest} days ago\n' \
                           f'  vulns to verify: {finding["vulns"]}\n\n'
        else:
            if not exploits:
                findings_ret.append(finding)
                url = get_url(subs_name, finding_id)
                message += f'{url}\n'
                message += f'  requested: {finding_oldest} days ago\n' \
                           f'  vulns to verify: {finding["vulns"]}\n\n'

    return message, findings_ret


def main(with_exp: bool):
    """
    Print all non-verified findings and their exploits

    param: with_exp: Show findings with or without exploits
    """
    total_vulns: int = 0
    total_fin: int = 0
    oldest: tuple = (0, 'null')
    subs_names: List[str] = utils.integrates.get_my_projects()
    for subs_name in subs_names:
        message, pending_findings = to_reattack(subs_name, with_exp)
        if message:
            print(subs_name)
            print(message)
            total_vulns += sum(map(lambda x: x['vulns'], pending_findings))
            total_fin += len(pending_findings)
            old = pending_findings[0]['oldest']
            oldest = (old, subs_name) if old > oldest[0] else oldest
    summary = (
        f"TO-DO: FIN: {total_fin}; "
        f"Vulns: {total_vulns}; "
        f"Days since oldest request: {oldest[0]}; "
        f"Group: {oldest[1]};"
    )
    print(summary)
