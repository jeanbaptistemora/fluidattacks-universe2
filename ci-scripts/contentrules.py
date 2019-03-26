#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script that defines the rules to be applied to the web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.1
Patch notes 1.1:
- Using Python3
- Updated functions to use Python3 sintax
"""

import os
import print_helper
import sys

def rulechecker(PATH, EXIT_CODE):
  #Define Rules

  # Check use of incorrect names to address the company
  OUT = os.popen("pcregrep -on 'Fluid(?!\WAttacks)|Fluidsignal\ "\
                 "Group|fluidsignal\ |\ fluid[)}\ \]] |FLUID\W|FLUIDAttacks' " \
                 +PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The only accepted name is Fluid Attacks. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check blank spaces after headers
  OUT = os.popen("pcregrep -Mrn '^=.*.[A-Z].*.*\n.*[A-Z]' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Leave a blank space after a header. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that the references are numbered
  OUT = os.popen("pcregrep -Mnr '^== Referenc.*.*\n.*\n[A-Za-z]' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("References must be numbered. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check the titles of the images are well placed
  OUT = os.popen("pcregrep -Mnr 'image::.*\n\.[a-zA-Z]' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Image captions are placed "\
                               "before the image, not after. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that slugs have under 44 characters
  OUT = os.popen("pcregrep -nr  '^:slug: .{44,}' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The \"slug\" can have 43 characters maximum. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

    # Check that 4 '-' delimit the code block, not more, not less
  OUT = os.popen("pcregrep -nr '^-{5,}' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Code blocks must be delimited "\
                               "by exactly four hyphens '-'. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that the start attribute is never used
  OUT = os.popen("pcregrep  -nr '\[start' " +PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Do not use the \"start\" attribute for list "\
                               "numbering, use a plus sing '+' to concatenate "\
                               "the content that breaks the numbering. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that the slug ends in a '/'
  OUT = os.popen("pcregrep -nr '^:slug:.*[a-z]$' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The \"slug\" must end in '/'. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check alternative text in images
  OUT = os.popen("pcregrep -Mnr 'image\:\:.*\[\]' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Images do not have alt attribute."\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check for multiple main title
  OUT = os.popen("pcregrep -nr '^=\s.*$' "+PATH).read()
  OUT = OUT.split('\n')
  OUT = list(filter(None, OUT))
  if len(OUT) > 1:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("\nMultiple main titles defined. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check double quotes are not used in the title
  OUT = os.popen("pcregrep -nr '^={1,6}\s.*\"' "+PATH).read()
  if len(OUT) > 1:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Do not use double quotes \" in titles. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that code does not follow inmmediatly after a paragraph
  OUT = os.popen("pcregrep -Mnr '^[a-zA-Z0-9].*\n.*\[source' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Source code must be separated from a paragraph"\
                               " using a plus sign '+'. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

    OUT = os.popen("pcregrep -o '^=\s.{60,}' "+PATH).read()

  #Titles must not exceed 60 characters
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Titles must not exceed 60 characters. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that every .adoc has keywords defined
  OUT = os.popen("pcregrep -L '^:keywords:' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_warning("The attribute \"keywords\" must be defined. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that the every .adoc has description defined
  OUT = os.popen("pcregrep -L '^:description:' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_warning("The attribute \"description\" "\
                               "must be defined. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that translation names finish with '/'
  OUT = os.popen("pcregrep -nr '^:translate.*(?<!/)$' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The name of the translated file "\
                               "must end in '/'. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check all Asciidoc metadata are lowercase
  OUT = os.popen("pcregrep -nr '^:[A-Z]' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("All metadata attributes in asciidoc files "\
                               "must be lowercase."\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that titles and subtitles don't contain monospaces
  OUT = os.popen("pcregrep -nr '^=.*\+.+\+.*' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Titles and subtitles "\
                               "must not contain monospaces. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check the character '>' is not used in type button links
  OUT = os.popen("pcregrep -nr '\[button\].*>' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The '>>' characters are written by the style "\
                               "and are not needed in the source code. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  # Check that the meta description is in [250-300] char range
  OUT = os.popen("pcregrep -no '(?<=:description: ).{306,}$"\
                 "|(?<=:description:).{0,249}$' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Descriptions must be in the [250-300] "\
                               "characters range. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  # Check that there are exactly 6 keywords
  OUT = os.popen("pcregrep -o '(?<=^:keywords:).*' "+PATH).read()
  OUT = OUT.split(",")
  if len(OUT) != 6:
    print_helper.print_failure("Issue found in "+PATH)
    print_helper.print_warning("\nThere must be exactly 6 keywords. "\
                               "Please correct the file and try again.\n\n")

    EXIT_CODE = 1

  #Check that every URL starts with link:
  os.system("sh exttxt.sh "+PATH+">> temp.txt")
  OUT = os.popen("pcregrep '(\s|\w|\()http(s)?://' temp.txt").read()
  os.system('rm -r temp.txt')
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("URLs must start with \'link:\'. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  #Check that every URL has a short name between brackets:
  os.system("sh exttxt.sh "+PATH+">> temp.txt")
  OUT = os.popen("pcregrep 'link:http(s)?://' temp.txt").read()
  os.system('rm -r temp.txt')
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("URLs must have a short name between brackets. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  #Check that local URLs always uses relative paths:
  OUT = os.popen("pcregrep -n 'link:http(s)?://fluidattacks.com/web' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Local URLs must use relative paths. "\
                               "Please correct the file and try again.\n\n")
    EXIT_CODE = 1

  # Check if first source code has title
  OUT1 = os.popen("pcregrep --color -M '^\[source' "+PATH).read()
  if len(OUT1) > 0:
    OUT2 = os.popen("pcregrep --color -ML '^\..*\n\[source' "+PATH).read()
    if len(OUT2) > 0:
          print_helper.print_failure("Issue found in "+PATH+"\n")
          print_helper.print_warning("The first code block of an article "\
                                     "must have a title. "\
                                     "Please correct the file and try again.\n\n")
          EXIT_CODE = 1

  # Check that every keyword starts with uppercase
  OUT = os.popen("pcregrep -o '(?<=^:keywords:).*' "+PATH).read()
  OUT = OUT.replace('\n', '')
  OUT = OUT.replace(' ', '')
  OUT = OUT.split(",")
  for KEYWD in OUT:
    if KEYWD == "":
      print_helper.print_failure("Issue found in "+PATH+"\n")
      print_helper.print_warning("Keywords cannot be empty\n\n")
      EXIT_CODE = 1
    elif not KEYWD[0].isupper():
        print_helper.print_failure("Issue found in "+PATH+"\n")
        print_helper.print_warning("The keyword "+KEYWD+" is not in Title case. "\
                                   "Please correct the file and try again.\n\n")
        EXIT_CODE = 1

  # Check if source adoc has content past the 80th column
  os.system("sh exttxt.sh "+PATH+">> temp.txt")
  OUT = os.popen("pcregrep -nu '.{81,}' temp.txt").read()
  os.system('rm -r temp.txt')
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Documents must be wrapped at column 80. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  #Only autonomicmind.com is allowed
  OUT = os.popen("pcregrep -o '(autonomicmind.co(?!m))' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The only allowed domain is autonomicmind.com. "\
                               "Please correct the file and try again\n\n")
    EXIT_CODE = 1

  # Check that caption is not manually placed
  OUT = os.popen("pcregrep -ni '^\.imagen?\s\d|^\.figur(a|e)\s\d|^\.tabl(a|e)\s\d' "+PATH).read()
  if len(OUT) > 0:
    print_helper.print_failure("Issue found in "+PATH+"\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Captions must not contain \"Image #\", " \
                               "\"Figure #\" or \"Table #\".\n\n")
    EXIT_CODE = 1

  return EXIT_CODE
