#!/usr/bin/env python3
# coding: utf8

"""
Script that checks strict spelling of certain words
defined in strict-words.lst
Replaces check-spelling.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.1:
Patch note 1.1:
- Using Python3
"""

import os
import print_helper
import re

def spellchecker(PATH, EXIT_CODE):
  CORRECTWDS = os.popen("cat strict-words.lst").read()
  CORRECTWDS = CORRECTWDS.split('\n')
  CORRECTWDS = filter(None, CORRECTWDS)
  for CORRECT in CORRECTWDS:
    if " " in CORRECT:
        SRCH = CORRECT.replace(' ', '(\s)?')
    else:
        SRCH = CORRECT
    #Temporary file to run checks
    os.system("./exttxt.sh "+PATH+" >> temp.txt")
    OUT = os.popen("pcregrep -ioM '"+SRCH+"' temp.txt").read()
    if len(OUT) > 0:
      RGX = '(\s|^)[\*|\+|\(]?'+SRCH+'[\*\+\)]?[\.\:\;\,]?(\s|\\n|\])'
      RAW = os.popen("pcregrep -ioM '"+RGX+"' temp.txt").read()
      RAW = RAW.split('\n')
      RAW = filter(None, RAW)
      for WD in RAW:
        WORD = re.sub('^\s|\*|\+|\(|\)|\.|\:|\;|\,|\[|\]|\s$' , '', WD)
        if len(WORD) > 0:
          if WORD != CORRECT:
            print_helper.print_failure("Issue found in "+PATH+"\n")
            print_helper.print_warning("The spelling "+WORD+" is incorrect. "\
                                       "The only spelling admitted is "+CORRECT+"\n\n")
            EXIT_CODE = 1
    #Remove temporary file
    os.system("rm -r temp.txt")

  return EXIT_CODE
