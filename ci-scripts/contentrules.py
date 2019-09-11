#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script that defines the rules to be applied to the web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.3
Patch notes 1.3:
- Externalize repetitive checks
- Fully comply with pylint(10/10)
"""

import os
import print_helper as ph
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
        ph.print_failure("Issue found in "+path+"\n")
        ph.print_failure(out)
        ph.print_warning("\nMultiple main titles defined. "\
                         "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that there are exactly 6 keywords
    out = os.popen("pcregrep -o '(?<=^:keywords:).*' "+path).read()
    out = out.replace('\n', '').replace(' ', '').split(",")
    if len(out) != 6:
        ph.print_failure("Issue found in "+path)
        ph.print_warning("\nThere must be exactly 6 keywords. "\
                         "Please correct the file and try again.\n\n")
        exit_code = 1

    # Check that every keyword starts with uppercase
    for keywd in out:
        if keywd == "":
            ph.print_failure("Issue found in "+path+"\n")
            ph.print_warning("Keywords cannot be empty\n\n")
            exit_code = 1
        elif not keywd[0].isupper():
            ph.print_failure("Issue found in "+path+"\n")
            ph.print_warning("The keyword "+keywd+" is not in Title case.\n\n")
            exit_code = 1

    #Check that every URL starts with link:
    os.system("sh exttxt.sh "+path+">> temp.txt")
    out = os.popen("pcregrep '(\\s|\\w|^|\\()http(s)?://' temp.txt").read()
    if out:
        ph.print_failure("Issue found in "+path+"\n")
        ph.print_failure(out)
        ph.print_warning("URLs must start with \'link:\'. "\
                         "Please correct the file and try again.\n\n")
        exit_code = 1

    #Check that every URL has a short name between brackets:
    out = os.popen("pcregrep 'link:http(s)?://' temp.txt").read()
    if out:
        ph.print_failure("Issue found in "+path+"\n")
        ph.print_failure(out)
        ph.print_warning("URLs must have a short name between brackets. "\
                         "Please correct the file and try again.\n\n")
        exit_code = 1

    # Check if source adoc has content past the 80th column
    out = os.popen("pcregrep -nu '.{81,}' temp.txt").read()
    os.system('rm -r temp.txt')
    if out:
        ph.print_failure("Issue found in "+path+"\n")
        ph.print_failure(out)
        ph.print_warning("Documents must be wrapped at column 80. \n\n")
        exit_code = 1

    #  Many other repetitive checks from the dictionary:
    for regex, message in CONTENTRULES.items():
        out = os.popen(regex +"  "+ path).read()
        if out:
            ph.print_failure("Issue found in "+path+"\n")
            ph.print_failure(out)
            ph.print_warning(message+"\n\n")
            exit_code = 1

    return exit_code
