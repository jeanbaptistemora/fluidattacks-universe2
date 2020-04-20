# Local libraries
from toolbox.generic.commit import (
    has_short_line_length,
    is_valid_summary,
    VALID_SCOPES,
    VALID_TYPES,
)


def test_is_valid_summary():
    for type_ in VALID_TYPES:
        for scope in VALID_SCOPES:
            assert is_valid_summary(f'{type_}({scope}): #123.1 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): # test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #0 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #1.0 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #0.0 test this, now')
            assert not is_valid_summary(f'{scope}({type_}): #123.1 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #123 test this, now')
            assert not is_valid_summary(f'{type_}({scope}): #123 test2 this, now')
            assert not is_valid_summary(f'{type_}({scope}): #123  test2 this, now')
            assert not is_valid_summary(f'{type_}({scope}):  #123 test2 this, now')
            assert not is_valid_summary(f'{type_}({scope}):  $123 test2 this, now')
            assert not is_valid_summary(f' {type_}({scope}): #123.1 test this, nw')


def test_has_short_line_length():
    assert has_short_line_length('s' * 50, 'b' * 72)
    assert not has_short_line_length('s' * 51, 'b' * 72)
    assert not has_short_line_length('s' * 50, 'b' * 73)

    assert has_short_line_length('s', 'b' * 72 + '\n' + 'b' * 72)
    assert not has_short_line_length('s', 'b' * 73 + '\n' + 'b' * 72)
    assert not has_short_line_length('s', 'b' * 72 + '\n' + 'b' * 73)
