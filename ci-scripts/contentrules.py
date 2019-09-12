#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script that defines the rules to be applied to the web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.4
Patch notes 1.4:
- Using a function to print error messages
- Fixed source code false positives bug
"""

import os
from print_helper import error_print
from rules import CONTENTRULES

def rulechecker(path, exit_code):
    """
    Define Rules for web content
    """

    # Check for multiple main title
    out = os.popen("pcregrep -nr '^=\\s.*$' "+path).read()
    out = out.split('\n')
    out = list(filter(None, out))
    if len(out) > 1:
        message = "\nMultiple main titles defined. "
        error_print(path, out, message)
        exit_code = 1

    # Check that there are exactly 6 keywords
    out = os.popen("pcregrep -o '(?<=^:keywords:).*' "+path).read()
    out = out.replace('\n', '').replace(' ', '').split(",")
    if len(out) != 6:
        message = "There must be exactly 6 keywords."
        error_print(path, '', message)
        exit_code = 1

    # Check that every keyword starts with uppercase
    for keywd in out:
        if keywd == "":
            message = "Keywords cannot be empty"
            error_print(path, '', message)
            exit_code = 1
        elif not keywd[0].isupper():
            message = "The keyword "+keywd+" is not in Title case."
            error_print(path, '', message)
            exit_code = 1

    # Check if first source code has title
    has_source = os.popen("pcregrep '\\[source' "+ path).read()
    if has_source:
        out = os.popen("pcregrep -ML '^\\..*\n\\[source' " + path).read()
        if out:
            message = "The first code block of an article must have a title. "
            error_print(path, '', message)

    #Check that every URL starts with link:
    os.system("sh exttxt.sh "+path+">> temp.txt")
    out = os.popen("pcregrep '(\\s|\\w|^|\\()http(s)?://' temp.txt").read()
    if out:
        message = "URLs must start with \'link:\'. "
        error_print(path, out, message)
        exit_code = 1

    #Check that every URL has a short name between brackets:
    out = os.popen("pcregrep 'link:http(s)?://' temp.txt").read()
    if out:
        message = "URLs must have a short name between brackets."
        error_print(path, out, message)
        exit_code = 1

    # Check if source adoc has content past the 80th column
    out = os.popen("pcregrep -nu '.{81,}' temp.txt").read()
    os.system('rm -r temp.txt')
    if out:
        message = "Documents must be wrapped at column 80."
        error_print(path, out, message)
        exit_code = 1

    #  Many other repetitive checks from the dictionary:
    for regex, message in CONTENTRULES.items():
        out = os.popen(regex +"  "+ path).read()
        if out:
            error_print(path, out, message)
            exit_code = 1

    return exit_code
