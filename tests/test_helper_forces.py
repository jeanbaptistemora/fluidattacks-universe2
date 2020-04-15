# Local libraries
from toolbox.helper.forces import (
    get_forces_configuration,
)

# Constants
SUBS: str = 'continuoustest'
SUBS_BAD: str = 'not-existing-subscription'


def test_get_forces_configuration(relocate):
    assert get_forces_configuration(SUBS) == {
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
    assert get_forces_configuration(SUBS_BAD) == {
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
