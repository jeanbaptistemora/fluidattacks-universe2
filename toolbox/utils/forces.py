# Standard library
import functools
import os
import re
from typing import Tuple

# Third party libraries
import ruamel.yaml as yaml

# Local libraries
from toolbox import (
    logger,
)


def get_config(subs: str) -> dict:
    """Scans the group configuration file and returns a dict."""
    config_path: str = f'subscriptions/{subs}/config/config.yml'
    config: dict = {
        'schedules': {
            'synchronization': {
                'dynamic': {
                    'run': False,
                },
                'static': {
                    'run': False,
                },
            },
        },
    }

    if os.path.exists(config_path):
        with open(config_path) as config_handle:
            config_obj = yaml.safe_load(config_handle)

        if 'forces' in config_obj:
            config['schedules']['synchronization']['dynamic'] = \
                config_obj['forces']['schedules']['synchronization']['dynamic']
            config['schedules']['synchronization']['static'] = \
                config_obj['forces']['schedules']['synchronization']['static']

    return config


@functools.lru_cache(maxsize=None, typed=True)
def scan_exploit_for_kind_and_id(exploit_path: str) -> Tuple[str, str]:
    """Scan the exploit in search of metadata."""
    # /567890.exp        -> 567890, 'exp'
    # /567890.mock.exp   -> 567890, 'mock.exp'
    # /567890.cannot.exp -> 567890, 'cannot.exp'
    exploit_kind, finding_id = '', ''
    re_match = re.search(r'/(\d+)\.(exp|mock.exp|cannot.exp)$', exploit_path)
    if re_match:
        finding_id, exploit_kind = re_match.groups()
    else:
        logger.warn('no kind or id found in', exploit_path)
    return exploit_kind, finding_id
