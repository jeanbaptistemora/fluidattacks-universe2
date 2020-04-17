# Local libraries
from toolbox.forces.commit import (
    is_valid_summary,
    is_exploits_commit,
)


def test_is_exploits_commit():
    assert is_exploits_commit('feat(exp)')
    assert is_exploits_commit('xx(exp)')
    assert not is_exploits_commit('style(cross)')
    assert not is_exploits_commit('drills(lines)')


def test_is_valid_summary():
    assert is_valid_summary('feat(exp): continuoustest')
    assert is_valid_summary('perf(exp): continuoustest')
    assert is_valid_summary('xxxx(exp): continuoustest')
    assert not is_valid_summary('feat(job): continuoustest')

    assert is_valid_summary('fix(exp): #123 continuoustest asserts-ch')
    assert is_valid_summary('fix(exp): #123 continuoustest asserts-fn')
    assert is_valid_summary('fix(exp): #123 continuoustest asserts-fp')
    assert is_valid_summary('fix(exp): #123 continuoustest service-logic')
    assert is_valid_summary('fix(exp): #123 continuous toe-availability')
    assert is_valid_summary('fix(exp): #123 continuoustest toe-location')
    assert is_valid_summary('fix(exp): #123 continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): # continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): #0 continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): #00 continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): #001 continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): #010 continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): #123 continuoustest')
    assert not is_valid_summary('fix(exp): #123 continuoustest reason-x')
    assert not is_valid_summary('fix(exp): # continuoustest toe-resource')
    assert not is_valid_summary('fix(exp): continuoustest toe-resource')
    assert not is_valid_summary('xxxx(exp): #123 continuoustest reason-x')
    assert not is_valid_summary('xxxx(exp): # continuoustest toe-resource')
    assert not is_valid_summary('xxxx(exp): continuoustest toe-resource')
