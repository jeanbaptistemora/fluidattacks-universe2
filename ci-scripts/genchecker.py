#!/usr/bin/env python3
# coding: utf8

"""
Script to run general content checks of web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.5
Patch notes 1.5:
- Use error_print function
"""

import os
from print_helper import error_print
from rules import GENCHECKS

def genchecks(exit_code):
    """
    General checks to run just once:
    """

    # Repetitive checks from the dictionary:
    for check, message in GENCHECKS.items():
        out = os.popen(check).read()
        if out:
            error_print("", out, message)
            exit_code = 1

    return exit_code
