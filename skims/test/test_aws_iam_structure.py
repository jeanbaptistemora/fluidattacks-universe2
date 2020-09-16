# Local libraries
from aws.iam.structure import (
    is_action_permissive,
)


def test_is_action_permissive() -> None:
    assert is_action_permissive('*')
    assert is_action_permissive('s3:*')
    assert is_action_permissive('s3*')
    assert is_action_permissive('s3*:*')
    assert is_action_permissive('s3******:*')

    assert not is_action_permissive('s3:')
    assert not is_action_permissive('s3:xx')
    assert not is_action_permissive('s3:xx*')
    assert not is_action_permissive('s3:x*x*')
    assert not is_action_permissive('s3*:')
    assert not is_action_permissive('s3***:')

    assert not is_action_permissive(None)  # type: ignore
    assert not is_action_permissive({})  # type: ignore
    assert not is_action_permissive([])  # type: ignore
