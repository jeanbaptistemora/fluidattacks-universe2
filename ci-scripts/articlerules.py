#!/usr/bin/env python3
# coding: utf8
"""
Script that checks structure and rules in blog entries
Replaces check-articles.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.2
Patch notes 1.2:
- Removed spanish related linters
"""

import os
import print_helper

def artchecker(PATH, EXIT_CODE):

  #check that every article has valid category
  ARTCAT = os.popen("pcregrep -o '(?<=^:category:\s).*$' "+PATH).read()
  ARTCAT = ARTCAT.replace('\n', '')
  if "blog" in PATH:
    OUT = os.popen("pcregrep  '"+ARTCAT+"' categories.lst ").read()
  if not len(OUT):
    print_helper.print_failure("Issue found in "+PATH+" \n")
    print_helper.print_warning(ARTCAT+" does not match any valid category " \
                               "in categories list file.\n\n")
    EXIT_CODE = 1

  #check that every article has valid tags
  ARTTAGS = os.popen("pcregrep -o '(?<=^:tags:\s).*$' "+PATH).read()
  ARTTAGS = ARTTAGS.replace('\n', '')
  ARTTAGS = ARTTAGS.split(", ")
  for TAG in ARTTAGS:
    if "blog/" in PATH:
      OUT = os.popen("pcregrep  '"+TAG+"' tags.lst ").read()
    if not len(OUT):
      print_helper.print_failure("Issue found in "+PATH+" \n")
      print_helper.print_warning(TAG+" does not match any valid tag " \
                               "in tags list file.\n\n")
      EXIT_CODE = 1

  #Check that every article in blog has a valid title lenght
  OUT = os.popen("pcregrep -no '(?<=^=\s).{37,}' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The title lenght exceeds 35 characters. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  #Check that every article in blog has a subtitle defined
  OUT = os.popen("pcregrep -L '^:subtitle:' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_warning("The attributte \"subtitle\" must be defined. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  #Check that every article in blog has a valid subtitle lenght
  OUT = os.popen("pcregrep -o '(?<=^:subtitle: ).{56,}' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The subtitle lenght exceeds 55 characters. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  # Check that articles have alt description for their featured images
  OUT = os.popen("pcregrep -L  '^:alt:' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The articles must have the \"alt\" metadata "\
                               "set for their representative image. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  return EXIT_CODE
