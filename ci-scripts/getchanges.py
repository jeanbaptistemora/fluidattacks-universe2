#!/usr/bin/env python3
# coding: utf8

"""
Script to get the modified files in the repository
Takes into account Added or Modified files
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.0
Patch notes 1.0:
- Comply with pylint
"""

import os
import print_helper

def repochanges(exit_code):
    """
    Get changed files in the repo:
    """

    branch = os.popen('git rev-parse --abbrev-ref HEAD').read()
    branch = branch.split()
    remote = os.popen('git rev-list --count --no-merges origin/master').read()
    local = os.popen('git rev-list --count --no-merges '+branch[0]).read()
    ncommits = str(int(local) - int(remote))
    #Check if branch is updated:
    if int(ncommits) < 1:
        print_helper.print_warning("Your current branch is behind master. ")
        print_helper.print_warning("Update your local repo and try again.\n")
        changes = ''
        exit_code = 1
    else:
        print_helper.print_warning('Number of commits: '+ncommits+'\n')
        #get only Added or Modified Files:
        changes = os.popen('git diff HEAD~'+ncommits+' --name-status  \
                     | pcregrep "^(M|A)" | sed "s/^[A-Z][[:blank:]]//" ').read()
        changes = changes.split()

    return changes, exit_code
