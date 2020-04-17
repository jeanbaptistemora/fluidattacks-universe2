# Local libraries
from toolbox.drills.commit import (
    is_valid_msg,
    is_drills_commit,
    VALID_SCOPES,
    VALID_TYPES,
)


def test_is_drills_commit():
    assert is_drills_commit('drills(lines)')
    assert is_drills_commit('drills(xxxxx)')
    assert not is_drills_commit('style(cross)')
    assert not is_drills_commit('feat(lines)')


def test_is_valid_msg():
    assert is_valid_msg('drills(lines): test - 72.75%, 0 el, 6 ei')
    assert is_valid_msg('drills(inputs): test - 72.75%, 0 el, 6 ei')
    assert is_valid_msg('drills(cross): test - 72.75%, 0 el, 6 ei')
    assert not is_valid_msg('drills(cross): test 72.75%, 0 el, 6 ei')
    assert not is_valid_msg('drills(cross): test - 72.7%, 0 el, 6 ei')
    assert not is_valid_msg('drills(cross): test - 72.75, 0 el, 6 ei')
    assert not is_valid_msg('drills(cross): test - 72.75%,  0 el, 6 ei')
    assert not is_valid_msg('drills(cross): test - 72.75%,  0 el, 6 ei')
    assert not is_valid_msg('drills(cross): test - 72.75%,  0 el 6 ei')
    assert not is_valid_msg('drills(cross): test - 72.75%, 0 el, 6 e')
    assert not is_valid_msg('drills(cross): t st - 72.75%, 0 el, 6 ei')

    assert is_valid_msg('drills(enum): test - 0 nl, 3 ni')
    assert not is_valid_msg('drills(enum): t st - 0 nl, 3 ni')
    assert not is_valid_msg('drills(enum): test  0 nl, 3 ni')
    assert not is_valid_msg('drills(enum): test -  nl, 3 ni')
    assert not is_valid_msg('drills(enum): test - 0 l, 3 ni')
    assert not is_valid_msg('drills(enum): test - 0 nl 3 ni')
    assert not is_valid_msg('drills(enum): test - 0 nl, ni')
    assert not is_valid_msg('drills(enum): test - 0 nl, 3i')
    assert not is_valid_msg('drills(enum): test -0 nl, 3 ni')
    assert not is_valid_msg('drills(enum): test- 0 nl, 3 ni')
    assert not is_valid_msg('drills(enum): test - 0 nl, 3 ni ')

    assert is_valid_msg('drills(conf): test - comment, continued')
    assert not is_valid_msg('drills(conf): test - comm|ent, continued')
    assert not is_valid_msg('drills(conf): test - comm|ent, continued.')
    assert not is_valid_msg('drills(conf): test - comm|ent, continued2')
