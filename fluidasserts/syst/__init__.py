# -*- coding: utf-8 -*-

"""Fluid Asserts syst module."""

# standard imports
from typing import List

# local imports
from fluidasserts import Unit, OPEN, CLOSED


def _get_result_as_tuple(*,
                         system: str, host: str,
                         msg_open: str, msg_closed: str,
                         open_if: bool) -> tuple:
    """Return the tuple version of the Result object."""
    units: List[Unit] = [
        Unit(where=f'{system}://{host}',
             specific=[msg_open if open_if else msg_closed])]

    if open_if:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units
