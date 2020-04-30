# Local libraries
from toolbox.utils.forces import (
    get_config,
)

# Constants
SUBS: str = 'continuoustest'
SUBS_BAD: str = 'not-existing-group'


def test_get_config(relocate):
    assert get_config(SUBS) == {
        'schedules': {
            'synchronization': {
                'dynamic': {
                    'run': True,
                },
                'static': {
                    'run': True,
                },
            },
        },
    }
    assert get_config(SUBS_BAD) == {
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
