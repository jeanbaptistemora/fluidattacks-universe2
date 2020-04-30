# Local libraries
from toolbox.drills.to_reattack import (
    to_reattack
)

EXP_EXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/508273958'
EXP_UNEXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/975673437'

NO_EXP_EXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/710340580'
NO_EXP_UNEXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/975673437'

def test_drills_to_reattack(relocate):
    exp_message: str = to_reattack('continuoustest', True)[0]
    no_exp_message: str = to_reattack('continuoustest', False)[0]
    assert EXP_EXPECTED_URL in exp_message
    assert EXP_UNEXPECTED_URL not in exp_message
    assert NO_EXP_EXPECTED_URL in no_exp_message
    assert NO_EXP_UNEXPECTED_URL not in no_exp_message
