# -*- coding: utf-8 -*-

"""Test execution times of many Asserts methods."""


from contextlib import (
    contextmanager,
)
import pytest
from time import (
    perf_counter,
)

pytestmark = pytest.mark.asserts_module("lang_times")


from fluidasserts.lang import (
    core,
    java,
)

# Constants
JAVA: str = "test/times/rxjava/src/main/java/io/reactivex/rxjava3"
MARKD: str = "test/times/rxjava/docs"

TIME_ZERO: float = 0.0
# The build system introduce overhead
TIME_NOTHING_TESTED: float = 1.0

COMMON_TEXT: str = "a"
UNCOMMON_TEXT: str = "abc$%^#def"

LSPECS_MD = {"extensions": ("md",)}

# Context managers


@contextmanager
def assert_times_between(min_time: float, max_time: float) -> None:
    """Wrap a block of code and raise if the time is not between boundaries."""
    time_start: float = perf_counter()
    try:
        yield
    finally:
        time_end: float = perf_counter()
        assert min_time <= (time_end - time_start) <= max_time


#
# Tests
#


def test_exclude_parameter():
    """Test checks configured to test nothing due to the exclude parameter."""
    open_message = "text found in code."
    closed_message = "text not found in code."
    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_text(
            JAVA, COMMON_TEXT, open_message, closed_message, exclude=[JAVA]
        )

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_not_text(JAVA, UNCOMMON_TEXT, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_all_text(JAVA, [COMMON_TEXT], exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_any_text(JAVA, [COMMON_TEXT], exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_not_any_text(JAVA, [UNCOMMON_TEXT], exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_weak_cipher(JAVA, COMMON_TEXT, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_secret(JAVA, COMMON_TEXT, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_any_secret(JAVA, [COMMON_TEXT], exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.uses_unencrypted_sockets(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_null_pointer_exception(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_insecure_randoms(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_log_injection(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_system_exit(JAVA, exclude=[JAVA])


def test_lang_specs_parameter():
    """Test checks configured to test nothing due to lang_specs parameter."""
    # Checks below will be skiped because
    #   the lang_specs is pointing to .md files
    #   and the directory is full of .java files
    open_message = "text found in code."
    closed_message = "text not found in code."
    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_text(
            JAVA,
            COMMON_TEXT,
            open_message,
            closed_message,
            lang_specs=LSPECS_MD,
        )

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_not_text(JAVA, UNCOMMON_TEXT, lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_all_text(JAVA, [COMMON_TEXT], lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_any_text(JAVA, [COMMON_TEXT], lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_not_any_text(JAVA, [UNCOMMON_TEXT], lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_weak_cipher(JAVA, COMMON_TEXT, lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_secret(JAVA, COMMON_TEXT, lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_any_secret(JAVA, [COMMON_TEXT], lang_specs=LSPECS_MD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.uses_unencrypted_sockets(JAVA, lang_specs=LSPECS_MD)

    # Checks below will be skiped because java searches for .java files
    # And the directory is full of .md files

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_null_pointer_exception(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_insecure_randoms(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_log_injection(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_system_exit(MARKD)
