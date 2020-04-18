# Local libraries
from toolbox.drills.findings_pending_to_verify import (
    findings_pending_to_verify
)

EXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/508273958'
UNEXPECTED_URL: str = 'https://fluidattacks.com/integrates/dashboard#!/project/continuoustest/975673437'

def test_drills_findings_pending_to_verify():
    message: str = findings_pending_to_verify('continuoustest')
    assert EXPECTED_URL in message
    assert UNEXPECTED_URL not in message
