#!/usr/bin/env python3
# coding: utf8

"""
Script to run general content checks of web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.2
Patch notes 1.2:
- Comply with pylint
"""

import os
import print_helper

def genchecks(exit_code):
    """
    General checks to run just once:
    """

    # Check there are not any articles with the .asc extension
    out = os.popen("find content -iname '*.asc' | grep -E './.*'").read()
    if out:
        print_helper.print_failure(out)
        print_helper.print_warning("Extension \".asc\" is no longer supported. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that names do not have underscore
    out = os.popen("find content -iname '*_*' | grep -E './.*'").read()
    if out:
        print_helper.print_failure(out)
        print_helper.print_warning("Use hyphen '-' instead of underscore '_' "\
                                   "for filenames. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check no uppercase characters are used in the filenames
    out = os.popen("find content | grep -E '.*[A-Z].*'").read()
    if out:
        print_helper.print_failure(out)
        print_helper.print_warning("Filenames must always be lowercase. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    #Check that there are no spaces in filenames
    out = os.popen("find content -iname '* *' | grep -E './.*'").read()
    if out:
        print_helper.print_failure(out)
        print_helper.print_warning("Filenames must not have spaces in them, "\
                                   "use hyphen \"-\" instead. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    return exit_code
