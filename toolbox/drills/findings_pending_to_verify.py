# Standard library
import glob
from os import listdir
from typing import List, Dict

# Local libraries
from toolbox import api
from toolbox.constants import API_TOKEN


BASE_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project'


def get_url(subs_name: str, finding_id: str) -> str:
    """Return a string with an url associated to a subs finding"""
    return f'    {BASE_URL}/{subs_name}/{finding_id}'


def get_exploits(subs_name: str, finding_id: str) -> str:
    """Return a string with exploit paths associated to a subs finding"""
    message: str = ''
    exp_glob: str = \
        f'./subscriptions/{subs_name}/break-build/*/exploits/*{finding_id}*'
    exp_paths: List[str] = glob.glob(exp_glob)
    for exp_path in exp_paths:
        message += f'        Exploit: {exp_path}'
        if exp_path != exp_paths[-1]:
            message += '\n'
        else:
            pass
    return message


def findings_pending_to_verify(subs_name: str) -> str:
    """
    Return a string with non-verified findings from a subs.
    It includes integrates url and exploits paths in case they exist
    """
    message: str = ''
    findings: List[Dict] = api.integrates.Queries.project(
        api_token=API_TOKEN,
        project_name=subs_name,
        with_findings=True).data['project']['findings']
    for finding in findings:
        verified: bool = finding['verified']
        if not verified:
            identifier: str = finding['id']
            url: str = get_url(subs_name, identifier)
            exploits: str = get_exploits(subs_name, identifier)
            message += f'{url}\n'
            if exploits:
                message += f'{exploits}\n'
        else:
            pass
    return message


def main():
    """Print all non-verified findings and their exploits"""
    subs_names: List[str] = listdir('subscriptions')
    for subs_name in subs_names:
        message: str = findings_pending_to_verify(subs_name)
        if message:
            print(subs_name)
            print(message)
