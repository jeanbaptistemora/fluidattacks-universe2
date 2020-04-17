# Local libraries
from toolbox.drills.commit import (
    is_valid_msg,
    is_drills_commit,
)


def test_is_drills_commit():
    assert is_drills_commit('drills(lines)')
    assert is_drills_commit('drills(xxxxx)')
    assert not is_drills_commit('style(cross)')
    assert not is_drills_commit('feat(lines)')


def test_is_valid_msg():
    assert is_valid_msg('drills(lines)')
    assert is_valid_msg('drills(xxxxx)')
    assert not is_valid_msg('style(cross)')
    assert not is_valid_msg('feat(lines)')
