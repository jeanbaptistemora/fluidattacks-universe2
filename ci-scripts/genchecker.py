#!/usr/bin/env python3
# coding: utf8

"""
Script to run general content checks of web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.3
Patch notes 1.4:
- Create dictionary for repetitive checks
"""

import os
import print_helper as ph
from rules import GENCHECKS

def genchecks(exit_code):
    """
    General checks to run just once:
    """

    # Repetitive checks from the dictionary:
    for check, message in GENCHECKS.items():
        out = os.popen(check).read()
        if out:
            ph.print_failure(out)
            ph.print_warning(message+"\n\n")
            exit_code = 1

    return exit_code
