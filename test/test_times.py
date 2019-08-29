# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.java."""

# standard imports
from time import perf_counter
from contextlib import contextmanager

# 3rd party imports
# None

# local imports
from fluidasserts.lang import java


# Constants
CODE: str = 'test_times_rxjava/src/main/java/io/reactivex/rxjava3/core'
TIME_ZERO: float = 0.0
TIME_NOTHING_TESTED: float = 0.25

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


def test_nothing_tested():
    """Test nothing happens."""
    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_generic_exceptions(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_generic_exceptions(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_null_pointer_exception(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_catch_for_runtime_exception(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_print_stack_trace(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.swallows_exceptions(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.does_not_handle_exceptions(CODE, should_have=[], exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_switch_without_default(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_insecure_randoms(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_if_without_else(CODE, conditions=[], exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_insecure_cipher(CODE, 'DES', exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_insecure_hash(CODE, 'MD5', exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_md5_hash(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_sha1_hash(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_des_algorithm(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.has_log_injection(CODE, exclude=[CODE])

    with assert_times_between(TIME_ZERO, TIME_NOTHING_TESTED):
        java.uses_system_exit(CODE, exclude=[CODE])
