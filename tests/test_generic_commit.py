# Local libraries
from toolbox.generic.commit import (
    is_valid_summary,
    VALID_SCOPES,
    VALID_TYPES,
)


def test_is_valid_summary():
    for type_ in VALID_TYPES:
        for scope in VALID_SCOPES:
            assert is_valid_summary(f'{type_}({scope}): #123.1 test this, now')
            assert not is_valid_summary(f'{scope}({type_}): #123.1 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #123 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #123 test2 this, now')
            assert not is_valid_summary(f'{type_}({scope}): #123  test2 this, now')
            assert not is_valid_summary(f'{type_}({scope}):  #123 test2 this, now')
            assert not is_valid_summary(f'{type_}({scope}):  $123 test2 this, now')
            assert not is_valid_summary(f' {type_}({scope}): #123.1 test this, nw')
