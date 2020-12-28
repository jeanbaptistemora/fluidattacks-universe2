# Local libraries
from toolbox.drills.to_reattack import (
    to_reattack
)


def test_drills_to_reattack(relocate):
    data: list = to_reattack('continuoustest')['projects_info']

    assert data[0]['name'] == 'continuoustest'
    assert data[0]['findings'][0]['url'] == 'https://integrates.fluidattacks.com/groups/continuoustest/vulns/508273958'
    assert len(data[0]['findings'][0]['vulnerabilities']) == 2
