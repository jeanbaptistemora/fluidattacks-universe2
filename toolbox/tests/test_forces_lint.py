# Local imports
from toolbox.forces.lint import (
    many_exploits_by_change_request,
    many_exploits_by_subs_and_filter,
)

# Constants
SUBS: str = 'continuoustest'


def test_many_exploits_by_change_request(relocate):
    assert many_exploits_by_change_request('09f574ed')


def test_many_exploits_by_subs_and_filter(relocate):
    assert many_exploits_by_subs_and_filter(SUBS, filter_str='')
