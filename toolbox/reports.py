# Standard library
import csv
from typing import List, NamedTuple

# Third parties libraries

# Local imports
from toolbox import constants, logger, toolbox, utils

ExploitInfo = NamedTuple('ExploitInfo', [
    ('path', str),
    ('subscription', str), ('customer', str), ('integrates_status', str),
    ('kind', str), ('type', str), ('score', float), ('finding_id', str),
    ('finding_title', str), ('reason', str), ('url', str)
])


def process_exploit(exp_path: str):
    """
    Get all the information from an exploit.

    :param exp_path: Exploit path.

    :rtype: :class:`ExploitInfo`
    """
    result = None
    subs = exp_path.split('/')[1]
    exp_type = exp_path.split('/')[3]

    exp_kind, finding_id = utils.forces.scan_exploit_for_kind_and_id(exp_path)
    reason = utils.forces.get_integrates_exploit_category(exp_path)

    if utils.integrates.does_finding_exist(finding_id):
        score = utils.integrates.get_finding_cvss_score(finding_id)
        title = utils.integrates.get_finding_title(finding_id)

        url = ('https://fluidattacks.com/integrates/dashboard#!/'
               f'project/{subs}/findings/{finding_id}/evidence')
        status = ('accepted' if 'accepted' in exp_path else
                  ('open' if utils.integrates.is_finding_open(
                      finding_id=finding_id,
                      finding_types=(constants.SAST if exp_type == 'static'
                                     else constants.DAST)) else 'closed'))
        result = ExploitInfo(
            path=exp_path,
            subscription=subs,
            integrates_status=status,
            kind=exp_kind,
            type=exp_type,
            score=score,
            finding_id=finding_id,
            customer='',
            finding_title=title,
            url=url,
            reason=reason)
    else:
        result = ExploitInfo(
            path=exp_path,
            subscription=subs,
            customer='',
            integrates_status='unknown',
            kind=exp_kind,
            type=exp_type,
            score=0,
            finding_id=finding_id,
            finding_title='unknown',
            url='unknown',
            reason=reason)
    return result


def process_group_exploits(subs: dict) -> List:
    """
    Process all exploits of a group.

    :param group: group configuration.

    :rtype: :class:`List[ExploitInfo]`
    """
    result = []
    subs_name = subs['name']
    exploit_paths_iterator = utils.generic.iter_exploit_paths(subs_name)
    for exploit in map(process_exploit, exploit_paths_iterator):
        exploit = exploit._replace(customer=subs['customer'])
        result.append(exploit)
    return result


def generate_exploits_report(file_name: str = 'report.csv',
                             customer: str = None,
                             group: str = None):
    """
    Generate a report of all exploits.
    """
    logger.info('Generating exploits report')
    with open(file_name, 'w') as new_csv_handle:
        writer = csv.DictWriter(
            new_csv_handle,
            fieldnames=ExploitInfo._fields,
            quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for subs in utils.generic.iter_subscritions_config():
            if not toolbox.has_forces(subs['name']) or (
                    customer and subs['customer'] != customer) or (
                        group and subs['name'] != group):
                continue

            logger.info(f'Filling with iexps {subs["name"]}')
            with utils.generic.output_block(indent=4):
                toolbox.fill_with_iexps(subs['name'])

            logger.info(f'Gererating report for {subs["name"]}')
            info = process_group_exploits(subs)
            for row in info:
                writer.writerow(row._asdict())
