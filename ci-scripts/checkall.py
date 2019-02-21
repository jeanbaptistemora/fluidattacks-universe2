#!/usr/bin/env python
# coding: utf8

"""
Script to check if defined rules are strictly applied
Replaces check-all.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.0
"""
import os
import sys
import print_helper
import re
import genchecker
import contentrules

EXIT1 = 0
EXIT2 = 0

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
  print_helper.print_warning('Number of commits: '+NCOMMITS+'\n')
  CHANGES = os.popen('git diff HEAD~'+NCOMMITS+' --name-only').read()
  CHANGES = CHANGES.split()

  for FILE in CHANGES:
    print (FILE)
  print_helper.print_warning("^ Modified files\n")
  print_helper.print_success("Checking recent changes to the repo ...\n")
  EXIT1 = genchecker.genchecks(EXIT1)

  for FILE in CHANGES:
    if '.adoc' in FILE:
      EXIT2 = contentrules.rulechecker(FILE, EXIT2)
  print_helper.print_success("Done! \n")

if len(sys.argv) == 1:
  print_helper.print_success("Checking all asciidoc files in repo ...\n")
  FILES = os.popen('find content/ -iname "*.adoc"').read()
  EXIT1 = genchecker.genchecks(EXIT1)
  FILES = FILES.split()
  for CHECK in FILES:
    EXIT2 = contentrules.rulechecker(CHECK, EXIT2)
  print_helper.print_success("Done! \n")

sys.exit(EXIT1 or EXIT2)
