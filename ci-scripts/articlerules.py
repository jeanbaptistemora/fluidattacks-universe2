#!/usr/bin/env python3
# coding: utf8
"""
Script that checks structure and rules in blog entries
Replaces check-articles.sh
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.3
Patch notes 1.3:
- Comply with pylint
"""

import os
import print_helper

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
        print_helper.print_failure("Issue found in "+path+" \n")
        print_helper.print_warning(art_cat+" does not match any valid category " \
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
            print_helper.print_failure("Issue found in "+path+" \n")
            print_helper.print_warning(tag+" does not match any valid tag " \
                                      "in tags list file.\n\n")
            exit_code = 1

    #Check that every article in blog has a valid title lenght
    out = os.popen("pcregrep -no '(?<=^= ).{37,}' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The title lenght exceeds 35 characters. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    #Check that every article in blog has a subtitle defined
    out = os.popen("pcregrep -L '^:subtitle:' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_warning("The attributte \"subtitle\" must be defined. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    #Check that every article in blog has a valid subtitle lenght
    out = os.popen("pcregrep -o '(?<=^:subtitle: ).{56,}' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The subtitle lenght exceeds 55 characters. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    # Check that articles have alt description for their featured images
    out = os.popen("pcregrep -L  '^:alt:' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The articles must have the \"alt\" metadata "\
                                   "set for their representative image. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    # Check that every article has a proper Word Count and LIX metrics:
    os.system("sh exttxt.sh "+path+" >> temp.txt")
    word_count = os.popen("style temp.txt | pcregrep -o '[0-9]+ words,'\
                   | tr -d [[:alpha:]][[:punct:]][[:blank:]]").read()
    lix = os.popen("style temp.txt | pcregrep -o 'Lix: [0-9]+'\
                   | tr -d [[:alpha:]][[:punct:]][[:blank:]]").read()
    os.system("rm -rf temp.txt")

    if int(lix) >= 50:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure("Current LIX: "+lix)
        print_helper.print_warning("LIX must be lower than 50\n\n")
        exit_code = 1

    if not 800 < int(word_count) < 1200:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure("Current Word Count: "+word_count)
        print_helper.print_warning("Word count must be in range [800-1200]\n\n")
        exit_code = 1

    return exit_code
