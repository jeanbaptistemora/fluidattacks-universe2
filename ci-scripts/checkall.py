#!/usr/bin/env python3
# coding: utf8

"""
Script to check if defined rules are strictly applied
Replaces check-all.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.6
Patch notes 1.6:
- Comply with pylint
"""
import os
import sys
import print_helper
import genchecker
import contentrules
import articlerules
import spelling

EXIT_CODE = 0

if len(sys.argv) > 2:
    print_helper.print_failure("Error! too many arguments\n")
else:
    if len(sys.argv) == 2 and sys.argv[1] != 'changes':
        print_helper.print_failure(sys.argv[1]+" <- Unrecognized argument\n")

if len(sys.argv) == 2 and sys.argv[1] == 'changes':
    #get changes in the repo:
    BRANCH = os.popen('git rev-parse --abbrev-ref HEAD').read()
    BRANCH = BRANCH.split()
    REMOTE = os.popen('git rev-list --count --no-merges origin/master').read()
    LOCAL = os.popen('git rev-list --count --no-merges '+BRANCH[0]).read()
    NCOMMITS = str(int(LOCAL) - int(REMOTE))
    #Check if branch is updated:
    if int(NCOMMITS) < 1:
        print_helper.print_warning("Your current branch is behind master. ")
        print_helper.print_warning("Update your local repo and try again.\n")
        CHANGES = ''
        EXIT_CODE = 1
    else:
        print_helper.print_warning('Number of commits: '+NCOMMITS+'\n')
        #get only Added or Modified Files:
        CHANGES = os.popen('git diff HEAD~'+NCOMMITS+' --name-status  \
                     | pcregrep "^(M|A)" | sed "s/^[A-Z][[:blank:]]//" ').read()
        CHANGES = CHANGES.split()

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
