# Standard library
import contextlib
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


def get_integrates_exploit_justification(exploit_path: str) -> str:
    justification: str = \
        'We are working on this exploit! This is an Integrates exploit for now'

    if os.path.exists(exploit_path) and '.reason' in exploit_path:
        with open(exploit_path) as exploit_handle:
            with contextlib.suppress(yaml.error.YAMLError):
                exploit_content = yaml.safe_load(exploit_handle)
                justification = exploit_content['justification']

    return justification


def get_integrates_exploit_category(exploit_path: str) -> str:
    category: str = 'OTHER'

    if os.path.exists(exploit_path) and '.reason' in exploit_path:
        with open(exploit_path) as exploit_handle:
            with contextlib.suppress(yaml.error.YAMLError):
                exploit_content = yaml.safe_load(exploit_handle)
                category = exploit_content['category']

    return category


@functools.lru_cache(maxsize=None, typed=True)
def scan_exploit_for_kind_and_id(exploit_path: str) -> Tuple[str, str]:
    """Scan the exploit in search of metadata."""
    # /567890.exp            -> 567890, 'exp'
    # /567890.integrates.exp -> 567890, 'integrates.exp'
    # /567890.reason.exp     -> 567890, 'reason.exp'
    exploit_kind, finding_id = '', ''
    re_match = \
        re.search(r'/(\d+)\.(exp|integrates.exp|reason.exp)$', exploit_path)

    if re_match:
        finding_id, exploit_kind = re_match.groups()
    else:
        logger.warn('no kind or id found in', exploit_path)
    return exploit_kind, finding_id
