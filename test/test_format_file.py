# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.format.file."""

# standard imports

# local imports
from fluidasserts.format import file


# Constants

COMPILED_BINARY: str = 'test/static/format/file/open'
COMPILED_BINARY_1: str = 'test/static/format/file/open/MyJar.jar'
COMPILED_BINARY_2: str = 'test/static/format/file/open/MyJar.class'
COMPILED_BINARY_3: str = 'test/static/format/file/open/open'


TEXT_FILE: str = 'test/static/format/file/closed'
TEXT_FILE_1: str = 'test/static/format/file/closed/MyJar.java'
TEXT_FILE_2: str = 'test/static/format/file/closed/MyJar.jar'
TEXT_FILE_3: str = 'test/static/format/file/closed/closed_1'

NO_FILE: str = 'test/static/format/file/not-exists'

#
# Open tests
#


def test_has_compiled_binaries_open():
    """Test has_compiled_binaries."""
    assert file.has_compiled_binaries(COMPILED_BINARY).is_open()
    assert file.has_compiled_binaries(COMPILED_BINARY_1).is_open()
    assert file.has_compiled_binaries(COMPILED_BINARY_2).is_open()


#
# Closing tests
#


def test_has_compiled_binaries_closed():
    """Test has_compiled_binaries."""
    assert file.has_compiled_binaries(TEXT_FILE_1).is_closed()
    assert file.has_compiled_binaries(TEXT_FILE_2).is_closed()
    assert file.has_compiled_binaries(TEXT_FILE_3).is_closed()

    assert file.has_compiled_binaries(
        TEXT_FILE, exclude=['test']).is_closed()
    assert file.has_compiled_binaries(
        COMPILED_BINARY, exclude=['test']).is_closed()


#
# Unknown tests
#


def test_has_compiled_binaries_unknown():
    """Test has_compiled_binaries."""
    assert file.has_compiled_binaries(NO_FILE).is_unknown()
