# Local libraries
from toolbox.forces.commit import (
    is_valid_msg,
    is_exploits_commit,
)


def test_is_exploits_commit():
    assert is_exploits_commit('feat(exp)')
    assert is_exploits_commit('xx(exp)')
    assert not is_exploits_commit('style(cross)')
    assert not is_exploits_commit('drills(lines)')


def test_is_valid_msg():
    assert is_valid_msg('feat(exp): continuoustest')
    assert is_valid_msg('perf(exp): continuoustest')
    assert is_valid_msg('xxxx(exp): continuoustest')
    assert not is_valid_msg('feat(job): continuoustest')

    assert is_valid_msg('fix(exp): #123 continuoustest asserts-ch')
    assert is_valid_msg('fix(exp): #123 continuoustest asserts-fn')
    assert is_valid_msg('fix(exp): #123 continuoustest asserts-fp')
    assert is_valid_msg('fix(exp): #123 continuoustest service-logic')
    assert is_valid_msg('fix(exp): #123 continuous toe-availability')
    assert is_valid_msg('fix(exp): #123 continuoustest toe-location')
    assert is_valid_msg('fix(exp): #123 continuoustest toe-resource')
    assert not is_valid_msg('fix(exp): #123 continuoustest reason-x')
    assert not is_valid_msg('fix(exp): # continuoustest toe-resource')
    assert not is_valid_msg('fix(exp): continuoustest toe-resource')
    assert not is_valid_msg('xxxx(exp): #123 continuoustest reason-x')
    assert not is_valid_msg('xxxx(exp): # continuoustest toe-resource')
    assert not is_valid_msg('xxxx(exp): continuoustest toe-resource')
