# Standard library
import re
import csv
import glob
from multiprocessing import Pool, cpu_count
from typing import List
from itertools import repeat
from concurrent.futures.thread import ThreadPoolExecutor
from collections import namedtuple

# Third parties libraries
import ruamel.yaml as yaml

# Local imports
from toolbox import constants, helper, logger, toolbox, utils


ExploitInfo = namedtuple(
    'ExploitInfo', ('subscription', 'integrates_status', 'kind', 'type',
                    'score', 'finding_id', 'finding_title', 'url', 'customer'))


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
        subs, exp_type = re.match(pattern=r'^\w+/(\w+)/break-build/(\w+)',
                                  string=exp_path).groups()

        if subs not in customer_subs:
            return None

        exp_kind, fin_id = toolbox.scan_exploit_for_kind_and_id(exp_path)

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
                        glob.glob('subscriptions/*/break-build/*/*/*.exp')))
                if row is not None)

        for row in rows:
            writer.writerow(row)


def process_exploit(exp_path: str):
    """
    Get all the information from an exploit.

    :param exp_path: Exploit path.

    :rtype: :class:`ExploitInfo`
    """
    subs = exp_path.split('/')[1]
    exp_type = exp_path.split('/')[3]

    exp_kind, finding_id = toolbox.scan_exploit_for_kind_and_id(exp_path)

    score = helper.integrates.get_finding_cvss_score(finding_id)
    title = helper.integrates.get_finding_title(finding_id)

    url = (f'https://fluidattacks.com/integrates/dashboard#!/'
           f'project/{subs}/findings/{finding_id}/evidence')
    status = ('accepted' if 'accepted' in exp_path else
              ('open' if helper.integrates.is_finding_open(
                  finding_id=finding_id,
                  finding_types=(constants.SAST if exp_type == 'static' else
                                 constants.DAST)) else 'closed'))
    return ExploitInfo(subs, status, exp_kind, exp_type, score, finding_id,
                       title, url, None)


def process_subscription_exploits(subs: dict) -> List:
    """
    Process all exploits of a subscription.

    :param subscription: Subscription configuration.

    :rtype: :class:`List[ExploitInfo]`
    """
    result = []
    with ThreadPoolExecutor(max_workers=cpu_count() * 8) as executor:
        for exploit in executor.map(process_exploit,
                                    utils.iter_exploit_paths(subs['name'])):
            exploit = exploit._replace(customer=subs['customer'])
            result.append(exploit)
    return result


def generate_exploits_report():
    """
    Generate a report of all exploits.
    """
    result = []
    for subs in utils.iter_subscritions_config():
        if not toolbox.has_break_build(subs['name']):
            continue

        result.append(process_subscription_exploits(subs))
