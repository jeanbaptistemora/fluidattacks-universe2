# Standard library
from glob import glob
from textwrap import dedent, indent
from typing import (
    Dict,
)

# Local libraries
from toolbox import (
    api,
    constants,
    logger,
    utils,
)

#
# Given a finding on Integrates may have many exploits
# Then we are going to bundle the related exploits into a single file
# And upload it to the corresponding finding
#


def _get_exploits_for_finding(group: str, finding_id: str) -> Dict[str, str]:
    """Return a dictionary mapping (exploit_path -> exploit_content)."""
    data: Dict[str, str] = {}
    for exp in glob(f'groups/{group}/forces/*/exploits/{finding_id}*.exp'):
        logger.info(f'  - {exp}')

        with open(exp) as exp_handle:
            data[exp] = exp_handle.read()

    return data


def _get_exploits_bundles(group: str) -> Dict[str, str]:
    """Return a dictionary mapping (finding_id -> exploit_bundle)."""
    data: Dict[str, str] = {}

    for finding_id, _ in utils.integrates.get_project_findings(group):
        logger.info(f'---')
        logger.info(f'group: {group}')
        logger.info(f'finding_id: {finding_id}')
        logger.info(f'exploits:')
        exploits = _get_exploits_for_finding(group, finding_id)

        data[finding_id] = dedent(f"""
            # group: {group}
            # id: {finding_id}
            #
            """)
        for exp_path, exp_content in exploits.items():
            data[finding_id] += dedent(f"""
                # path: {exp_path}
                #

                """)
            data[finding_id] += indent(exp_content, '    ')
            data[finding_id] += '\n\n'

    return data


def from_repo_to_integrates(group: str) -> bool:
    """Bundle related exploits and upload them to the corresponding finding."""
    success: bool = True
    exploits_bundles = _get_exploits_bundles(group)

    logger.info('---')
    for finding_id, exp_bundle in exploits_bundles.items():
        with utils.file.create_ephemeral('bundle.exp', exp_bundle) as file:
            response = api.integrates.Mutations.update_evidence(
                constants.API_TOKEN,
                finding_id,
                'EXPLOIT',
                file,
            )
            success = success \
                and response.ok \
                and not response.errors \
                and response.data['updateEvidence']['success']

            logger.info(f'response[{group}][{finding_id}]: {response}')

    return success
