"""This migration removes orphan evidence files
Evidences files listed in s3 without reference in dynamodb
because evidence files since a change be saved with a
generic names, leaving old files
Execution Time:     2020-06-16 14:43 UTC-5
Finalization Time:  2020-06-16 15:21 UTC-5
"""
import os
from typing import List

from backend.dal import (
    finding as finding_dal,
    project as project_dal,
)
from __init__ import FI_TEST_PROJECTS


TEST_PROJECTS: List[str] = FI_TEST_PROJECTS.split(',')
STAGE: str = os.environ['STAGE']


def clean_finding_evidences(group_name: str) -> None:
    findings = \
        project_dal.list_drafts(group_name, should_list_deleted=True) + \
        project_dal.list_findings(group_name, should_list_deleted=True)

    for finding_id in findings:
        finding = finding_dal.get_finding(finding_id)
        evidence_prefix = f'{group_name}/{finding_id}'
        files = [file_name.get('file_url', '')
                 for file_name in finding.get('files', [])]
        files = [f'{evidence_prefix}/{file_name}' for file_name in files]
        for file_name in finding_dal.search_evidence(evidence_prefix):
            if file_name not in files and \
               file_name != f'{group_name}/{finding_id}/':
                if STAGE == 'test':
                    print(f'orphan evidence file_name: {file_name}')
                else:
                    print(f'removing evidence file_name: {file_name}')
                    finding_dal.remove_evidence(file_name)


def main() -> None:
    print('Starting migration 0011')

    groups = project_dal.get_all()
    for group in groups:
        group_name = group['project_name']

        if group_name not in TEST_PROJECTS:
            print(f'--- group name {group_name}')
            clean_finding_evidences(group_name)

        print('---')


if __name__ == '__main__':
    main()
