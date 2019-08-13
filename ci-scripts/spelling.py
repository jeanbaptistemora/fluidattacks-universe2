#!/usr/bin/env python3
# coding: utf8

"""
Script that checks strict spelling of certain words
defined in strict-words.lst
Replaces check-spelling.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.2:
Patch note 1.2:
- Comply with pylint
"""

import os
import re
import print_helper

def spellchecker(path, exit_code):
    """
    Define strict spelling convention
    """
    correctwds = os.popen("cat strict-words.lst").read()
    correctwds = correctwds.split('\n')
    correctwds = filter(None, correctwds)
    for correct in correctwds:
        if " " in correct:
            srch = correct.replace(' ', r'(\s)?')
        else:
            srch = correct
        #Temporary file to run checks
        os.system("./exttxt.sh "+path+" >> temp.txt")
        out = os.popen("pcregrep -ioM '"+srch+"' temp.txt").read()
        if out:
            rgx = r'(\s|^)[\*|\+|\(]?'+srch+r'[\*\+\)]?[\.\:\;\,]?(\s|\\n|\])'
            raw = os.popen("pcregrep -ioM '"+rgx+"' temp.txt").read()
            raw = raw.split('\n')
            raw = filter(None, raw)
            for w_d in raw:
                word = re.sub(r'^\s|\*|\+|\(|\)|\.|\:|\;|\,|\[|\]|\s$', '', w_d)
                if word:
                    if word != correct:
                        print_helper.print_failure("Issue found in "+path+"\n")
                        print_helper.print_warning("The spelling "+word+" is incorrect. "\
                                                   "The only spelling admitted is "+correct+"\n\n")
                        exit_code = 1
        #Remove temporary file
        os.system("rm -r temp.txt")

    return exit_code
