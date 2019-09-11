#!/usr/bin/env python3
# coding: utf8
"""
Script that checks structure and rules in blog entries
Replaces check-articles.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.4
Patch notes 1.4:
- Externalize repetitive checks
"""

import os
import print_helper as ph
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
        ph.print_failure("Issue found in "+path+" \n")
        ph.print_warning(art_cat+" does not match any valid category " \
                                   "in categories list file.\n\n")
        exit_code = 1

    #check that every article has valid tags
    art_tags = os.popen("pcregrep -o '(?<=^:tags: ).*$' "+path).read()
    art_tags = art_tags.replace('\n', '')
    art_tags = art_tags.split(", ")
    for tag in art_tags:
        if "blog/" in path:
            out = os.popen("pcregrep  '"+tag+"' tags.lst ").read()
        if not out:
            ph.print_failure("Issue found in "+path+" \n")
            ph.print_warning(tag+" does not match any valid tag " \
                                      "in tags list file.\n\n")
            exit_code = 1

    # Check that every article has a proper Word Count and LIX metrics:
    os.system("sh exttxt.sh "+path+" >> temp.txt")
    word_count = os.popen("style temp.txt | pcregrep -o '[0-9]+ words,'\
                   | tr -d [[:alpha:]][[:punct:]][[:blank:]]").read()
    lix = os.popen("style temp.txt | pcregrep -o 'Lix: [0-9]+'\
                   | tr -d [[:alpha:]][[:punct:]][[:blank:]]").read()
    os.system("rm -rf temp.txt")

    if int(lix) >= 50:
        ph.print_failure("Issue found in "+path+"\n")
        ph.print_failure("Current LIX: "+lix)
        ph.print_warning("LIX must be lower than 50\n\n")
        exit_code = 1

    if not 800 < int(word_count) < 1200:
        ph.print_failure("Issue found in "+path+"\n")
        ph.print_failure("Current Word Count: "+word_count)
        ph.print_warning("Word count must be in range [800-1200]\n\n")
        exit_code = 1

    #  Many other repetitive checks:
    for regex, message in ARTRULES.items():
        out = os.popen(regex +"  "+ path).read()
        if out:
            ph.print_failure("Issue found in "+path+"\n")
            ph.print_failure(out)
            ph.print_warning(message+"\n\n")
            exit_code = 1

    return exit_code
