# Local libraries
from toolbox.drills.to_reattack import (
    to_reattack
)

EXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/508273958'
UNEXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/975673437'

def test_drills_to_reattack():
    message: str = to_reattack('continuoustest')
    assert EXPECTED_URL in message
    assert UNEXPECTED_URL not in message
