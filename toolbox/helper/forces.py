# Standard library
import functools
import os

# Third party libraries
import ruamel.yaml as yaml

# Local libraries
from toolbox import (
    constants,
    logger,
)


def get_forces_configuration(subs: str) -> dict:
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
def scan_exploit_for_kind_and_id(exploit_path: str) -> tuple:
    """Scan the exploit in search of metadata."""
    # /fin-1234-567890.exp        -> 567890, 'exp'
    # /fin-1234-567890.mock.exp   -> 567890, 'mock.exp'
    # /fin-1234-567890.cannot.exp -> 567890, 'cannot.exp'
    exploit_kind, finding_id = '', ''
    re_match = constants.RE_EXPLOIT_NAME.search(exploit_path)
    if re_match:
        finding_id, exploit_kind = re_match.groups()
    else:
        logger.warn('no kind or id found in', exploit_path)
    return exploit_kind, finding_id
