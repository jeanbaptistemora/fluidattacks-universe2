# Standard library
from glob import glob
from os import listdir
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
                    id
                }}
            }}
        }}
    '''

    return api.integrates.request(API_TOKEN, query)


def get_url(subs_name: str, finding_id: str) -> str:
    """Return a string with an url associated to a subs finding"""
    return f'    {BASE_URL}/{subs_name}/{finding_id}'


def get_exploits(subs_name: str, finding_id: str) -> str:
    """Return a string with exploit paths associated to a subs finding"""
    message: str = ''
    exp_glob: str = \
        f'./subscriptions/{subs_name}/break-build/*/exploits/*{finding_id}*'
    exp_paths: List[str] = glob(exp_glob)
    for exp_path in exp_paths:
        message += f'        Exploit: {exp_path}'
        if exp_path != exp_paths[-1]:
            message += '\n'
        else:
            pass
    return message


def to_reattack(subs_name: str) -> str:
    """
    Return a string with non-verified findings from a subs.
    It includes integrates url and exploits paths in case they exist
    """
    message: str = ''
    findings_raw: List[Dict[str, str]] = \
        get_subs_unverified_findings(subs_name).data['project']['findings']
    findings_parsed: List[str] = list(map(lambda x: x['id'], findings_raw))
    for finding_id in findings_parsed:
        url: str = get_url(subs_name, finding_id)
        exploits: str = get_exploits(subs_name, finding_id)
        message += f'{url}\n'
        if exploits:
            message += f'{exploits}\n'
    return message


def main():
    """Print all non-verified findings and their exploits"""
    subs_names: List[str] = listdir('subscriptions')
    for subs_name in subs_names:
        message: str = to_reattack(subs_name)
        if message:
            print(subs_name)
            print(message)
