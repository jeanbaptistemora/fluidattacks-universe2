# Standard library
import re
import csv
import glob
from multiprocessing import Pool, cpu_count
from typing import List, NamedTuple
from itertools import repeat

# Third parties libraries
import ruamel.yaml as yaml

# Local imports
from toolbox import constants, helper, logger, toolbox, utils

ExploitInfo = NamedTuple(
    'ExploitInfo',
    [('subscription', str), ('customer', str), ('integrates_status', str),
     ('kind', str), ('type', str), ('score', float), ('finding_id', str),
     ('finding_title', str), ('reason', str), ('url', str)])


def get_customer_subs(customer: str) -> tuple:
    return tuple(sorted({
        config['name'].lower()
        for config_path in glob.glob('subscriptions/*/config/config.yml')
        for config in (yaml.safe_load(open(config_path)),)
        if config['customer'].lower() == customer
    }))


def process_exp(customer_subs, cache, exp_path):
    """Process an exploit."""
    try:
        subs, exp_type = re.match(pattern=r'^\w+/(\w+)/forces/(\w+)',
                                  string=exp_path).groups()

        if subs not in customer_subs:
            return None

        exp_kind, fin_id = helper.forces.scan_exploit_for_kind_and_id(exp_path)

        int_status = (
            'accepted'
            if 'accepted' in exp_path
            else (
                'open'
                if helper.integrates.is_finding_open(
                    finding_id=fin_id,
                    finding_types=(
                        constants.SAST
                        if exp_type == 'static'
                        else constants.DAST
                    )
                )
                else 'closed'
            ))
        int_score = helper.integrates.get_finding_cvss_score(fin_id)
        int_title = helper.integrates.get_finding_title(fin_id)

        row = {
            'subscription': subs,
            'integrates status': int_status,
            'exploit kind': exp_kind,
            'exploit type': exp_type,
            'score': int_score,
            'finding id': fin_id,
            'finding title': int_title,
            **{
                field: cache.get((subs, fin_id), {}).get(field, 'FIX ME')
                for field in (
                    'is optimized ?',
                    'can be automatized?',
                    'reason',
                )
            }
        }
        logger.info('ok', exp_path)
        return row
    except (IndexError, TypeError):
        logger.info('please manually add:', exp_path)
        return None


def generate_bancolombia_exploits_report(old_csv: str = 'report.csv'):
    """Generate the csv report."""
    fieldnames: List[str] = [
        'subscription',
        'integrates status',
        'exploit kind',
        'exploit type',
        'score',
        'finding id',
        'finding title',
        'is optimized ?',
        'can be automatized?',
        'reason',
        'URL',
    ]
    new_csv = old_csv.replace('.csv', '.new.csv')
    bancolombia_subs = get_customer_subs('bancolombia')

    with open(old_csv, 'r') as old_csv_handle:
        cache = {
            (row['subscription'], row['finding id']): row
            for row in csv.DictReader(f=old_csv_handle, fieldnames=fieldnames)
        }

    with open(new_csv, 'w') as new_csv_handle:
        writer = csv.DictWriter(new_csv_handle, fieldnames=fieldnames)
        writer.writeheader()

        with Pool(processes=cpu_count() * 8) as worker:
            rows = tuple(
                row
                for row in worker.starmap(
                    process_exp,
                    zip(repeat(bancolombia_subs),
                        repeat(cache),
                        glob.glob('subscriptions/*/forces/*/*/*.exp')))
                if row is not None)

        for row in rows:
            writer.writerow(row)


def process_exploit(exp_path: str):
    """
    Get all the information from an exploit.

    :param exp_path: Exploit path.

    :rtype: :class:`ExploitInfo`
    """
    result = None
    reason = ''
    subs = exp_path.split('/')[1]
    exp_type = exp_path.split('/')[3]

    exp_kind, finding_id = helper.forces.scan_exploit_for_kind_and_id(exp_path)

    if exp_kind == 'cannot.exp':
        reason_pattern = r'(?::\s*(.*))'
        with open(exp_path, 'r') as reader:
            reader.readline()
            reason_line = reader.readline()
            search_r = re.search(reason_pattern, reason_line)
            if search_r and len(search_r.groups()) >= 1:
                reason = search_r.groups()[0]

    if helper.integrates.does_finding_exist(finding_id):
        score = helper.integrates.get_finding_cvss_score(finding_id)
        title = helper.integrates.get_finding_title(finding_id)

        url = ('https://fluidattacks.com/integrates/dashboard#!/'
               f'project/{subs}/findings/{finding_id}/evidence')
        status = ('accepted' if 'accepted' in exp_path else
                  ('open' if helper.integrates.is_finding_open(
                      finding_id=finding_id,
                      finding_types=(constants.SAST if exp_type == 'static'
                                     else constants.DAST)) else 'closed'))
        result = ExploitInfo(
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


def process_subscription_exploits(subs: dict) -> List:
    """
    Process all exploits of a subscription.

    :param subscription: Subscription configuration.

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
                             subscription: str = None):
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
                        subscription and subs['name'] != subscription):
                continue

            logger.info(f'Filling with mocks {subs["name"]}')
            with utils.generic.output_block(indent=4):
                toolbox.fill_with_mocks(subs['name'])

            logger.info(f'Gererating report for {subs["name"]}')
            info = process_subscription_exploits(subs)
            for row in info:
                writer.writerow(row._asdict())
