#!/usr/bin/env python3
# coding: utf8

"""
Script to get the modified files in the repository
Takes into account Added or Modified files
Author: Oscar Eduardo Prado oprado@fluidattacks.com
"""

import os
import print_helper as ph

def repochanges(exit_code):
    """
    Get changed files in the repo:
    """

    branch = os.popen('git rev-parse --abbrev-ref HEAD').read()
    branch = branch.split()
    remote = os.popen('git rev-list --count --no-merges origin/master').read()
    local = os.popen('git rev-list --count --no-merges '+branch[0]).read()
    ncommits = str(int(local) - int(remote))
    commithash = os.popen("git rev-parse HEAD").read()
    author = os.popen("git show -s --format='%aN <%aE>' "+commithash).read().split('\n')[0]
    name = author.split("<")[0]
    ph.print_warning("Author: "+author+"\n")

    ph.print_warning('Number of commits: '+ncommits+'\n')
    #get only Added or Modified Files:
    changes = os.popen('git diff HEAD~'+ncommits+' --name-status  \
                 | pcregrep "^(M|A)" | sed "s/^[A-Z][[:blank:]]//" ').read()
    changes = changes.split()

    #Check if commiter is in mailmap:
    in_mailmap = os.popen("grep '"+author+"' .mailmap").read()
    if not in_mailmap:
        ph.print_success("Hello "+name+",you seem to be new in here.\n")
        ph.print_success("Before making awesome changes to this repo, "
                         "please make yourself a place in the .mailmap\n")
        ph.print_success("Use the format: FirstName LastName <email>\n")
        exit_code = 1

    return changes, exit_code
