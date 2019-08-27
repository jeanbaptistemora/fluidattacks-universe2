#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script that defines the rules to be applied to the web repo
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.2
Patch notes 1.2:
- Comply with pylint
"""

import os
import print_helper

def rulechecker(path, exit_code):
    """
    Define Rules for web content
    """

    # Check use of incorrect names to address the company
    out = os.popen("pcregrep -on 'Fluid(?! Attacks)|Fluidsignal Group\
                   |fluidsignal\\ |\\ fluid[)}\\ \\]] |FLUID\\W|FLUIDAttacks' " \
                   +path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The only accepted name is Fluid Attacks. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check blank spaces after headers
    out = os.popen("pcregrep -Mrn '^=.*.[A-Z].*.*\n.*[A-Z]' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Leave a blank space after a header. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that the references are numbered
    out = os.popen("pcregrep -Mnr '^== Referenc.*.*\n.*\n[A-Za-z]' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("References must be numbered. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check the titles of the images are well placed
    out = os.popen("pcregrep -Mnr 'image::.*\n\\.[a-zA-Z]' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Image captions are placed "\
                                   "before the image, not after. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that slugs have under 44 characters
    out = os.popen("pcregrep -nr  '^:slug: .{44,}' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The \"slug\" can have 43 characters maximum. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that 4 '-' delimit the code block, not more, not less
    out = os.popen("pcregrep -nr '^-{5,}' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Code blocks must be delimited "\
                                   "by exactly four hyphens '-'. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that the start attribute is never used
    out = os.popen("pcregrep  -nr '\\[start' " +path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Do not use the \"start\" attribute for list "\
                                   "numbering, use a plus sing '+' to concatenate "\
                                   "the content that breaks the numbering. "\
                                  "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that the slug ends in a '/'
    out = os.popen("pcregrep -nr '^:slug:.*[a-z]$' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The \"slug\" must end in '/'. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check alternative text in images
    out = os.popen("pcregrep -Mnr 'image\\:\\:.*\\[\\]' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Images do not have alt attribute."\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check for multiple main title
    out = os.popen("pcregrep -nr '^=\\s.*$' "+path).read()
    out = out.split('\n')
    out = list(filter(None, out))
    if len(out) > 1:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("\nMultiple main titles defined. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check double quotes are not used in the title
    out = os.popen("pcregrep -nr '^={1,6}\\s.*\"' "+path).read()
    if len(out) > 1:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Do not use double quotes \" in titles. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that code does not follow inmmediatly after a paragraph
    out = os.popen("pcregrep -Mnr '^[a-zA-Z0-9].*\n.*\\[source' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Source code must be separated from a paragraph"\
                                   " using a plus sign '+'. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    #Titles must not exceed 60 characters
    out = os.popen("pcregrep -o '^=\\s.{60,}' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Titles must not exceed 60 characters. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that every .adoc has keywords defined
    out = os.popen("pcregrep -L '^:keywords:' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_warning("The attribute \"keywords\" must be defined. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that the every .adoc has description defined
    out = os.popen("pcregrep -L '^:description:' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_warning("The attribute \"description\" "\
                                   "must be defined. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that translation names finish with '/'
    out = os.popen("pcregrep -nr '^:translate.*(?<!/)$' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The name of the translated file "\
                                   "must end in '/'. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check all Asciidoc metadata are lowercase
    out = os.popen("pcregrep -nr '^:[A-Z]' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("All metadata attributes in asciidoc files "\
                                   "must be lowercase."\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that titles and subtitles don't contain monospaces
    out = os.popen("pcregrep -nr '^=.*\\+.+\\+.*' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Titles and subtitles "\
                                   "must not contain monospaces. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that the meta description is in [250-300] char range
    out = os.popen("pcregrep -no '(?<=^:description: ).{306,}$"\
                     "|(?<=^:description:).{0,249}$' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Descriptions must be in the [250-300] "\
                                   "characters range. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    # Check that there are exactly 6 keywords
    out = os.popen("pcregrep -o '(?<=^:keywords:).*' "+path).read()
    out = out.split(",")
    if len(out) != 6:
        print_helper.print_failure("Issue found in "+path)
        print_helper.print_warning("\nThere must be exactly 6 keywords. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    #Check that every URL starts with link:
    os.system("sh exttxt.sh "+path+">> temp.txt")
    out = os.popen("pcregrep '(\\s|\\w|^|\\()http(s)?://' temp.txt").read()
    os.system('rm -r temp.txt')
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("URLs must start with \'link:\'. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    #Check that every URL has a short name between brackets:
    os.system("sh exttxt.sh "+path+">> temp.txt")
    out = os.popen("pcregrep 'link:http(s)?://' temp.txt").read()
    os.system('rm -r temp.txt')
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("URLs must have a short name between brackets. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    #Check that local URLs always uses relative paths:
    out = os.popen("pcregrep -n 'link:http(s)?://fluidattacks.com/web' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Local URLs must use relative paths. "\
                                   "Please correct the file and try again.\n\n")
        exit_code = 1

    # Check if first source code has title
    out1 = os.popen("pcregrep --color -M '^\\[source' "+path).read()
    if out1:
        out2 = os.popen("pcregrep --color -ML '^\\..*\n\\[source' "+path).read()
        if out2:
            print_helper.print_failure("Issue found in "+path+"\n")
            print_helper.print_warning("The first code block of an article "\
                                       "must have a title. "\
                                       "Please correct the file and try again.\n\n")
            exit_code = 1

    # Check that every keyword starts with uppercase
    out = os.popen("pcregrep -o '(?<=^:keywords:).*' "+path).read()
    out = out.replace('\n', '')
    out = out.replace(' ', '')
    out = out.split(",")
    for keywd in out:
        if keywd == "":
            print_helper.print_failure("Issue found in "+path+"\n")
            print_helper.print_warning("Keywords cannot be empty\n\n")
            exit_code = 1
        elif not keywd[0].isupper():
            print_helper.print_failure("Issue found in "+path+"\n")
            print_helper.print_warning("The keyword "+keywd+" is not in Title case. "\
                                       "Please correct the file and try again.\n\n")
            exit_code = 1

    # Check if source adoc has content past the 80th column
    os.system("sh exttxt.sh "+path+">> temp.txt")
    out = os.popen("pcregrep -nu '.{81,}' temp.txt").read()
    os.system('rm -r temp.txt')
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Documents must be wrapped at column 80. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    #Only autonomicmind.com is allowed
    out = os.popen("pcregrep -o '(autonomicmind.co(?!m))' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("The only allowed domain is autonomicmind.com. "\
                                   "Please correct the file and try again\n\n")
        exit_code = 1

    # Check that caption is not manually placed
    out = os.popen("pcregrep -ni '^\\.image\\s\\d|^\\.table\\s\\d|^\\.figure\\s\\d\' "+path).read()
    if out:
        print_helper.print_failure("Issue found in "+path+"\n")
        print_helper.print_failure(out)
        print_helper.print_warning("Captions must not contain \"Image #\", " \
                                   "\"Figure #\" or \"Table #\".\n\n")
        exit_code = 1

    return exit_code
