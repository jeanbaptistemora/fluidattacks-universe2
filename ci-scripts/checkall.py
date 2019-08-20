#!/usr/bin/env python3
# coding: utf8

"""
Script to check if defined rules are strictly applied
Replaces check-all.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.7
Patch notes 1.7:
- Externalized repo changes in a different function
"""
import os
import sys
import print_helper
import genchecker
import contentrules
import articlerules
import spelling
import getchanges

EXIT_CODE = 0

if len(sys.argv) > 2:
    print_helper.print_failure("Error! too many arguments\n")
else:
    if len(sys.argv) == 2 and sys.argv[1] != 'changes':
        print_helper.print_failure(sys.argv[1]+" <- Unrecognized argument\n")

if len(sys.argv) == 2 and sys.argv[1] == 'changes':
    #get changes in the repo:
    CHANGES, EXIT_CODE = getchanges.repochanges(EXIT_CODE)

    for FILE in CHANGES:
        print_helper.print_unknown(FILE+"\n")
    print_helper.print_warning("^ Modified files\n")
    print_helper.print_success("Checking recent changes to the repo ...\n")
    EXIT_CODE = genchecker.genchecks(EXIT_CODE)

    for FILE in CHANGES:
        if '.adoc' in FILE:
            EXIT_CODE = contentrules.rulechecker(FILE, EXIT_CODE)
            EXIT_CODE = spelling.spellchecker(FILE, EXIT_CODE)
            if "content/blog" in FILE:
                EXIT_CODE = articlerules.artchecker(FILE, EXIT_CODE)
    print_helper.print_success("Done! \n")

if len(sys.argv) == 1:
    print_helper.print_success("Checking all asciidoc files in repo ...\n")
    FILES = os.popen('find content/ -iname "*.adoc"').read()
    EXIT_CODE = genchecker.genchecks(EXIT_CODE)
    FILES = FILES.split()
    for CHECK in FILES:
        EXIT_CODE = contentrules.rulechecker(CHECK, EXIT_CODE)
        EXIT_CODE = spelling.spellchecker(CHECK, EXIT_CODE)
        if "content/blog" in CHECK:
            EXIT_CODE = articlerules.artchecker(CHECK, EXIT_CODE)
    print_helper.print_success("Done! \n")

sys.exit(EXIT_CODE)
