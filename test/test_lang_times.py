# -*- coding: utf-8 -*-

"""Test execution times of many Asserts methods."""

# standard imports
from time import perf_counter
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('lang')

# local imports
from fluidasserts.lang import core, java


# Constants
JAVA: str = 'test/times/rxjava/src/main/java/io/reactivex/rxjava3'
MARKD: str = 'test/times/rxjava/docs'

TIME_ZERO: float = 0.0
TIME_NOTHING_TESTED: float = 0.1

COMMON_TEXT: str = 'a'
UNCOMMON_TEXT: str = 'abc$%^#def'

LSPECS_MD = {
    'extensions': ('md',)
}

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
    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_text(JAVA, COMMON_TEXT, exclude=[JAVA])

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
        java.has_generic_exceptions(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_generic_exceptions(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_null_pointer_exception(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_runtime_exception(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_print_stack_trace(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.swallows_exceptions(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.does_not_handle_exceptions(JAVA, should_have=[], exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_switch_without_default(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_insecure_randoms(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_if_without_else(JAVA, conditions=[], exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_insecure_cipher(JAVA, 'DES', exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_insecure_hash(JAVA, 'MD5', exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_md5_hash(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_sha1_hash(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_des_algorithm(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_log_injection(JAVA, exclude=[JAVA])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_system_exit(JAVA, exclude=[JAVA])


def test_lang_specs_parameter():
    """Test checks configured to test nothing due to lang_specs parameter."""
    # Checks below will be skiped because
    #   the lang_specs is pointing to .md files
    #   and the directory is full of .java files
    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        core.has_text(JAVA, COMMON_TEXT, lang_specs=LSPECS_MD)

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
        java.has_generic_exceptions(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_generic_exceptions(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_null_pointer_exception(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_runtime_exception(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_print_stack_trace(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.swallows_exceptions(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.does_not_handle_exceptions(MARKD, should_have=[])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_switch_without_default(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_insecure_randoms(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_if_without_else(MARKD, conditions=[])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_insecure_cipher(MARKD, 'DES')

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_insecure_hash(MARKD, 'MD5')

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_md5_hash(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_sha1_hash(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_des_algorithm(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_log_injection(MARKD)

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_system_exit(MARKD)
