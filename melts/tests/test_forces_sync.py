# Local imports
from toolbox.forces.sync import (
    _get_bb_aws_role_arns,
)

# Constants
SUBS: str = 'continuoustest'
SUBS_BAD: str = 'does-not-exist'


def test_many_exploits_by_change_request(relocate):
    assert _get_bb_aws_role_arns(SUBS) == (
        'arn:aws:iam::0123456789:role/fluid-audit-role',
        'arn:aws:iam::9876543210:role/fluid-audit-role',
    )
    assert _get_bb_aws_role_arns(SUBS_BAD) == ()
