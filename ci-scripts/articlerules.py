#!/usr/bin/env python3
# coding: utf8
"""
Script that checks structure and rules in blog entries
Replaces check-articles.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.5
Patch notes 1.5:
- Use error_print function
"""

import os
from print_helper import error_print
from rules import ARTRULES

def artchecker(path, exit_code):
    """
    Define checks for blog articles
    """

    #check that every article has valid category
    art_cat = os.popen("pcregrep -o '(?<=^:category: ).*$' "+path).read()
    art_cat = art_cat.replace('\n', '')
    if "blog" in path:
        out = os.popen("pcregrep  '"+art_cat+"' categories.lst ").read()
    if not out:
        message = art_cat+ " does not match any valid category "\
                 "in categories list file."
        error_print(path, '', message)
        exit_code = 1

    #check that every article has valid tags
    art_tags = os.popen("pcregrep -o '(?<=^:tags: ).*$' "+path).read()
    art_tags = art_tags.replace('\n', '')
    art_tags = art_tags.split(", ")
    for tag in art_tags:
        if "blog/" in path:
            out = os.popen("pcregrep  '"+tag+"' tags.lst ").read()
        if not out:
            message = tag+" does not match any valid tag in tags list file."
            error_print(path, '', message)
            exit_code = 1
    # Temporary disabled to add source metadata in articles
    # Check that every article has a proper Word Count and LIX metrics:
    # os.system("sh exttxt.sh "+path+" >> temp.txt")
    # word_count = os.popen("style temp.txt | pcregrep -o '[0-9]+ words,'\
    #                | tr -d [[:alpha:]][[:punct:]][[:blank:]]").read()
    # lix = os.popen("style temp.txt | pcregrep -o 'Lix: [0-9]+'\
    #                | tr -d [[:alpha:]][[:punct:]][[:blank:]]").read()
    # os.system("rm -rf temp.txt")

    # if int(lix) >= 50:
    #     message = "LIX must be lower than 50"
    #     error_print(path, "Current LIX: "+lix, message)
    #     exit_code = 1

    # if not 800 <= int(word_count) <= 1200:
    #     message = "Word count must be in range [800-1200]"
    #     error_print(path, "Current Word Count: "+word_count, message)
    #     exit_code = 1

    #  Many other repetitive checks:
    for check, errmessage in ARTRULES.items():
        out = os.popen(check +"  "+ path).read()
        if out:
            error_print(path, out, errmessage)
            exit_code = 1

    return exit_code
