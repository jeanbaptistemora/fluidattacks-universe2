# Local libraries
from aws.iam.utils import (
    match_pattern,
)


def test_match_pattern() -> None:
    assert match_pattern('iam:PassRole', 'iam:PassRole')
    assert match_pattern('iam:PassR*', 'iam:PassRole')
    assert match_pattern('iam:Pass*', 'iam:PassRole')
    assert match_pattern('iam:P*', 'iam:PassRole')
    assert match_pattern('iam:*PassRole', 'iam:PassRole')
    assert match_pattern('iam:*PassR*', 'iam:PassRole')
    assert match_pattern('iam:*Pass*', 'iam:PassRole')
    assert match_pattern('iam:*P*', 'iam:PassRole')
    assert match_pattern('iam:*', 'iam:PassRole')
    assert match_pattern('iam*', 'iam:PassRole')
    assert match_pattern('*:PassRole', 'iam:PassRole')
    assert match_pattern('*:*Pass*', 'iam:PassRole')
    assert match_pattern('*', 'iam:PassRole')
    assert match_pattern('.*', '.iam:PassRole')

    assert not match_pattern('a*', 'iam:PassRole')
    assert not match_pattern('iam', 'iam:PassRole')
    assert not match_pattern('iam:PassRol', 'iam:PassRole')

    # Ensure symbolic chars in a regex context are properly escaped
    assert not match_pattern('.', 'x')
    assert not match_pattern('iam:PassRol.', 'iam:PassRole')
    assert not match_pattern('iam:Pa.sRol.', 'iam:PassRole')
    assert not match_pattern('............', 'iam:PassRole')
    assert not match_pattern('.*', 'iam:PassRole')
