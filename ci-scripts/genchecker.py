#!/usr/bin/env python3
# coding: utf8

"""
Script to run general content checks of web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.1
Patch notes 1.1:
- Using Python3
"""

import os
import print_helper

def genchecks(EXIT_CODE):
    #General checks to run just once:

    # Check there are not any articles with the .asc extension
    OUT = os.popen("find content -iname '*.asc' | grep -E './.*'").read()
    if len(OUT) > 0:
      print_helper.print_failure(OUT)
      print_helper.print_warning("Extension \".asc\" is no longer supported. "\
                                 "Please correct the file and try again\n\n")
      EXIT_CODE = 1

    # Check that names do not have underscore
    OUT = os.popen("find content -iname '*_*' | grep -E './.*'").read()
    if len(OUT) > 0:
      print_helper.print_failure(OUT)
      print_helper.print_warning("Use hyphen '-' instead of underscore '_' "\
                                 "for filenames. "\
                                 "Please correct the file and try again\n\n")
      EXIT_CODE = 1

    # Check no uppercase characters are used in the filenames
    OUT = os.popen("find content | grep -E '.*[A-Z].*'").read()
    if len(OUT) > 0:
      print_helper.print_failure(OUT)
      print_helper.print_warning("Filenames must always be lowercase. "\
                                 "Please correct the file and try again\n\n")
      EXIT_CODE = 1

    #Check that there are no spaces in filenames
    OUT = os.popen("find content -iname '* *' | grep -E './.*'").read()
    if len(OUT) > 0:
      print_helper.print_failure(OUT)
      print_helper.print_warning("Filenames must not have spaces in them, "\
                                 "use hyphen \"-\" instead. "\
                                 "Please correct the file and try again\n\n")
      EXIT_CODE = 1

    return EXIT_CODE
