# Local libraries
from toolbox.forces.quality import (
    is_commit_msg_valid,
)


def test_is_commit_msg_valid():
    assert is_commit_msg_valid('feat(exp): continuoustest')
    assert is_commit_msg_valid('perf(exp): continuoustest')
    assert is_commit_msg_valid('xxxx(exp): continuoustest')
    assert not is_commit_msg_valid('feat(job): continuoustest')

    assert is_commit_msg_valid('fix(exp): #123 continuoustest asserts-ch')
    assert is_commit_msg_valid('fix(exp): #123 continuoustest asserts-fn')
    assert is_commit_msg_valid('fix(exp): #123 continuoustest asserts-fp')
    assert is_commit_msg_valid('fix(exp): #123 continuoustest service-logic')
    assert is_commit_msg_valid('fix(exp): #123 continuous toe-availability')
    assert is_commit_msg_valid('fix(exp): #123 continuoustest toe-location')
    assert is_commit_msg_valid('fix(exp): #123 continuoustest toe-resource')
    assert not is_commit_msg_valid('fix(exp): #123 continuoustest reason-x')
    assert not is_commit_msg_valid('fix(exp): # continuoustest toe-resource')
    assert not is_commit_msg_valid('fix(exp): continuoustest toe-resource')
    assert not is_commit_msg_valid('xxxx(exp): #123 continuoustest reason-x')
    assert not is_commit_msg_valid('xxxx(exp): # continuoustest toe-resource')
    assert not is_commit_msg_valid('xxxx(exp): continuoustest toe-resource')
